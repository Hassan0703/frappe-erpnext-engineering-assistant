# Data Migration Plan

**Purpose:** define scope, source snapshot, mapping approach, sequencing, and acceptance for a data
migration.

**How to use:** complete before writing any load script. The plan is approved by the business owner,
not only by engineering.

---

## 1. Scope

| Item | Value |
|---|---|
| Engagement / ticket ID | |
| Source system(s) and owner | |
| Target system, site, company/entities | |
| In scope (entities, date ranges) | |
| Explicitly out of scope | |
| Cutover date / freeze window | |
| Migration owner | |
| Reconciliation sign-off owner (business) | |

## 2. Source access and snapshot

| Item | Value |
|---|---|
| Access method (replica/extract/API) | |
| Extract timestamp | |
| Row count / checksum reference | |
| Access restrictions (PII, masked fields) | |
| Extract location (secured) | |
| Re-extract policy (delta) | |

## 3. Source profile summary

| Entity | Rows | Distinct key | Duplicates | Nulls in required fields | Orphans | Encoding/date/currency notes |
|---|---|---|---|---|---|---|
| | | | | | | |

## 4. Approach

| Decision | Choice | Reason |
|---|---|---|
| Natural key per entity | | |
| Duplicate rule (golden record) | | |
| Load order / waves | | |
| Import method (tool / script / API) | | |
| Validation level (full vs fast path) | | |
| Idempotency strategy | | |
| Notifications during load | disabled | avoid emailing historical documents |

## 5. Field mapping reference

See `data-mapping.md`. Summary of complex transforms:

| # | Entity | Transform | Risk |
|---|---|---|---|
| 1 | | | |

## 6. Environment and rehearsal

| Item | Value |
|---|---|
| Target versions (Frappe/ERPNext) | |
| Rehearsal environment | |
| Rehearsal date(s) | |
| Target reset method between rehearsals | |
| Measured throughput | |
| Estimated production runtime | |

## 7. Reconciliation plan

| Area | Method | Owner | Acceptance |
|---|---|---|---|
| Counts by entity/status | | | exact, or explained |
| Relationships / orphans | | | zero unexplained |
| Financial totals / opening balances | | | signed by finance |
| Stock quantities / valuation | | | signed by ops |
| Attachments | | | count + checksum sample |

## 8. Cutover and rollback

| Item | Value |
|---|---|
| Freeze and delta plan | |
| Go/no-go criteria | |
| Decision maker | |
| Rollback method | restore pre-cutover target / re-enable source |
| Data-loss window | |
| Hypercare window / owner | |

## 9. Risks

| # | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |

## 10. Approvals

| Role | Name | Date |
|---|---|---|
| Business owner | | |
| Finance owner (if money/stock) | | |
| Implementer | | |
