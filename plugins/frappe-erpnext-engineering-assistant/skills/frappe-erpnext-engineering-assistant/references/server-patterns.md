# Server-side Patterns (Python)

Version note: the examples are v15-safe. Items marked **v16** changed behavior and must be checked
against the detected version (`version-compatibility.md`).

## 1. Controller skeleton

```python
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, cint, getdate, nowdate, get_link_to_form


class LoanApplication(Document):
    def validate(self):
        self.validate_dates()
        self.validate_items()
        self.set_totals()

    def before_submit(self):
        self.check_credit_limit()

    def on_submit(self):
        self.create_ledger_entries()

    def on_cancel(self):
        self.reverse_ledger_entries()

    # --- validations -------------------------------------------------
    def validate_dates(self):
        if self.to_date and getdate(self.to_date) < getdate(self.from_date):
            frappe.throw(_("To Date cannot be before From Date"))

    def validate_items(self):
        for row in self.items:
            if flt(row.qty) <= 0:
                frappe.throw(_("Row {0}: Qty must be greater than 0").format(row.idx))

    def set_totals(self):
        self.total = sum(flt(row.amount) for row in self.items)
```

Rules:

- One small, named method per concern; `validate()` reads like a table of contents.
- Use the right hook: `before_insert`, `validate`, `before_save`, `on_update`, `after_insert`,
  `before_submit`, `on_submit`, `before_cancel`, `on_cancel`, `on_trash`, `after_delete`,
  `on_change`, `before_rename`, `after_rename`.
- Don't do submit-only work in `validate`.
- Inside `validate`/`before_save`, set fields on `self` directly; never call `self.save()`.
- In `on_update`/`on_submit`, use `self.db_set("field", value)` for own fields; `db_set` skips
  validation by design.
- Use `frappe.utils` helpers (`flt`, `cint`, `getdate`, `nowdate`, `add_days`, `date_diff`) — never
  `float()`/`int()` on doc fields (they may be `None`).
- Do not put business logic in `hooks.py`; it is a registry of dotted paths.
- Do not suppress validation with `flags.ignore_validate`/`ignore_mandatory` to make a flow work.

## 2. Documents, transactions, and concurrency

Frappe wraps a request in a transaction. The framework commits on success and rolls back on an
unhandled exception.

- **Do not call `frappe.db.commit()` in controllers, `doc_events`, or whitelisted request handlers.**
  In v16 it is blocked from document hooks; in v15 it is still a defect because it breaks atomicity.
  Committing per batch is acceptable only in a standalone migration/job context, and then the work
  must be restartable.
- For a multi-step operation that must be all-or-nothing, let the exception propagate. If you need a
  partial rollback inside a larger flow, use a savepoint where the API is available:

```python
frappe.db.savepoint("before_items")
try:
    process_items(self)
except Exception:
    frappe.db.rollback(save_point="before_items")
    raise
```

- For read-modify-write on a shared record, lock the row:

```python
doc = frappe.get_doc("Loan Application", name, for_update=True)
```

  Keep the lock window short; do not call external services while holding it.
- Assume another request can modify the same document. Re-read before writing, or use `db_set` on a
  field whose value does not depend on stale data.
- External calls have side effects that a DB rollback cannot undo. Make them idempotent (request key),
  enqueue them after commit where appropriate, and record the outcome.
- `frappe.enqueue(..., enqueue_after_commit=True)` avoids enqueuing a job for data that later rolls
  back. Use it for jobs that depend on the transaction's writes.

## 3. Messages and errors

```python
frappe.throw(_("Customer {0} is disabled").format(frappe.bold(self.customer)))
frappe.throw(_("Not permitted"), frappe.PermissionError)
frappe.throw(msg, title=_("Missing Data"))

frappe.msgprint(_("{0} items updated").format(count), alert=True)   # toast
frappe.msgprint(_("Check these rows: {0}").format(", ".join(rows)), title=_("Warning"), indicator="orange")
```

- `frappe.throw` stops execution and rolls back. Prefer specific exceptions
  (`frappe.ValidationError`, `frappe.PermissionError`, `frappe.DoesNotExistError`,
  `frappe.DuplicateEntryError`) when callers may catch them.
- Never `raise Exception("...")`, never `print()`, never bare `except:`.
- Catch only what you expect, then re-throw with a clear message or log:

```python
try:
    response = make_request(...)
except requests.exceptions.RequestException:
    frappe.log_error(title=_("Payment Gateway Error"), message=frappe.get_traceback())
    frappe.throw(_("Could not reach the payment gateway. Please try again."))
```

- User-facing messages must not leak SQL, file paths, stack traces, or secrets.
- Logging: `frappe.logger("my_app").info(...)` for diagnostics; `frappe.log_error(...)` for Error Log.
  Redact personal data.

## 4. Whitelisted methods

