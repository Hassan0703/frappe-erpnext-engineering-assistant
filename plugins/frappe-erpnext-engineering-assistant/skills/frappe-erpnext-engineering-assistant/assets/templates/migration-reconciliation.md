# Migration Reconciliation

**Purpose:** prove the target system is equivalent to the agreed source scope. This document is the
evidence that migration succeeded — not the absence of import errors.

**How to use:** complete after the final load, before cutover and again after the first live close.
Every difference is either zero, approved, or blocking.

---

## 1. Context

| Item | Value |
|---|---|
| Source system / extract timestamp | |
| Target site / company / entities | |
| As-at date (cutover) | |
| Currency / precision | |
| Frappe / ERPNext versions | |
| Prepared by / date | |
| Business reviewer | |

## 2. Counts

| Entity | Source | Target | Difference | Explained? | Approved? |
|---|---|---|---|---|---|
| Customers | | | | | |
| Suppliers | | | | | |
| Items | | | | | |
| Sales orders | | | | | |
| Sales invoices (submitted) | | | | | |
| Purchase invoices (submitted) | | | | | |
| Payments | | | | | |
| Journal entries | | | | | |
| Stock documents | | | | | |
| Attachments | | | | | |

By status:

| Entity | Draft | Submitted | Cancelled | Total |
|---|---|---|---|---|
| | | | | |

> Compare like with like: same date boundary, same status scope, same company/currency, and the same
> transformation rules recorded in `data-mapping.md`.

## 3. Relationships

| Check | Query/description | Failures | Explained? |
|---|---|---|---|
| Orphan customer links | | | |
| Orphan item links | | | |
| Orphan account/tax links | | | |
| Parent/child count mismatch | | | |
| Duplicate natural keys | | | |
| Missing required links | | | |

## 4. Financial reconciliation

| Check | Source | Target | Difference | Explanation | Approved by |
|---|---|---|---|---|---|
| Total debits = total credits | | | | | |
| Opening balances (per account) | | | | | |
| Trial balance vs source report | | | | | |
| AR aging (0–30/31–60/61–90/90+) | | | | | |
| AP aging | | | | | |
| Unreconciled payments | | | | | |
| Tax totals | | | | | |

Method and comparability notes (currency, rounding, date boundaries, excluded statuses):

```text

```

## 5. Inventory reconciliation

| Check | Source | Target | Difference | Explanation | Approved by |
|---|---|---|---|---|---|
| Quantity by item/warehouse | | | | | |
| Valuation total | | | | | |
| Negative stock items | | | | | |
| Batches / serials | | | | | |
| Expiry dates | | | | | |

## 6. Attachments and files

| Item | Source | Target | Difference |
|---|---|---|---|
| File count | | | |
| Total size | | | |
| Private files count | | | |
| Checksum sample matches | | | |

## 7. Transformation exceptions

| # | Record | Source value | Target value | Rule applied | Why |
|---|---|---|---|---|---|
| 1 | | | | | |

## 8. Known differences

| # | Difference | Amount/count | Cause | Impact | Owner | Approved by | Date |
|---|---|---|---|---|---|---|---|
| 1 | | | | | | | |

> Unapproved differences block cutover sign-off.

## 9. Conclusion

| Item | Value |
|---|---|
| Reconciled? | yes / yes with approved differences / no |
| Blocking items | |
| Prepared by / date | |
| Finance sign-off (name/date) | |
| Operations sign-off (name/date) | |
| Post-go-live re-reconciliation due | |
