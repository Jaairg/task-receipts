# 2. Use guard clauses in `print_receipt`

- **Date:** 2026-05-09
- **Status:** Accepted

## Context

`print_receipt` was missing a check for the POST method.

## Decision

The only way to print is to send a POST request that contains `print_receipt_button`
in the form, so both conditions are combined into one boolean, `is_print_submission`.
If it's false, this isn't a print submission and the function returns the template
right away. Otherwise it runs the printing logic and then returns the template.

## Alternatives considered

- **Nested conditionals.** This worked, but the nesting kept growing and buried the
  logic inside layers of `if` statements. Each extra level made the code harder to
  read.

## Consequences

- The function uses guard clauses: it exits early when a condition isn't met instead
  of nesting deeper. Each check's purpose is clear, and the main path stays at the
  top level of the function, which makes it easier to read and change later.

### Related decision: extract a helper

Returning early meant `render_template` would be called in two places with the same
arguments. `render_receipt_page()` was extracted so the rendering logic lives in one
place.
