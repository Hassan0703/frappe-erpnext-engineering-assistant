# Version Compatibility — Frappe/ERPNext v15 and v16

This repository supports **Frappe Framework v15 and v16**, with the matching ERPNext major. It does
not support v14 or earlier, and does not claim v17 support.

## Confidence labels

Every version-sensitive statement carries one of these:

| Label | Meaning |
|---|---|
| **Verified (source)** | Confirmed in the cited upstream documentation or release/migration notes |
| **Verified (code)** | Confirmed by reading the installed source on the target bench |
| **Unverified** | Plausible or reported, but not confirmed here — treat as a question, not a fact |

Do not silently upgrade an **Unverified** statement into guidance. Confirm it on the target bench
first, then record the evidence.

These are the labels used inside this reference. The project-wide scale used by the README and the
audit documents maps onto them as follows:

| Project-wide label | Equivalent here | Meaning |
|---|---|---|
| **Runtime-verified** | — (recorded in `docs/audit/phase-2-compatibility-matrix.md`) | a command was executed on the named version and its output observed |
| **Source-verified** | Verified (source) / Verified (code) | the installed source, upstream release notes, or official documentation was read |
| **Documentation-verified** | Verified (source), docs only | official documentation states it; source was not inspected |
| **Unverified** | Unverified | not confirmed; treat as a question |

A label describes one statement, not the whole release. When a claim depends on a patch level, name
the patch level you checked.

## 1. Detect the versions before deciding anything

Run what exists; do not guess flags. `bench <command> --help` is authoritative for the installed
bench.

```bash
bench version                                   # apps + versions; v16 changed default output format
bench --site <site> list-apps                   # what is installed on THIS site
git -C apps/frappe branch --show-current        # version-15 / version-16 / develop
git -C apps/erpnext branch --show-current
grep -n "__version__" apps/frappe/frappe/__init__.py
grep -n "__version__" apps/erpnext/erpnext/__init__.py
```

Record:

```text
Frappe:  <major.minor.patch>  (branch: <branch>)
ERPNext: <major.minor.patch>  (branch: <branch>)
Add-ons: <app, branch, version> …
Site:    <site>   Installed apps: <…>
Evidence: <command output / file path>
```

**If the version is unknown:** stop version-sensitive work, tell the user what you need
(`bench version` output or the app branch), and mark any provisional recommendation **Unverified**.
Do not default to "latest" or to an assumed major version.

## 2. Pair versions correctly

- Frappe and ERPNext must share a major version: v15 with v15, v16 with v16. Do not mix.
- Add-on apps (HRMS, Lending, CRM, Payments, …) must run a branch compatible with the Frappe major.
  Check the app's branch and its declared requirements before adding or upgrading.
- A v15 app installed on a v16 bench is a migration, not a version bump. Treat it as an upgrade
  project with a backup, a staging rehearsal, and a rollback plan.
- Patch-level differences matter: if a behavior is fixed in `15.42.x` but the site runs `15.30.x`,
  the fix is not present. Confirm the patch level, not just the major.

## 3. Difference matrix

Rows are grouped by the decision they affect. "Action" is what the implementing engineer must do.

### 3.1 Runtime, tooling, and deployment

| Area | v15 | v16 | Action | Confidence |
|---|---|---|---|---|
| Python / Node requirements | v15-era versions | **Python 3.14+, Node 24+** | Re-check server images and CI before upgrade; pin in runbook | Verified (source) — v16 migration wiki |
| `bench version` output | `legacy` default | **`plain` default** (name, version, branch, commit) | Any script parsing this output must handle the new format or pass the legacy format flag | Verified (source) — v16 migration wiki |
| Desk route | `/app` | **`/desk`**; `/apps` deprecated | Update bookmarks, redirects, API tests, screenshots, docs | Verified (source) — v16 migration wiki |
| PDF rendering | wkhtmltopdf | **Chromium** for editor formats; `bench setup-chrome` or `chromium_path` | Provision Chromium in every container that prints; no-internet servers must pre-install | Verified (source) — PDF generation docs |
| Classic print formats | Supported | **Deprecated**; new ones cannot be created; converted formats render with Chromium | Convert before v17; re-test CSS selectors | Verified (source) — v16 migration wiki |
| Removed modules | Present | Blog, Newsletter, Energy Points, Backup Integrations moved out/removed | Check for imports and site data before upgrade | Verified (source) — v16 migration wiki |
| Standard workspace edits | Persist | **Overwritten on migrate** | Back up workspace customizations; re-apply as standard/private workspaces | Verified (source) — v16 migration wiki |
| Site/common config caching | — | Cached up to ~1 minute | Do not assume `set-config` takes effect instantly in running workers | Verified (source) — v16 migration wiki |

