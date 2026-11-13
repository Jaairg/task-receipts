# 5. Validate form input when saving, not at print time

- **Date:** 2026-07-30
- **Status:** Accepted
- **Supersedes:** [ADR-0001](0001-missing-fields-returns-list.md)

## Context

[ADR-0001](0001-missing-fields-returns-list.md) validated the task *after* it had
been saved: `create_receipt` copied the form into the session, and when the user
pressed print, `print_receipt` called `get_session_missing_fields()`. If anything
was missing, it redirected back to `create_receipt`.

So the only thing the check could do with a failure was send the user back to the
form they had just left. Validating after the fact made no sense when the fix
always happened in `create_receipt` anyway.

The missing-fields list also wasn't used: the redirect carried no message, so the
user was sent back without being told what was wrong.

## Decision

Validate directly in `create_receipt` when the form is saved. The route loops over a
`required_fields` list of `(field, label)` pairs and reads each one with
`request.form.get(field, "").strip()`:

- If a field is empty, it flashes `Missing required field: <label>`.
- If it has a value, it's stored in the session.

Only when every field is present does the route redirect to `print_receipt`.
Otherwise it re-renders the form with the messages.

## Alternatives considered

- **Keep validating at print time, but pass the missing fields along with the
  redirect.** Rejected: it would fix the missing message, but the user would still
  make a round trip (save → print → back to the form) just to find out about
  something that could have been caught on save.

## Consequences

- Validation happens where the fix happens: no redirect, no round trip.
- Invalid input never reaches the session, so `print_receipt` can trust what's
  there, and `get_session_missing_fields()` was removed.
- The goal behind ADR-0001, telling the user *which* field is missing, is finally
  met: each empty field gets its own flash message on the form. Field labels live
  next to the field names in `required_fields`, so messages are formatted where
  they're shown.
