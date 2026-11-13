# 6. Support attended printing only

- **Date:** 2026-11-13 (recorded retroactively; decided earlier)
- **Status:** Accepted

## Context

The app can confirm that a job was *sent* to the printer, but not that a receipt was
*printed*: the printer's sensor states never reach the code.

## Decision

Support attended printing, not unattended. The app has no way to observe the print
result, so a person has to be the one who confirms the receipt exists.

## Alternatives considered

- **Ask the user to confirm every print.** Rejected: it adds a step to every print
  to catch a rare failure, while reprinting already covers that failure and costs
  nothing when things go well.

## Consequences

Because of the "sent but no receipt" case, these follow-up features are planned
(they depend on the database work in progress on `db-migration`):

- A database column records *when the bytes were sent* to the printer (`sent_at`),
  instead of claiming the job was printed.
- Reprinting is a first-class action, not an edge case. A task must be printable
  again from the list view, because paper jams, receipts get lost and ink fades.
- Completing a task needs a path that doesn't rely on a QR code: a "mark done" button
  in the web UI, for the same reason.
