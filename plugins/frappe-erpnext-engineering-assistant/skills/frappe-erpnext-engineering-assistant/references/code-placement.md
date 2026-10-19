# Code Placement

The rule: put code where a Frappe developer opening the project would look for it first. Working
code in the wrong place is a defect, because the next developer will not find it and the next
upgrade will fight it.

Version note: `extend_doctype_class` is **v16**. `override_doctype_class` exists in both, but in
v16 the overriding class must inherit from the overridden class. See `version-compatibility.md`.

## 1. Find the owning app first

```bash
# Which app defines this DocType?
find apps -path "*/doctype/<doctype_snake>/<doctype_snake>.json"
# Read the JSON: "module" tells you the module folder; the app is the folder above it
```

- **Our app owns it** → edit its own `.py` / `.js` files.
- **Another vendor app owns it** (frappe, erpnext, hrms, …) → extend from our app. Never edit the
  vendor app; upgrades overwrite it.
- **Nobody owns it** (created on site) → decide whether it belongs in the app repository. If it is
  business logic, it does.

## 2. App layout (reference)

```
apps/<app>/<app>/
├── hooks.py
├── patches.txt
├── <module>/                          # one folder per Module Def
│   ├── doctype/<doctype_snake>/
│   │   ├── <doctype_snake>.json       # schema (Desk developer mode, or careful hand edit)
│   │   ├── <doctype_snake>.py         # controller class
│   │   ├── <doctype_snake>.js         # form script
│   │   ├── <doctype_snake>_list.js    # list view script
│   │   └── test_<doctype_snake>.py    # tests
│   ├── report/<report_snake>/         # script / query reports
│   ├── page/                          # custom desk pages
│   ├── extensions/<doctype_snake>.py  # v16 extend_doctype_class mixins
│   └── overrides/<doctype_snake>.py   # doc_events / override_doctype_class targets
├── patches/<version>/                 # one idempotent patch per file
├── public/
│   ├── js/                            # shared utils + overrides of other apps' forms
│   ├── css/                           # scoped overrides
│   └── images/                        # logo, favicon, brand assets
├── templates/
│   ├── emails/                        # email templates
│   └── pages/                         # portal/web template overrides
├── www/                               # web pages / portal routes
├── fixtures/                          # exported Custom Field, Property Setter, etc.
└── config/                            # app-specific config if used
```

`services/` and `utils.py` are acceptable homes for shared business logic when the app grows; create
them deliberately, not as a dumping ground.

## 3. Decision tree

1. **Is the DocType defined in our app?**
   - Yes → form logic in `<name>.js`, server logic in `<name>.py`. No `hooks.py` entry needed.
   - No → continue.
2. **Server logic on another app's DocType** → `doc_events` in `hooks.py` pointing to
   `<app>.<module>.overrides.<doctype_snake>.<function>`. Signature:
   `def validate(doc, method=None):`.
3. **Client logic on another app's DocType** → `public/js/<doctype_snake>.js` and
   `doctype_js = {"Sales Invoice": "public/js/sales_invoice.js"}`.
4. **Need to change a controller method of another app**
   - v16: prefer `extend_doctype_class` to add behavior without replacing the class.
   - Both versions: `override_doctype_class`, subclass the original, call `super()`. In v16 the
     subclass is mandatory.
   - If both hooks exist, extensions apply on top of the overridden class (hooks docs).
5. **Need a field on another app's DocType** → Custom Field / Property Setter exported as a fixture
   filtered by our module. Never edit the other app's JSON.
6. **Need to replace a whitelisted framework endpoint** → `override_whitelisted_methods` with the
   same signature, only when there is no narrower hook. Document why.
7. **Logic used by several DocTypes** → a plain Python module in our app (`<app>/<module>/utils.py`
   or `services/`), called from each controller. JS helpers → `public/js/` + bundle, only if truly
   shared.
8. **Branding assets** → `public/images/` plus the app's settings/hooks. See `white-labeling.md`.

## 4. Child tables

Child DocType events go in the **parent's** JS file, in their own block:

```js
frappe.ui.form.on("Sales Order Custom Item", {
    qty(frm, cdt, cdn) { calculate_row_amount(frm, cdt, cdn); },
    rate(frm, cdt, cdn) { calculate_row_amount(frm, cdt, cdn); },
    items_remove(frm) { calculate_totals(frm); },
});
```

Server-side logic on child rows goes in the **parent controller** (loop over `self.items`), not the
child DocType's controller, unless the child is genuinely independent of its parent.

## 5. Site-level scripts: discouraged, not always forbidden

Client Script and Server Script records live in the database, not the repository. They are:

- invisible to code review and CI,
- not reproducible on a fresh site,
- easy to break on upgrade,
- different per environment.

Default: put logic in the app. If the client's deployment model forbids custom apps or the client
owns that layer, a site script may be the sanctioned mechanism. In that case: keep it minimal,
document it in the configuration inventory, export a backup, and test the upgrade path. Do not
present it as equivalent to versioned code.

## 6. Multiple apps, hooks, and conflicts

- Hook resolution is "last writer wins" for overrides and "in install order" for extensions. This
  means two apps overriding the same DocType class silently fight.
- Prefer `doc_events` and `extend_doctype_class` over replacing a class when another app may also
  extend it.
- Record which app owns each extension in the technical design; avoid duplicate validation in two
  apps.
- Never patch another app's Python at runtime (monkey patching). It is invisible and order-dependent.

## 7. Wrong vs right

- ❌ `hooks.py: doctype_js = {"My Own DocType": "public/js/my_own_doctype.js"}`
  ✅ `my_app/my_module/doctype/my_own_doctype/my_own_doctype.js`
- ❌ Validation only in `frappe.ui.form.on(... validate(frm) {...})`
  ✅ Validation in controller `validate()`; JS may add a UX hint.
- ❌ `doc_events = {"My Own DocType": {...}}` for the DocType's core business logic
  ✅ Controller methods. (`doc_events` is acceptable for a cross-cutting concern registered by
  another module — audit logging, for example — but do not split one DocType's logic across both.)
- ❌ Logic in a site-level Server Script record with no backup or documentation
  ✅ Code in the app repository (versioned, reviewable, deployable) — unless the deployment model
  forces the former, in which case document and back it up.
- ❌ Editing `apps/erpnext/...` files
  ✅ hooks + overrides/extensions + fixtures in our app.
- ❌ Monkey patching a vendor class at import time
  ✅ `override_doctype_class` / `extend_doctype_class`.

## 8. Placement review questions

1. If a new developer searched for this rule, which file would they open first?
2. Does this file belong to the app that owns the DocType?
3. Will an upgrade overwrite it?
4. Is the same behavior implemented twice (JS + Python, or hook + controller)?
5. Is the change reproducible on a fresh site without manual steps?
