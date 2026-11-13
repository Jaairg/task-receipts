# 4. Handle only known errors during development

- **Date:** 2026-07-25
- **Status:** Accepted

## Context

Printing touches several things that can fail: the USB printer, Playwright and image
conversion. Printer connection errors in particular came up often while building the
app (printer not found, `[Errno 16] Resource busy`, `[Errno 19]` device
disconnected).

## Decision

While developing, handle only errors that are known and understood, each with a
specific message for the user. Don't add a generic catch-all: let unknown errors
crash the app so they're visible and can be understood.

## Consequences

- `print_receipt` catches `USBNotFoundError` and specific `usb.core.USBError` codes
  (16, 19) and flashes a message for each one. Anything else surfaces as a crash.
- Bugs aren't hidden behind a vague "something went wrong" message.
- Before running this in production, a catch-all handler will be needed. That change
  gets its own ADR.
