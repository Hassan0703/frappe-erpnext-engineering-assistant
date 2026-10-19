# Data Migration and Reconciliation

A migration is a controlled data-engineering project, not a CSV import. Success means the target
system is **provably equivalent** to the agreed source scope — not that the import finished without
errors.

**Hard rule:** never declare a migration successful because the error log is empty. Reconcile counts,
relationships, financial totals, and stock where applicable, and record the differences.

## 1. Start with scope and ownership

Write down, before touching data:

- Source systems, owners, and access method (read-only replica preferred).
- In-scope entities and date ranges; explicitly out-of-scope items.
- Cutover date, freeze window, and who can approve a go/no-go.
- Target company/entities, currencies, fiscal year, and localization.
- Who signs off reconciliation, and against which source report.

If the source owner cannot provide a stable extract, stop. A migration against a moving source
cannot be reconciled.

## 2. Source discovery and access constraints

- Prefer a read-only extract or replica. Do not run heavy queries against a live production source
  during business hours.
- Capture the extract time and a checksum/row count. Every later discrepancy must be explainable
  against that snapshot.
- Identify encoding, collation, timezone, and date format at the source. These cause silent
  corruption when assumed.
- Document inaccessible fields (encrypted, masked, legally restricted) and how they are handled.

## 3. Profile before mapping

For every source table/entity:

| Check | Why |
|---|---|
| Row count, distinct keys, nulls | Baseline and mapping completeness |
| Duplicates on the intended natural key | Prevents duplicate masters/transactions |
| Orphan foreign keys | Detects broken relationships before load |
| Min/max dates, timezone offsets | Date-boundary errors |
| Status/code enumerations | Map to target states, not guessed |
| Currency, precision, rounding | Financial mismatch |
| Units of measure and conversions | Quantity/value mismatch |
| Text encoding, trailing spaces, case variants | Matching and duplicate failures |
| Attachments: count, size, types, missing files | Scope and storage estimate |

Record the profile in `assets/templates/migration-plan.md`. Do not map a field you have not profiled.

## 4. Cleansing and duplicates

- Decide the **natural key** per entity (legacy ID, tax ID, email, SKU). Store it in the target as a
  dedicated field (e.g. `custom_legacy_id`) so re-runs are deterministic.
- Choose a golden record rule for duplicates (most recent, most complete, manual review).
- Do not merge accounts or parties silently. Produce a duplicate report and get business approval.
- Normalize codes and units before load, not after — post-load normalization creates untraceable
  differences.

## 5. Field mapping and transformations

`assets/templates/data-mapping.md` is the contract. For each target field record:

- Source field/expression and target field.
- Transformation (trim, uppercase, lookup, unit conversion, date shift, default).
- Null/blank policy (null vs empty string vs zero).
- Validation rule and failure behavior.
- Owner and approval status.

Specific traps:

- **Money:** source currency → target currency, exchange rate source and date, rounding policy.
  Never compare totals without accounting for currency and precision.
- **Dates:** timezone conversion, inclusive/exclusive end dates, fiscal-year boundaries.
- **Status:** map to the target's real states and `docstatus` (draft/submitted/cancelled), not just a
  label. A "Closed" source invoice may need to be submitted, not draft.
- **UOM:** convert quantities and rates consistently; a rate per box vs per unit changes totals.
- **Taxes:** map tax templates/accounts deliberately; do not let defaults silently change tax.
- **Names/identifiers:** target naming series and uniqueness; preserve legacy IDs for traceability.

## 6. Sequence and dependencies

Load in dependency order, in waves with a checkpoint after each:

