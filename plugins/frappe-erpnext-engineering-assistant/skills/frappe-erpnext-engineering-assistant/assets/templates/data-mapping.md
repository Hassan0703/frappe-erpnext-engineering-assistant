# Data Mapping

**Purpose:** the field-level contract between source and target. Ambiguous mapping is the most common
cause of post-cutover reconciliation failures.

**How to use:** one section per target DocType. Every target field that receives data must appear with
a rule. "Leave default" is a rule; a blank cell is not.

---

## Entity: `<Target DocType>`  (source: `<source table/object>`)

| Item | Value |
|---|---|
| Natural key | |
| Load order / wave | |
| Expected row count | |
| Owner | |
| Approval status | draft / approved |

| Target field | Type | Source field / expression | Transform | Null/blank rule | Validation | Failure behavior | Notes |
|---|---|---|---|---|---|---|---|
| name / naming | | | | | | reject / default | |
| | | | | | | | |
| custom_legacy_id | Data | | trim, uppercase | required | unique | reject | idempotency key |
| | | | | | | | |

### Transform definitions

| Name | Definition | Example |
|---|---|---|
| | | |

### Value maps (enumerations)

| Source value | Target value | Notes |
|---|---|---|
| | | |

### Date/time rules

| Item | Rule |
|---|---|
| Timezone conversion | |
| Inclusive/exclusive end dates | |
| Fiscal-year / period boundaries | |
| Backdated documents allowed? | |

### Money rules

| Item | Rule |
|---|---|
| Currency conversion | source rate, date, provider |
| Rounding | decimal places, method |
| Tax handling | template/account mapping |
| Precision storage | target field precision |

### Units of measure

| Source UOM | Target UOM | Conversion factor | Applies to |
|---|---|---|---|
| | | | |

### Relationships

| Target link field | Source reference | Resolution rule | If missing |
|---|---|---|---|
| | | | reject / create / leave empty (justify) |

### Attachments

| Source location | Target DocType/field | Privacy | Naming rule | Missing file behavior |
|---|---|---|---|---|
| | | public/private | | |

---

## Rejected-record handling

| Rejection reason | Count (last run) | Action | Owner |
|---|---|---|---|
| | | | |

## Known differences accepted

| # | Difference | Amount/count | Cause | Approved by | Date |
|---|---|---|---|---|---|
| 1 | | | | | |
