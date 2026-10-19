# Reports and Printing

## 1. Choosing the report type

| Type | Use when | Note |
|---|---|---|
| Standard report (shipped with ERPNext) | It already answers the question | Prefer filters over a new report |
| Report Builder (no code) | Simple filtered list of one DocType | Prefer when sufficient |
| Query Report | A single SQL query with no logic | Runs raw SQL; review carefully |
| Script Report | Logic, joins, computed columns, multiple sources | Default choice for custom reports |

Custom reports belong in the app as standard reports (`Is Standard = Yes`, module set) so they are
versioned and deployable. A report built by hand in the UI is not reproducible.

## 2. Script report structure

```
<module>/report/<report_snake>/
├── <report_snake>.json
├── <report_snake>.py
└── <report_snake>.js
```

```python
import frappe
from frappe import _


def execute(filters=None):
    filters = frappe._dict(filters or {})
    validate_filters(filters)
    return get_columns(), get_data(filters)


def validate_filters(filters):
    if filters.from_date and filters.to_date and filters.from_date > filters.to_date:
        frappe.throw(_("From Date cannot be after To Date"))


def get_columns():
    return [
        {"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link",
         "options": "Customer", "width": 180},
        {"label": _("Total"), "fieldname": "total", "fieldtype": "Currency", "width": 120},
    ]


def get_data(filters):
    SI = frappe.qb.DocType("Sales Invoice")
    query = (
        frappe.qb.from_(SI)
        .select(SI.customer, SI.grand_total)
        .where(SI.docstatus == 1)
    )
    if filters.from_date and filters.to_date:
        query = query.where(SI.posting_date[filters.from_date:filters.to_date])
    if filters.company:
        query = query.where(SI.company == filters.company)
    return query.run(as_dict=True)
```

- Columns as dicts with proper `fieldtype` (Currency, Link, Date, Int, Float) — string column specs
  like `"Customer:Link/Customer:180"` still work but are harder to read and extend; prefer dicts in
  new code.
- Apply filters **in the query**, not in Python after fetching everything.
- Return values with the right type and precision; format money as Currency, not as a text column.
- Report logic must be a small set of named functions so it can be tested directly.
- **v16 strict parsing:** SQL strings inside `fields` (for example `"sum(qty) as total"`) are no
  longer accepted in `get_all`/`get_list`. Use dict syntax or pypika functions:

```python
fields = [{"SUM": "grand_total", "as": "total"}]           # v16 dict form
# or
from frappe.query_builder.functions import Sum
fields = [Sum(SI.grand_total).as_("total")]
```

- v16 also changed the implicit default ordering to `creation`; order reports explicitly.

## 3. Filters (JS)

```js
frappe.query_reports["Customer Outstanding"] = {
    filters: [
        { fieldname: "company", label: __("Company"), fieldtype: "Link", options: "Company", reqd: 1 },
        { fieldname: "from_date", label: __("From Date"), fieldtype: "Date",
          default: frappe.datetime.add_months(frappe.datetime.get_today(), -1) },
        { fieldname: "to_date", label: __("To Date"), fieldtype: "Date", default: frappe.datetime.get_today() },
    ],
};
```

- Mark filters `reqd` when the report is meaningless without them; provide sensible defaults.
- Validate from/to ranges in Python as well.
- Report JS is evaluated as an IIFE in v16 — do not create implicit globals.

## 4. Permissions and data exposure

- Reports are a common data-leak path.

```python
# Respects user permissions and row scoping:
rows = frappe.get_list("Sales Invoice", filters=..., fields=[...])

# Ignores permissions — only for system/aggregate contexts you control:
rows = frappe.get_all(...)
```

- Scope by the user's allowed companies (or use `get_list`, which applies
  `permission_query_conditions`).
- Never accept a company/field/list from the client without validating it against the user's
  permissions.
- Query Reports execute raw SQL with database privileges; a report that accepts user input into SQL
  is an injection vector. Prefer script reports with parameterized queries.
- Hiding columns client-side is not access control.

## 5. Print formats

- Store print formats in the app as standard formats (`Is Standard = Yes`, module set) so they are
  versioned and reproducible.
- Use the Print Format Editor (the current layout tool) for new formats where possible; Jinja HTML
  formats when you need code.
- Jinja: use `doc.get_formatted("field")` for currency/date, `_()` for labels, and avoid
  `frappe.db.get_value` inside loops.
- Jinja runs server-side with elevated data access in some paths; do not print data the requesting
  user is not allowed to see. Test a print as a restricted user.
- Shared Jinja helpers: `jinja = {"methods": ["my_app.utils.jinja.helper"]}` in `hooks.py`.
- Letterhead (logo, address, footer) belongs in the Letter Head DocType and must be assigned to the
  right company. See `white-labeling.md` for branding across print/PDF.

### 5.1 v16 print and PDF changes

Version-specific and easy to miss:

- Classic print formats are **deprecated** in v16: existing ones still print, new ones cannot be
  created, and upstream states they stop working in v17. Convert them with the convert action on the
  Print Format form (the original layout is kept as a backup) and re-test. Standard formats shipped in
  the app must be converted in developer mode and saved so the format's JSON is updated.
- Converted formats render with **Chromium**, not wkhtmltopdf. Servers without internet need
  `bench setup-chrome`, or set `chromium_path` in `common_site_config.json` to an installed
  Chromium. The first render on a cold server downloads Chromium and is slow.
- Converted formats use different CSS hooks. Classic selectors (`.print-format`, `.section-break`,
  `.data-field`) need rewriting for the new layout (`.print-format-doc`, `.section`,
  `.field .label`, `.field .value`).
- `create_custom_format(..., beta=False)` now throws; create formats in the editor instead.
- HTML (Jinja) print formats are not affected by the classic deprecation, but still render through
  the configured PDF engine.
- Bulk printing belongs in a background job; Chromium rendering is heavier than wkhtmltopdf.

Confirm the engine actually used for a given format: the format's own PDF renderer setting takes
precedence, then the format's PDF Generator, then Print Settings.

## 6. Testing reports and print formats

- Run the report with real filters and a large dataset; check timing.
- Test the empty result, the boundary dates, and a restricted user.
- Open the print format with a real document; generate a PDF; check totals, currency, dates, page
  breaks, logo, and letterhead.
- Test with a company that has no letterhead assigned.
- Confirm the PDF is generated on the same server configuration as production (Chromium, fonts).

## 7. Checklist

- [ ] Report/permission scope respects the user's companies and roles.
- [ ] Filters validated server-side; no SQL interpolation from user input.
- [ ] Field expressions compatible with the detected version (v16 strict parsing).
- [ ] Explicit ordering where the report's meaning depends on it.
- [ ] Performance measured at realistic volume; indexes in place.
- [ ] Print format stored in the app; letterhead assigned per company.
- [ ] v16: classic formats converted; CSS selectors updated; Chromium available on the server.
- [ ] PDF rendered and visually inspected; restricted-user test done.
- [ ] Bulk printing enqueued, not run in a request.