1. Company, currency, fiscal year, chart of accounts, warehouses, UOMs, item groups, territories.
2. Master data: customers, suppliers, items, contacts, addresses, price lists, tax templates.
3. Opening balances and stock positions (use the target version's standard opening mechanisms).
4. Open transactions: sales orders, purchase orders, invoices, payments, journal entries.
5. Historical/closed transactions (if in scope).
6. Attachments and communications.
7. Reference/integrity repair and final reconciliation.

Never insert general-ledger or stock-ledger rows directly. Use the standard documents and
opening/reconciliation mechanisms so the target's accounting and stock engines stay consistent.

Parent-child documents: insert the parent with child rows in one document operation so totals and
child naming are handled by the framework. Do not insert child rows independently.

## 7. Import methods and performance

| Method | Use for | Notes |
|---|---|---|
| Data Import tool / `bench --site <site> data-import` | Bounded, reviewed datasets | Verified in v16.52; good for masters; validate templates and error reports |
| Custom migration script | Complex transforms, relationships, idempotency | Version-controlled, logged, restartable |
| Bulk insert APIs | Very large, simple tables | Verify API and validation bypass on your version; reconcile afterwards |

Script rules:

- Batch work and commit per batch **only** in a standalone migration/bench context, never in a web
  request or controller.
- Make each batch restartable: record progress and skip already-loaded natural keys.
- Disable outbound notifications/emails during load, or route them to a sink. Do not spam customers
  with historical documents.
- Run heavy loads through `bench execute`/a worker with a log file; do not hold a web request open.
- Measure throughput and estimate the cutover window from a real dry run.

## 8. Idempotency and repeatability

A migration you cannot re-run is a migration you cannot fix.

```python
def upsert_customer(row):
    existing = frappe.db.get_value("Customer", {"custom_legacy_id": row["id"]}, "name")
    if existing:
        return "skipped", existing
    doc = frappe.get_doc({
        "doctype": "Customer",
        "customer_name": row["name"].strip(),
        "custom_legacy_id": row["id"],
        ...
    })
    doc.insert(ignore_permissions=True)   # system migration context; comment why
    return "inserted", doc.name
```

- Use a unique constraint/index on the legacy key where supported.
- Update-vs-skip must be an explicit decision, recorded in the mapping.
- Re-running the same extract must produce the same counts (inserted = 0 on the second run).
- Reset the target from a backup between full rehearsals; do not "clean up" by hand and call it a
  fresh run.

## 9. Errors, rejects, and logs

Every run produces `assets/templates/migration-run-log.md` with:

- Extract identity (timestamp, checksum, row counts).
- Rows read / inserted / updated / skipped / rejected per entity.
- Rejected rows with source key and reason, exported to a file.
- Transform exceptions and manual corrections.
- Duration per wave and total.

Rules:

- Never silently skip a row. A skip is a counted, categorized outcome.
- Do not "fix" rejected rows by editing the target by hand without recording it.
- Fix the mapping or the source, then re-run the affected wave idempotently.

## 10. Reconciliation

`assets/templates/migration-reconciliation.md` is the evidence. Compare source snapshot to target:

**Counts**
- Total by entity, by `docstatus`, by company, by date range.
- Inserted + skipped + rejected must equal rows read, with an explained remainder.

**Relationships**
- Orphan checks on every link field in scope.
- Parent-child row counts and totals.
- Duplicate checks on natural keys.

**Financials**
- Debits = credits per company and in total.
- Trial balance / opening balances against the source's signed report.
- AR/AP aging buckets at the cutover date.
- Compare at the same date boundary, currency, precision, and status scope. Document every
  transformation that affects comparability.

**Inventory**
- Quantity by item/warehouse vs source at cutover.
- Valuation totals, including currency and costing method.
- Negative stock, batches, serials, and expiring items called out explicitly.

**Attachments**
- Count and total size vs source; checksum sample; private/public flag preserved.

**Known differences**
- Each difference: description, amount/count, cause, approval, owner, date.
- Unapproved differences block sign-off.

## 11. Cutover

Use `assets/templates/cutover-checklist.md`.

```text
[ ] Freeze source writes (or define delta-capture method)
[ ] Final delta extract and load
[ ] Final reconciliation; differences approved or zero
[ ] Permissions and roles verified with real users
[ ] Opening balances and stock signed off by finance/ops
[ ] Integrations pointed at the new system and tested
[ ] Email/notifications enabled (they were disabled during load)
[ ] Scheduler enabled; jobs verified
[ ] Backups taken immediately after go-live
[ ] Rollback trigger and decision-maker agreed
[ ] Hypercare window and owner named
```

Rollback for a migration usually means restoring the pre-cutover target and re-enabling the source.
State the data-loss window and get explicit approval before cutover.

## 12. Post-go-live

- Monitor Error Log, failed jobs, duplicate creation, and integration errors for the hypercare window.
- Run the first period close with the finance owner; reconcile again after live transactions begin.
- Keep the source read-only for an agreed period.
- Archive the mapping, run logs, reconciliation, and approvals with the project handover.

## 13. Anti-patterns

- "Import completed with no errors" presented as success.
- Loading transactions before masters, or children before parents.
- Direct inserts into ledger/stock tables.
- Comparing totals across different currencies, precisions, date boundaries, or status scopes.
- Hand-editing the target to fix rejects with no record.
- Re-running a non-idempotent script and duplicating data.
- Disabling validations globally to make the load pass.
- Leaving notifications enabled and emailing customers historical documents.
- Migrating attachments without privacy flags or checksums.
- No owner for reconciliation sign-off.

## 14. Checklist

- [ ] Scope, snapshot, source owner, and sign-off owner documented.
- [ ] Profile completed; duplicates, orphans, encodings, dates, currencies, UOMs known.
- [ ] Natural keys defined and stored in the target.
- [ ] Field mapping approved; null/rounding/status rules explicit.
- [ ] Load sequenced by dependency; no direct ledger/stock inserts.
- [ ] Script is idempotent and restartable; dry run rehearsed on a production-like target.
- [ ] Run log records read/inserted/updated/skipped/rejected per entity.
- [ ] Reconciliation covers counts, relationships, financials, stock, attachments, exceptions.
- [ ] Known differences approved by the business owner.
- [ ] Cutover checklist completed; rollback trigger agreed.
- [ ] Post-go-live monitoring and first-close reconciliation planned.
