# 7. Use a queue and a single worker for printing

- **Date:** 2026-11-13 (recorded retroactively; proposed earlier)
- **Status:** Proposed

## Context

The server makes a request to itself while a handler is blocked.

When the user prints a receipt, a request hits `/print_receipt` and a thread starts
running that route handler (call it *Handler A*). Handler A calls
`generate_receipt_image()` → `run(playwright)` → launches the browser →
`page.goto(url_for("print_receipt", _external=True))`. That `goto()` is an HTTP GET
to the app's own server (call it *Request B*). Handler A is paused at `goto()`,
waiting for Request B to return a page, but Request B needs a thread to run its
handler, and Handler A can't finish until Request B does.

This works today only because Flask's development server is threaded by default.
When Request B arrives while Thread 1 is stuck in Handler A, a second thread serves
it. Nothing was designed to make that happen; a default is quietly doing us a favor.

With only one thread, that thread is stuck inside Handler A at `page.goto()`, and
nobody is left to answer Request B. Handler A waits forever: a deadlock. This was
observed under `gunicorn --workers 1`, where the app hangs on the first print.

There is also a USB problem. Two prints at the same time both try to claim the
printer and collide with `usb.core.USBError: [Errno 16] Resource busy`. (Calling
`printer.close()` after each cut fixed this for prints one after another, but not
for prints at the same time.)

## Decision

Add a queue plus one worker. When the user clicks **PRINT**, the request adds a job
with the task's ID to the queue and immediately returns a message about what it
did. The worker loops over the queue: it takes an ID, starts Playwright, loads the
task from the database, renders the receipt with `goto("/receipt/<id>")` instead of
using the session, takes the screenshot and prints it.

## Alternatives considered

- **Rely on (more) threads.** Rejected because it isn't a fix, it's luck. It only
  works while a spare thread happens to be free. Under load, every thread can be busy
  with other users, nobody answers the self-request, and the app deadlocks again. It
  also does nothing about the USB race: with many threads, two prints can still grab
  the printer at the same time (errno 16).

## Consequences

- The self-request deadlock goes away: the page Playwright loads is served by a
  request handler that isn't waiting on anything.
- One worker means prints happen one at a time, so the USB race, and errno 16,
  can't happen.
- The handler returns *before* the print happens, so the accurate success message is
  "Queued for printing" (see [ADR-0006](0006-attended-printing.md)).
- Depends on tasks being stored in the database (in progress on `db-migration`).
