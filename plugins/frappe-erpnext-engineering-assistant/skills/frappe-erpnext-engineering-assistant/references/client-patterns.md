# Client-side Patterns (JS)

Client code is for UX: filters, visibility, defaults, buttons, and display values. Business rules
that must always hold belong on the server. A user can bypass every line of JavaScript.

Version note: v16 reroutes Desk from `/app` to `/desk`, deprecates `/apps`, and evaluates report,
dashboard-chart, and page JS as IIFEs. See `version-compatibility.md`.

## 1. Form script skeleton (our own DocType: `<name>.js`)

```js
frappe.ui.form.on("Loan Application", {
    setup(frm) {
        // runs once per form load; set_query belongs here
        frm.set_query("loan_type", () => ({
            filters: { company: frm.doc.company, disabled: 0 },
        }));
        frm.set_query("item_code", "items", () => ({
            filters: { is_stock_item: 1 },
        }));
    },

    refresh(frm) {
        if (frm.doc.docstatus === 1 && frm.doc.status !== "Closed") {
            frm.add_custom_button(__("Close"), () => close_application(frm), __("Actions"));
        }
        frm.toggle_display("approval_section", frm.doc.status === "Pending Approval");
    },

    customer(frm) {
        if (!frm.doc.customer) return;
        frm.call("get_outstanding")
            .then((r) => frm.set_value("outstanding", r.message))
            .catch(() => frappe.show_alert({ message: __("Could not load outstanding"), indicator: "red" }));
    },
});

frappe.ui.form.on("Loan Application Item", {
    qty: calculate_row_amount,
    rate: calculate_row_amount,
    items_remove(frm) { calculate_total(frm); },
});

function calculate_row_amount(frm, cdt, cdn) {
    const row = locals[cdt][cdn];
    frappe.model.set_value(cdt, cdn, "amount", flt(row.qty) * flt(row.rate));
    calculate_total(frm);
}

function calculate_total(frm) {
    frm.set_value("total", (frm.doc.items || []).reduce((s, r) => s + flt(r.amount), 0));
}
```

Event choice:

| Event | Use for |
|---|---|
| `setup` | `set_query`, one-time form configuration |
| `onload` | Data needed before display; `frm.doc.__onload` |
| `refresh` | Buttons, indicators, visibility based on current state |
| field event | Reacting to a value change |
| `validate` | Last-minute UX check; never the only enforcement |

## 2. `set_query` rules

- Put `frm.set_query` in `setup` (or `onload`), not in `refresh` or a field event. Re-registering on
  every refresh stacks queries and causes confusing filters.
- Child table: `frm.set_query("fieldname", "child_table_fieldname", fn)`.
- Filters as an object `{ field: value }` or a list `[["field", "in", [...]]]`.
- Custom server query only when filters are not enough:

```js
frm.set_query("supplier", () => ({
    query: "my_app.my_module.queries.supplier_query",
    filters: { company: frm.doc.company },
}));
```

```python
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def supplier_query(doctype, txt, searchfield, start, page_len, filters):
    ...  # frappe.qb / get_list, respect permissions and company scope
```

- Simple fetches (copy a field from a linked doc) → set **Fetch From** on the field, not JS.
- Static visibility/mandatory → **Depends On / Mandatory Depends On / Read Only Depends On** in the
  DocType, not JS.
- The query method must enforce permissions; a filter is not a security boundary.

## 3. Server calls

- Method on the current doc's controller → `frm.call("method_name", { args })`.
- Module-level whitelisted function → `frappe.call({ method: "app.module.file.fn", args, freeze: true })`.
- Use promises or `async/await`; never synchronous `async: false`.
- Handle failure: show a message, keep the form usable, and do not leave a spinner running.
- `freeze: true` only for actions that must block the UI; long actions belong in a background job.
- Don't save via `frappe.call` + `frappe.client.set_value` for the open form — use `frm.set_value`
  then `frm.save()` / `frm.save("Submit")`.
- Debounce calls triggered by typing; do not fire a request per keystroke.

## 4. Messages (JS)

```js
frappe.msgprint(__("Please select a customer first"));
frappe.throw(__("Qty must be positive"));            // stops the current JS flow
frappe.show_alert({ message: __("Saved"), indicator: "green" }, 5);
frappe.confirm(__("Close this application?"), () => close_application(frm));
```

- All strings wrapped in `__()`, placeholders: `__("Row {0}: missing rate", [row.idx])`.
- No `alert()`, no `console.log` left in committed code.
- `frappe.throw` in JS is a UX stop, not a security control; the server must enforce the same rule.

## 5. Dialogs

```js
const d = new frappe.ui.Dialog({
    title: __("Set Due Date"),
    fields: [{ fieldname: "due_date", fieldtype: "Date", label: __("Due Date"), reqd: 1 }],
    primary_action_label: __("Update"),
    primary_action(values) {
        frm.call("set_due_date", values)
            .then(() => { d.hide(); frm.reload_doc(); })
            .catch(() => { /* keep dialog open; message already shown */ });
    },
});
d.show();
```

- Validate in the dialog for UX, and again on the server.
- Do not hide the dialog before the server confirms success.

## 6. List view

```js
frappe.listview_settings["Loan Application"] = {
    add_fields: ["status", "outstanding_amount"],
    get_indicator(doc) {
        if (doc.status === "Overdue") return [__("Overdue"), "red", "status,=,Overdue"];
        return [__(doc.status), "gray", `status,=,${doc.status}`];
    },
};
```

- List-view JS lives in `<name>_list.js` and is registered with `frappe.listview_settings`.
- Do not compute authoritative totals in the list view; use a report for money.
- v16 changes default sort to `creation` and paginates map views; do not assume all rows are loaded.

## 7. Reports, dashboards, and pages (v16)

- Report/dashboard/page JS is evaluated as an **IIFE** in v16. Variables no longer leak into global
  scope by default; do not rely on implicit globals, and attach to `window` only deliberately.
- Keep report filters in `frappe.query_reports["Report Name"].filters`.
- Do not fetch data client-side that the report should compute server-side with permissions.

## 8. Don'ts

- No direct DOM manipulation (`$(...)`, `document.querySelector`) when a `frm.*` API exists.
- Don't duplicate server validation as the only check in JS.
- Don't use `cur_frm`; use the `frm` argument.
- Don't create a second `frappe.ui.form.on` block for the same DocType in the same file.
- Don't hardcode company/site/currency values; read them from the doc or settings.
- Don't hardcode URLs for branding assets; use the configured asset path.
- Don't use client-side permission checks as security.

## 9. Version checklist

- [ ] Links and docs use `/desk` (v16) or the correct route for the detected version.
- [ ] `set_query` is in `setup`/`onload`, including child tables.
- [ ] Every server call handles failure without leaving the form stuck.
- [ ] Report/page JS does not depend on implicit globals (v16 IIFE).
- [ ] No `console.log`, `alert`, or `cur_frm` in committed code.
- [ ] All user-facing strings use `__()` with placeholders.