### 3.2 Data access and query APIs

| Area | v15 | v16 | Action | Confidence |
|---|---|---|---|---|
| `frappe.get_all` / `get_list` `fields` | Raw SQL strings like `"sum(qty) as total"` tolerated | **Strict parsing**; such strings break | Use dict syntax (`{"SUM": "qty", "as": "total"}`) or pypika functions | Verified (source) — query builder migration wiki |
| `distinct` fields | `fields=["distinct batch_no"]` tolerated | Rejected | Pass `distinct=True` | Verified (source) — same |
| Literal fields | `"'X' as doctype"` tolerated | Needs `ValueWrapper` | Use `pypika.terms.ValueWrapper` | Verified (source) — same |
| Function filters | `"ifnull(field, 0)"` as a filter key | Needs `IfNull(Field(...))` | Use pypika function criteria | Verified (source) — same |
| Default ordering | Implicit `modified desc` | **Implicit `creation desc`** for `get_all`, `get_list`, `db.get_value(s)`, and `qb.get_query(..., order_by=DefaultOrderBy)`; a plain `qb.get_query` has no implicit order | Audit logic that relies on implicit order; add explicit `order_by` | Verified (source + code) — v16 migration wiki; runtime 16.52 |
| Empty `!= None` filter | Incorrect SQL | Fixed | Re-test filters that compare to `None` | Verified (source) — v16 migration wiki |
| `run=False` on query objects | Returned SQL string | Returns a QueryBuilder object | Use `.get_sql()` when a string is required | Verified (source) — query builder migration wiki |
| JSON query helpers | — | `JSONExtract`, `JSONValue`, `JSONContains` available | Use for JSON fields instead of ad-hoc SQL | Verified (source) — query builder docs |
| `db.get_value` on Single DocTypes | Returns strings | **Casts values** (`"1"` → `1`) | Fix comparisons that assume strings | Verified (source) — v16 migration wiki |
| `get_doc(doctype, name, field=value)` | Updated doc fields implicitly | **No longer updates** | Read the field explicitly if that was relied on | Verified (source) — v16 migration wiki |
| `db.value_cache` structure | Flat dict | Nested `defaultdict` | Only if you touch internals; prefer public APIs | Verified (source) — v16 migration wiki |
| `db.count(..., cache=True)` | Redis-backed | `value_cache`, evicted after transaction | Re-check cache-lifetime assumptions | Verified (source) — v16 migration wiki |
| `frappe.get_all` field `"*"` | Allowed | Allowed, but still discouraged in request paths | Keep explicit fields | Verified (source) — query builder docs |

> The existing `frappe.qb` range syntax (`field[start:end]`) is documented by Frappe and remains the
> idiomatic BETWEEN form. Do not replace it with string concatenation. If in doubt on a specific
> patch release, verify with `.get_sql()` before running.

### 3.3 Documents, controllers, and hooks

