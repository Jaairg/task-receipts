# 3. Extract image generation from `print_receipt`

- **Date:** 2026-07-19
- **Status:** Accepted

## Context

Creating the image is the heaviest thing the app does. To produce it, the app has
to start Playwright, pass the session cookie, open a page, take a screenshot and
convert it with Pillow. All of that lived inside `print_receipt`.

## Decision

Move it into a separate function, `generate_receipt_image()`, which returns the
converted image made from the Playwright screenshot.

## Consequences

- `print_receipt` is easier to read and maintain.
- Concerns are separated: each function has one clear purpose (render the image,
  send it to the printer, render the page).