```python
# On our own DocType controller — called from JS with frm.call("get_outstanding")
class LoanApplication(Document):
    @frappe.whitelist()
    def get_outstanding(self):
        self.check_permission("read")
        return frappe.db.get_value("Loan", self.loan, "outstanding_amount")
```

```python
# Module-level API — called with frappe.call({ method: "my_app.api.get_rates", args })
@frappe.whitelist(methods=["POST"])
def get_rates(item_code: str, price_list: str):
    frappe.has_permission("Item Price", "read", throw=True)
    return frappe.get_all(
        "Item Price",
        filters={"item_code": item_code, "price_list": price_list},
        fields=["price_list_rate", "currency"],
    )
```

- Every whitelisted function is a public endpoint. Check permissions explicitly; authentication is
  not authorization.
- Use type hints on arguments; Frappe validates them on recent versions.
- Use `methods=["POST"]` for anything that writes. v16 also requires POST for several core
  state-changing endpoints.
- `allow_guest=True` only with an explicit reason, strict validation, and rate limiting.
- Return the minimum data needed; do not return a full doc for three fields.
- Do not accept doctype/field/method names from the client and execute them. Allowlist.
- Prefer a controller method when the operation is about the current document (`frm.call`); use a
  module-level API for cross-document operations.

## 5. Database access

```python
doc = frappe.get_doc("Customer", name)                      # full doc, needed to modify/save
doc = frappe.new_doc("ToDo"); doc.update({...}); doc.insert()
value = frappe.db.get_value("Customer", name, "customer_group")
row = frappe.db.get_value("Customer", name, ["customer_group", "territory"], as_dict=True)
setting = frappe.db.get_single_value("Selling Settings", "cust_master_name")
cached = frappe.get_cached_value("Company", company, "default_currency")
exists = frappe.db.exists("Customer", {"tax_id": tax_id})
frappe.db.set_value("Task", name, "status", "Completed")   # skips validate — use deliberately
```

- `doc.insert(ignore_permissions=True)` only for system-created records, with a comment why.
- `frappe.db.set_value` bypasses controller logic; use `doc.save()` when validations must run.
- `frappe.get_cached_value` / `get_cached_doc` for rarely-changing masters. Invalidate caches when the
  source changes; do not cache per-request data globally.
- **v16: `db.get_value` casts Single DocType values.** Code comparing to `"1"` must compare to `1`.
- **v16: `get_doc(doctype, name, field=value)` no longer mutates the fetched document.** Read the field
  explicitly if that behavior was relied on.
- **v16: implicit default order changed from `modified desc` to `creation desc`** for `get_all`,
  `get_list`, `db.get_value(s)`, and `qb.get_query`. Add explicit `order_by` when order matters.

Query Builder for joins/aggregates:

```python
from frappe.query_builder.functions import Sum

SI = frappe.qb.DocType("Sales Invoice")
rows = (
    frappe.qb.from_(SI)
    .select(SI.customer, Sum(SI.grand_total).as_("total"))
    .where((SI.docstatus == 1) & (SI.posting_date[from_date:to_date]))
    .groupby(SI.customer)
).run(as_dict=True)
```

- Raw SQL only if QB cannot express it, always with `%(name)s` parameters — never f-strings.
- Never interpolate a user-supplied `order_by`, field, or table name. Allowlist it.
- `fields=["*"]` is acceptable in a one-off script or diagnostic; avoid it in request paths and
  reports where it causes over-fetching and breaks silently when schema changes.

## 6. Bulk writes and long-running work

- Prefer `frappe.db.set_value(doctype, filters, field, value)` for bulk field updates when controller
  validation is not required; otherwise iterate with `doc.save()`.
- For large imports, use a standalone script/job with batches, progress logging, and idempotency —
  see `data-migration.md`.
- Long work belongs in `frappe.enqueue`, not a web request. Jobs must log failures and be safe to
  retry.
- Do not spawn unbounded threads from a request. Use the queue.

## 7. Naming

- Prefer `autoname` in DocType settings (naming series, `field:`, `format:`).
- Use `autoname(self)` in the controller only for logic the settings cannot express.
- Keep legacy identifiers in a dedicated field for migrations and integrations; do not encode them
  into the document name unless the client requires it.

## 8. v15/v16 server checklist

- [ ] `get_all`/`get_list` field expressions use dict/pypika form (v16 strict parsing).
- [ ] Explicit `order_by` where order matters.
- [ ] Single DocType comparisons account for v16 type casting.
- [ ] No `frappe.db.commit()` in controllers or document hooks.
- [ ] `override_doctype_class` subclasses the original (mandatory in v16).
- [ ] `has_permission` hooks return explicit `True`.
- [ ] `sendmail(now=True)` flows commit explicitly where required (v16 no longer commits).
- [ ] Whitelisted writes use POST; permissions checked; inputs validated.
- [ ] No SQL interpolation; dynamic sort/field names allowlisted.