| Area | v15 | v16 | Action | Confidence |
|---|---|---|---|---|
| `frappe.db.commit()` in document hooks | Discouraged but possible | **Not supported: transaction control is disabled inside document hooks**, so the commit is a no-op with a warning | Remove commits from `validate`/`on_submit`/`doc_events`; rely on the request/job transaction | Verified (source + code) — v16 migration wiki; `frappe/model/document.py` 16.52 |
| `override_doctype_class` | Replaces class | **Must subclass** the overridden class | Ensure `class Custom(Original)` and call `super()` | Verified (source) — v16 migration wiki |
| `extend_doctype_class` | **Not available** | Available in v16 and later | v16: prefer mixins over replacing the class; v15: use `override_doctype_class` | Verified (source) — hooks docs |
| `has_permission` hook return | `None` tolerated as allow | **Must return explicit `True`** | Return real booleans; never rely on `None` | Verified (source) — v16 migration wiki; hooks page is ambiguous, treat `None` as unsafe |
| `frappe.permission.has_permission` | Accepts `raise_exception` | Uses `print_logs` instead | Replace the removed argument | Verified (source) — v16 migration wiki |
| `sendmail(..., now=True)` | Implicitly committed | **Does not commit** | Commit explicitly where the workflow requires it | Verified (source) — v16 migration wiki |
| `get_valid_columns()` | Includes virtual fields | Excludes virtual fields | Re-check dynamic field code | Verified (source) — v16 migration wiki |
| Time field default | Current time when empty | Only when `"Now"` is in options | Audit code relying on implicit time | Verified (source) — v16 migration wiki |
| `never_skip_patches` | Not present | Present in v16 (`frappe/modules/patch_handler.py`) | Confirm on the installed branch before relying on it | Verified (code) — Frappe 16.52.0; absent from the `version-15` branch |

### 3.4 Permissions, security, and metadata

| Area | v15 | v16 | Action | Confidence |
|---|---|---|---|---|
| `sanitize_html` implementation | bleach | **nh3** (forbidden tags stripped, not escaped) | Do not rely on bleach behavior; declare bleach yourself if needed | Verified (source) — v16 migration wiki |
| System Console access | Broader | Administrator by default | Grant roles deliberately; update runbooks | Verified (source) — v16 migration wiki |
| Country codes | Loose | ISO 3166 ALPHA-2 validation | Clean country data before migration | Verified (source) — v16 migration wiki |
| `site_cache` arguments | Unhashable allowed | Must be hashable | Remove dict arguments or serialize | Verified (source) — v16 migration wiki |
| `frappe.flags.in_test` | Supported | Deprecated → `frappe.in_test` | Update tests and fixtures | Verified (source) — v16 migration wiki |
| GeoIP | Built in | Removed | Remove dependency on GeoIP-based defaults | Verified (source) — v16 migration wiki |

### 3.5 UI, reports, and translations

| Area | v15 | v16 | Action | Confidence |
|---|---|---|---|---|
| Report / Dashboard Chart / Page JS | Inline global script | **Evaluated as an IIFE** | Do not create implicit globals; attach intentionally to `window` if unavoidable | Verified (source) — v16 migration wiki |
| List view default sort | `modified` | `creation` | Check saved filters/reports that assume order | Verified (source) — v16 migration wiki |
| Saved filters / quick filters | Limited | User-level quick filters, top-of-list saved filters | Update training material and screenshots | Verified (source) — v16 migration wiki |
| Workspaces | Public/private | Persistent sidebar (`Workspace Sidebar`) + desktop screen | Create curated sidebars; verify `add_to_apps_screen` for app tiles | Verified (source) — v16 migration wiki; apps page docs |
| View-specific translations | `get_translated_dict` | **Deprecated** — shim in `frappe/deprecation_dumpster.py`, removal slated for v17 | Move strings to app translation files; do not call it in new code | Source-verified (v16.16.0 deprecation shim) |
| Translation file format | CSV | **Gettext PO/MO** | Convert with the documented bench gettext commands; verify build | Verified (source) — bench commands docs |
| Currency/timezone translation | Various | No longer translated; country names translated everywhere | Check locale-sensitive labels | Verified (source) — v16 migration wiki |
| List/map view rendering | Renders all/map entries | Paginated like list view | No code change, but verify custom map views | Verified (source) — v16 migration wiki |

### 3.6 Tests

