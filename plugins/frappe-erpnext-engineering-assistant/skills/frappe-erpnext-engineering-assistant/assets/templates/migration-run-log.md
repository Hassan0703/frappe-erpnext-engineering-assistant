# Migration Run Log

**Purpose:** per-run evidence of what the migration actually did. One entry per execution (rehearsal or
production).

**How to use:** append a new entry for every run. Never overwrite a previous run. Record the exact
commands and the extract identity so results are reproducible.

---

## Run: `<id / date / environment>`

| Item | Value |
|---|---|
| Run ID | |
| Environment | rehearsal / staging / production |
| Started / finished (timezone) | |
| Duration | |
| Operator | |
| Code revision / script version | |
| Source extract timestamp | |
| Source extract checksum | |
| Target backup reference (pre-run) | |

### Waves executed

| # | Wave / entity | Command | Started | Finished | Result |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |

### Counts

| Entity | Read | Inserted | Updated | Skipped (already present) | Rejected | Notes |
|---|---|---|---|---|---|---|
| | | | | | | |
| **Total** | | | | | | |

> Read must equal inserted + updated + skipped + rejected, with any remainder explained below.

### Rejected records

| # | Entity | Source key | Reason | Raw row reference | Action taken |
|---|---|---|---|---|---|
| 1 | | | | | |

Export location of rejected rows: `<path>`

### Transform exceptions / manual corrections

| # | Record | Issue | Correction | Approved by |
|---|---|---|---|---|
| 1 | | | | |

### Errors and warnings

| Severity | Message | Count | Investigated? |
|---|---|---|---|
| | | | |

### Verification performed after this run

| Check | Result | Evidence |
|---|---|---|
| Idempotency re-run (inserted = 0) | | |
| Duplicate check on natural keys | | |
| Orphan link check | | |
| Count reconciliation | | |
| Financial reconciliation | | |
| Stock reconciliation | | |

### Outcome

| Item | Value |
|---|---|
| Run result | pass / pass with exceptions / fail |
| Blocking issues | |
| Next action | |
| Signed off by / date | |
