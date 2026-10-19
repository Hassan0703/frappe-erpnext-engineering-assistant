# hooks.py, Customization, Fixtures, Patches

`hooks.py` is a registry of dotted paths and declarations — not a code file. No logic, no
side effects at import time.

Hook availability varies by version. Items marked **v16** do not exist in v15. When adding a hook,
confirm it on the installed version (`version-compatibility.md`).

## 1. Common hooks

```python
doctype_js = {"Sales Invoice": "public/js/sales_invoice.js"}          # other apps' DocTypes only
doctype_list_js = {"Sales Invoice": "public/js/sales_invoice_list.js"}

doc_events = {
    "Sales Invoice": {
        "validate": "my_app.selling.overrides.sales_invoice.validate",
        "on_submit": "my_app.selling.overrides.sales_invoice.on_submit",
    },
}

scheduler_events = {
    "daily": ["my_app.tasks.daily.send_overdue_reminders"],
    "daily_long": ["my_app.tasks.daily.rebuild_statistics"],
    "cron": {"0 2 * * *": ["my_app.tasks.nightly.sync_rates"]},
}

fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "My Module"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "My Module"]]},
]

required_apps = ["erpnext"]
```

Rules:

- No logic in `hooks.py` — only dotted paths.
- Avoid `doc_events` for the core business logic of a DocType we own; use its controller. A
  cross-cutting concern (audit trail) may legitimately register `doc_events` for our own DocType.
- Never use `"*"` doc_events unless the logic truly applies to every DocType; it runs on every save
  and is a performance and blast-radius risk.
- After changing `scheduler_events`, run `bench --site <site> migrate` — scheduled events are
  registered on migrate.
- `required_apps` ensures dependencies are installed with the app; declare add-ons you actually need.

## 2. Overriding and extending another app's controller

```python
# v15 and v16 — replaces the class. In v16 you MUST subclass the original.
override_doctype_class = {
    "ToDo": "my_app.overrides.todo.CustomToDo",
}
```

```python
# my_app/overrides/todo.py
from frappe.desk.doctype.todo.todo import ToDo


class CustomToDo(ToDo):
    def on_update(self):
        self.my_custom_code()
        super().on_update()
```

```python
# v16 — add behavior without replacing the class; multiple apps can extend safely.
extend_doctype_class = {
    "Address": ["my_app.extensions.address.AddressMixin"],
}
```

```python
# my_app/extensions/address.py
from frappe.model.document import Document


class AddressMixin(Document):
    @property
    def full_address(self):
        return f"{self.address_line1}, {self.city}"
```

- Prefer `extend_doctype_class` (v16) or `doc_events` over replacing a class: replacement means
  "last app wins" and silently disables other apps' overrides.
- If both hooks exist, extensions are applied on top of the overridden class.
- Never monkey patch at import time.

## 3. Override functions

```python
# my_app/selling/overrides/sales_invoice.py
import frappe
from frappe import _


def validate(doc, method=None):
    validate_discount_limit(doc)


def validate_discount_limit(doc):
    limit = frappe.db.get_single_value("My App Settings", "max_discount")
    if doc.additional_discount_percentage > limit:
        frappe.throw(_("Discount cannot exceed {0}%").format(limit))
```

- Signature is `(doc, method=None)`. Never use `*args` to swallow the method name.
- Keep the function thin; put logic in named helpers and test them directly.
- One file per DocType under `overrides/` (or `extensions/` for mixins).

## 4. Custom Fields

- Preferred: create on site via Customize Form with **Module = our module**, then
  `bench --site <site> export-fixtures --app <app>` (confirm flags with `--help`).
- Alternative: create in code during install/migration with
  `from frappe.custom.doctype.custom_field.custom_field import create_custom_fields`.
- Field names on other apps' DocTypes: prefix with the app short code (e.g. `nx_approval_status`) to
  avoid collisions.
- Do not edit another app's DocType JSON.
- Fixtures work well for DocType records (Custom Field, Property Setter, Workflow, Notification,
  Print Format). **They are not guaranteed to round-trip Single DocTypes.** If a value must exist on
  every site (a setting, Website Settings branding), apply it in `after_install`/a patch with
  `frappe.db.set_single_value(...)` and verify on a fresh site. *(Unverified: fixture behavior for
  Singles.)*

## 5. Patches

```
# patches.txt
[pre_model_sync]
my_app.patches.v1_0.rename_old_field
[post_model_sync]
my_app.patches.v1_0.set_default_status
```

