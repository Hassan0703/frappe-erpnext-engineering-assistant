# Performance

Performance is a measured property. Do not claim a speedup without a before/after measurement on a
representative dataset.

## 1. Measure before changing

| Layer | How to measure |
|---|---|
| One query | `query.run(debug=True)` (Query Builder) or `frappe.db.sql(..., debug=True)` — prints SQL and execution time |
| Query plan | `bench --site <site> db-console` → `EXPLAIN <query>`, check index usage and rows examined |
| Slow queries | Database slow-query log; look for repeated identical queries (N+1) |
| Request | Browser network panel; time the endpoint before/after |
| Report/list | Time with production-like row counts and realistic filters; time the empty-result case too |
| Jobs | Queue depth and duration: `bench --site <site> show-pending-jobs`, `bench doctor`, worker logs |
| Disk/cache | Redis memory/evictions; `logs/` growth; backup size |

Record the change: dataset size, command, before, after. "Faster" without numbers is a guess.

## 2. Queries

- Fetch only needed fields: `frappe.get_all("Item", filters=..., fields=["name", "item_group"])`.
- Never fetch a document to read one field; use `frappe.db.get_value`, and `frappe.get_cached_value`
  for rarely-changing masters.
- Check existence with `frappe.db.exists` instead of loading and counting.
- Use `frappe.db.count` when you only need a number; do not load rows to `len()` them.
- Never `frappe.get_doc` inside a loop. Bulk fetch and map:

```python
# ❌ N+1
for row in self.items:
    group = frappe.db.get_value("Item", row.item_code, "item_group")

# ✅ one query
item_codes = [row.item_code for row in self.items]
groups = dict(frappe.get_all("Item", filters={"name": ("in", item_codes)},
                             fields=["name", "item_group"], as_list=True))
for row in self.items:
    group = groups.get(row.item_code)
```

- Aggregate in SQL/Query Builder (`Sum`, `Count`), not by loading rows into Python.
- Paginate large result sets (`limit`, `limit_start`); never return an unbounded list to the client.
- Add `search_index` to fields used in frequent filters and to fields used in `order_by`. Do not
  index everything — indexes slow writes and consume space.
- v16 changed the implicit default order from `modified` to `creation`. If a hot query relies on
  ordering, specify `order_by` explicitly so the index and plan are predictable.
- v16 parses `get_all`/`get_list` fields strictly: use dict/pypika function expressions instead of SQL
  strings, and `distinct=True` instead of `distinct field`. SQL-string forms that worked in v15 may
  error.

## 3. Writes

- Bulk field updates: `frappe.db.set_value(doctype, filters, field, value)` or a Query Builder
  `update`, but only when skipping controller validation is acceptable.
- Document-by-document `save()` is correct when validations, hooks, and ledger effects must run —
  batch it in a job, not a request.
- **Do not call `frappe.db.commit()` in request handlers or controllers.** In v16 transaction
  control is disabled inside document hooks, so the commit is a no-op rather than an error. Batch
  commits belong in standalone jobs/patches and must be restartable.
- Avoid write amplification: compute totals in one pass instead of re-saving on every row event.

## 4. Caching

- `frappe.get_cached_value` / `frappe.get_cached_doc` for settings and rarely-changing masters.
- Never cache user-specific or permission-filtered data in a shared cache key.
- Avoid long-lived in-process caches that survive permission changes; use framework caching and
  invalidate on write (a hook or `clear_cache` implementation).
- v16: `site_cache` requires hashable arguments — remove dict/list arguments or serialize them.
- v16: site/common config is cached for up to about a minute; do not assume instant effect.
- Cache is not a fix for an N+1; fix the query first.

## 5. Background jobs

```python
frappe.enqueue(
    "my_app.my_module.jobs.recalculate_balances",
    queue="long",
    timeout=1500,
    company=company,
    enqueue_after_commit=True,
)
```

- Anything slow (bulk processing, bulk email, external APIs, report generation, PDF batches) →
  `frappe.enqueue`.
- Choose the queue deliberately (short/long); a long job on the short queue starves interactive work.
- Use `enqueue_after_commit=True` when the job depends on data written by the current transaction.
- Jobs must: log errors with context, be safe to retry, be idempotent, and report progress for long
  runs (`frappe.publish_realtime` or a status record).
- Do not enqueue the same job twice for the same input; deduplicate with a key.
- Monitor queue depth; an unmonitored queue turns a slow feature into an outage.

## 6. Client performance

- Avoid `frappe.call` in `refresh` for data that rarely changes; load once in `onload` or pass data
  from the controller's `onload()` via `frm.doc.__onload`.
- Debounce calls triggered by typing.
- Don't fetch a list to display one value; ask the server for the value.
- Avoid rendering thousands of DOM nodes; paginate or use the list view.
- Keep asset bundles small; don't include a library for one helper.

## 7. Reports and printing

- Apply filters in the query, not in Python after fetching everything.
- Select only the columns the report shows.
- Index the fields used by common filters.
- Time reports at realistic data volume; a report that takes 2 seconds on 1,000 rows may take minutes
  on a million.
- v16 PDF generation via Chromium is heavier than wkhtmltopdf; batch/bulk printing belongs in a
  background job, and the first render on a cold server downloads Chromium.

## 8. Anti-patterns

- `fields=["*"]` in request paths and reports.
- Queries inside loops, or one query per row in a template.
- Loading a full document for a single value.
- Aggregating in Python after fetching all rows.
- `frappe.db.commit()` inside a handler.
- Unbounded queries and unbounded page sizes.
- Caching permission-filtered data globally.
- Adding an index to every field.
- Claiming a performance fix with no measurement.

## 9. Performance checklist

- [ ] Baseline measured (dataset, command, before).
- [ ] After measured (same dataset, same command).
- [ ] No queries inside loops; aggregates pushed to SQL.
- [ ] Explicit `fields`; pagination where lists can grow.
- [ ] Indexes added for hot filters/`order_by`, and the plan checked with `EXPLAIN`.
- [ ] No `commit()` in the request path; long work enqueued.
- [ ] Cache keys are not user/permission-specific unless intentional, with invalidation.
- [ ] Version-specific query APIs verified (v16 strict fields, default sort).
- [ ] Queue depth and job duration considered.
