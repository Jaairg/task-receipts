# Architecture Decision Records

Each record explains one decision: the context, what was chosen, what was rejected,
and the consequences. Records are never rewritten. When a decision changes, the old
record is marked **Superseded** and a new one explains why.

Records marked "recorded retroactively" were decided during development but written
down later; their exact decision date wasn't kept.

| # | Decision | Status |
|---|----------|--------|
| [0001](0001-missing-fields-returns-list.md) | Session validation returns a list of missing field names | Superseded by 0005 |
| [0002](0002-guard-clauses-in-print-receipt.md) | Use guard clauses in `print_receipt` | Accepted |
| [0003](0003-extract-image-generation.md) | Extract image generation from `print_receipt` | Accepted |
| [0004](0004-handle-only-known-errors.md) | Handle only known errors during development | Accepted |
| [0005](0005-validate-on-save.md) | Validate form input when saving, not at print time | Accepted |
| [0006](0006-attended-printing.md) | Support attended printing only | Accepted |
| [0007](0007-print-queue-and-worker.md) | Use a queue and a single worker for printing | Proposed |