```python
# my_app/patches/v1_0/set_default_status.py
import frappe


def execute():
    frappe.db.set_value("Loan Application", {"status": ("is", "not set")}, "status", "Draft")
```

- One patch per file; **idempotent** (safe to run twice); no `print`.
- Patches that need new fields → `[post_model_sync]`.
- A patch that must never be skipped can be listed in `never_skip_patches` (v16; absent from the
  v15 branch). Confirm it in the installed `frappe/modules/patch_handler.py` before relying on it.
- Patches run on every migration and on every site — they must not depend on a developer's local
  data or an external file that is not shipped.
- Client-specific bulk data loads are usually not patches; use a controlled migration script
  (`data-migration.md`).
- Patches are forward-only. Rollback means restoring a backup, not reverting the patch.

## 6. Settings

- App configuration → a Single DocType (`My App Settings`), read with
  `frappe.db.get_single_value` or `frappe.get_cached_doc`.
- Secrets (API keys, tokens) → a `Password` field on the settings DocType, read server-side with the
  framework's password helper (`frappe.utils.password.get_decrypted_password` — verify on your
  version). Never send secrets to the client or store them in plain text.
- Infra/environment values that differ per deployment (hostnames, provider regions) → site config or
  environment, not a DocType.
- No magic constants in code; no hardcoded company, site, currency, or prefix.

## 7. Permissions

- Roles and DocPerm live in the DocType JSON; extra rules via hooks:

```python
permission_query_conditions = {"ToDo": "my_app.permissions.todo_query"}
has_permission = {"Event": "my_app.permissions.event_has_permission"}
```

- `permission_query_conditions` returns a SQL `WHERE` fragment; escape values with
  `frappe.db.escape`. It affects `frappe.get_list`/`db.get_list`, not `get_all`.
- `has_permission(doc, user=None, permission_type=None)` must return an explicit `True` to allow.
  **v16:** returning `None` is not an approval — always return a real boolean.
- Don't hide fields in JS as a security measure — use `permlevel`.
- Test permission hooks as a restricted user; see `testing-and-qa.md`.

## 8. Branding, website, email, and file hooks

These are the supported extension points for identity and infrastructure work
(details: `white-labeling.md`, `deployment-and-operations.md`):

| Hook | Purpose | Version |
|---|---|---|
| `app_title`, `app_publisher`, `app_description` | App metadata shown in the UI and app listings. Confirm the exact rendering on the target version | both |
| `app_icon`, `app_color` | Legacy ERPNext hooks. ERPNext declares both, but Frappe core 15.94 and 16.16 do not read them for the app tile; use `add_to_apps_screen` (with `logo`) and `app_logo_url` instead | source-verified |
| `app_logo_url` | Desk logo | both |
| `brand_html` | Website/navbar brand HTML (alternative to Website Settings) | both |
| `website_context` / `update_website_context` | Favicon and other website context values | both |
| `add_to_apps_screen` | App tile on the apps/desktop screen (`name`, `logo`, `title`, `route`, `has_permission`) | v15 and later |
| `role_home_page`, `get_website_user_home_page` | Landing page per role; the default home is Website Settings `home_page` | both |
| `base_template`, `base_template_map` | Website base template overrides | both |
| `website_route_rules`, `website_redirects` | Route mapping and redirects (useful for branded URLs and error paths) | both |
| `default_mail_footer` | Global email footer | both |
| `get_sender_details` | Sender name/address for outgoing email | both |
| `override_email_send` | Route email through a provider | both |
| `write_file`, `before_write_file`, `delete_file_data_content` | Object storage/CDN file I/O | both |
| `app_include_js` / `app_include_css` | Desk-wide assets | both |
| `web_include_js` / `web_include_css` | Website-wide assets | both |
| `user_data_fields` | Personal-data DocTypes for download/deletion | both |
| `before_tests` | Seed data for test runs | both |

`add_to_apps_screen` entries with `has_permission` control which users see the tile — use it rather
than hiding tiles in JS.

## 9. Do not do this

- Logic in `hooks.py`.
- Editing another app's files instead of using hooks/fixtures.
- `doc_events` with `"*"` for convenience.
- Fixtures with no module filter (they export records you did not intend to ship).
- Patches that assume a specific site's data.
- Secrets in `hooks.py`, fixtures, or DocType defaults.
- Replacing a vendor asset or template file in place instead of overriding it.
