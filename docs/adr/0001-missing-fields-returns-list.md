# 1. Session validation returns a list of missing field names

- **Date:** 2026-05-09
- **Status:** Superseded by [ADR-0005](0005-validate-on-save.md)

## Context

Before printing can go ahead, the session must contain `task_name`, `date_str` and
`priority_level`. The app needs to check this, and when data is missing it needs to
tell the user *what* is missing so they understand why printing couldn't continue.

## Decision

`get_session_missing_fields()` returns a list of strings: the names of the fields
missing from the session. An empty list means the session is valid. A non-empty list
means validation failed, and its contents say which fields to fix.

## Alternatives considered

- **Return a boolean (True/False).** Rejected: the caller would know *that*
  validation failed, but not *what* failed, so it couldn't tell the user why printing
  was blocked.

## Consequences

- The function returns raw field names, not user-facing messages. This keeps it
  focused on validation and leaves message formatting to the caller, which helps when
  the same information is shown in different places (for example a flash message vs.
  an inline form error).

### Related decision: rename

The function was first called `session_has_required_data` in pseudocode, which
suggested a boolean return. It was renamed to `get_session_missing_fields` to match
what it actually returns. The `get_` prefix signals that it retrieves a value, and
`missing_fields` says what that value contains.