| Area | v15 | v16 | Action | Confidence |
|---|---|---|---|---|
| Base test classes | `frappe.tests.utils.FrappeTestCase` | **`frappe.tests.IntegrationTestCase` / `UnitTestCase`** | Import from `frappe.tests`; use Integration for DB, Unit for pure logic | Verified (source) — v16 migration wiki |
| Test dependency attributes | `test_dependencies`, `test_ignore` | `EXTRA_TEST_RECORD_DEPENDENCIES`, `IGNORE_TEST_RECORD_DEPENDENCIES` | Rename when touching the file | Verified (source) — v16 migration wiki |
| Test mode flag | `frappe.flags.in_test` | `frappe.in_test` (`toggle_test_mode` to change) | Update | Verified (source) — v16 migration wiki |
| `setUpClass` override | Not enforced | Must call `super().setUpClass()` | Add the call | Verified (source) — v16 migration wiki |

## 4. Supporting both versions in one codebase

Only do this when the client genuinely runs both. Otherwise target the detected version.

1. **Branch on capability, not on a hardcoded version string**, where the framework exposes one.
   For class extension, `extend_doctype_class` (v16) vs `override_doctype_class` (v15 and v16) is a
   hook-level choice, not a runtime branch.
2. **Keep version-specific code in one module** (e.g. `compat.py`) with a short comment naming the
   versions and the reason. Do not scatter `if version >= 16` through business logic.
3. **Use explicit query ordering** rather than depending on the default-sort change.
4. **Use dict/pypika field expressions** in `get_all`/`get_list` so the same code works on both.
5. **Test on both versions** if both are in scope. One passing version does not prove the other.
6. **Do not backport v16-only hooks to v15** by editing framework source.

## 5. Upgrade safety rules

- A major-version upgrade (v15 → v16) is a project, not a command. Plan staging, backups, a
  maintenance window, and a rollback path.
- Migrations and patches are generally **forward-only**. Rollback usually means restoring the
  pre-upgrade database and files, not running a reverse patch.
- Standard workspace modifications are lost on v16 migrate. Back them up first.
- Never present a backup as valid until a restore has been performed and recorded.
- Never upgrade production without a verified backup and a tested staging rehearsal.
- After upgrade, verify: app versions, scheduler and workers, login, a representative transaction,
  reports, print/PDF, email, permissions, and branding (see `white-labeling.md`).

## 6. Sources and verification date

Checked 2026-10-19:

- Frappe v16 migration guide: `github.com/frappe/frappe/wiki/Migrating-to-version-16`
- Query Builder refactor: `github.com/frappe/frappe/wiki/query-builder-migration`
- Hooks (including `extend_doctype_class`, available in v16 and later): `docs.frappe.io/framework/user/en/python-api/hooks`
- Query Builder: `docs.frappe.io/framework/user/en/api/query-builder`
- PDF generation (v16 and later): `docs.frappe.io/framework/user/en/printing/pdf-generation`
- Bench commands and translation formats: `docs.frappe.io/framework/user/en/bench/frappe-commands`
- Apps page / `add_to_apps_screen` (v15 and later): `docs.frappe.io/framework/user/en/apps-page`

Patch-level behavior is not covered here. When a decision depends on a specific patch release, read
the installed source (`apps/frappe/...`) and record what you found.

### Local verification record

Checked on 2026-10-19 against a development bench running Frappe **16.52.0** / ERPNext
**16.51.1** (both `version-16`), plus the upstream `version-15` branch:

- `bench version` printed the plain format (`app version branch (commit)`).
- `frappe.get_all("DocType", fields=["count(name) as n"])` raised
  `ValidationError: SQL functions are not allowed as strings in SELECT`.
- `fields=[{"SUM": "grand_total", "as": "total"}]` executed.
- `fields=["distinct name"]` raised `PermissionError: Invalid field format for SELECT`.
- `DatabaseQuery("DocType").execute(fields=["name"], run=False)` produced
  `... ORDER BY \`creation\` DESC`.
- `bench setup-chrome` and `bench --site <site> data-import` exist.
- `extend_doctype_class`, `never_skip_patches`, and `frappe.tests.IntegrationTestCase` exist in
  v16 and are absent from the `version-15` branch files inspected.
- `frappe.db.get_single_value` calls `cast_fieldtype`; `sendmail(now=True)` adds the message to
  `after_commit` rather than committing.

Not verified at runtime: scheduler and workers (Redis was not running), email delivery, and PDF
rendering. Those remain source-verified or unverified as labelled above.
