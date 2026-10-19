# Phase 2 Technical Findings — `frappe-code-standards`

> **Historical record (Phase 1/2).** This document describes the project under its original
> name, layout, and repository. It was renamed and independently rebranded in Phase 3; see
> `docs/audit/phase-3-release-audit.md`. Preserved as evidence, and exempt from the
> inherited-branding scan (see `NOTICE`). The development site/app name was redacted for
> publication; versions and results are unchanged.


**Review date:** 2026-10-19
**Method:** independent review of the working copy, compared against the recovered upstream
baseline (`099cbe7`) and against installed Frappe/ERPNext source and runtime.
**Environment:** Frappe 16.52.0 / ERPNext 16.51.1 (`version-16`) at `the local bench root`,
site `<dev-app>.local`; upstream `version-15` branch source read over HTTPS. No v15 runtime bench,
no production or client environment.

Severity: **Critical** = wrong or unsafe output likely; **High** = materially misleading guidance;
**Medium** = correctness or maintainability risk; **Low** = precision/consistency.

## 1. Summary

The upgraded product is substantially sound. The placement rules, security model, migration
discipline, evidence gate, and v15/v16 matrix are accurate against the installed v16 source and the
official v16 migration guide. The defects found are documentation-level: one invented hook, one
invented bench command, two approximate version claims, and the absence of any automated test for
the validator that the previous report described as fault-tested.

No Critical finding was identified. No instruction was found that would cause data loss, privilege
escalation, or an unrecoverable deployment when followed as written. The safety posture is stronger
than the baseline: production mutation, destructive data operations, secret handling, and unverified
success claims are explicitly prohibited.

## 2. Findings and corrections

### F2-01 — Invented hooks in the white-labeling guide (High) — **fixed**

`references/white-labeling.md` §3.3 listed `website_catch_all` as the mechanism for error pages. No
such hook exists in Frappe v16.52 or in the `version-15` branch (empty grep for `website_catch_all`
in both). It also listed `homepage` as a landing-page hook; the real mechanisms are Website Settings
`home_page` and the `role_home_page` / `get_website_user_home_page` hooks. The same file and
`hooks-and-customization.md` also described `app_icon` as app metadata "shown in the UI"; Frappe core
16.52 does not read an `app_icon` hook (ERPNext declares it, but core consumes `app_color` only and
uses `app_logo_url` for the visible logo).

This directly violates the repository's own rule against inventing hooks. Corrections:

- error pages now cite the app `www/404.html` override (verified in `TemplatePage.set_template_path`,
  which resolves `www/<path>.html` across installed apps) plus `website_route_rules` /
  `website_redirects`;
- `home_page` (setting) replaces the `homepage` hook;
- `app_icon` is labelled unverified and the guidance points to `app_logo_url` /
  `add_to_apps_screen`;
- `website_route_rules` and `website_redirects` were added to the hooks table.

### F2-02 — Non-existent bench command in the migration guide (Medium) — **fixed**

`references/data-migration.md` §7 listed `bench import-csv`. On the v16.52 bench this command does
not exist (`No such command: 'import-csv'`; suggestions are `export-csv`, `export-doc`,
`import-doc`). `bench --site <site> data-import` does exist and is verified. The table now lists the
Data Import tool, a custom script, and bulk APIs only.

### F2-03 — Stale "Unverified" label on `never_skip_patches` (Low) — **fixed**

`version-compatibility.md` and `hooks-and-customization.md` marked `never_skip_patches` as
"Unverified (version not stated)". Source inspection shows it in
`frappe/modules/patch_handler.py` on v16.52 and absent from the `version-15` branch. The label is now
"Verified (code) — Frappe 16.52.0; absent from the version-15 branch".

### F2-04 — "Commit is blocked" is imprecise (Low) — **fixed**

`SKILL.md`, `version-compatibility.md`, and `performance.md` said `frappe.db.commit()` is "blocked" in
v16 document hooks. The upstream wording is "not supported", but the implementation is subtler:
`frappe/model/document.py` disables transaction control around hook calls, so `commit()` becomes a
no-op that emits a warning rather than raising. An agent waiting for an exception to detect a bad
commit would never see one. The three places now say the commit is disabled / a no-op.

### F2-05 — `qb.get_query` default-order claim was too broad (Low) — **fixed**

The default-sort row attributed implicit `creation desc` ordering to `qb.get_query` unconditionally.
Runtime check:
`frappe.qb.get_query("DocType", fields=["name"]).get_sql()` emits **no** `ORDER BY`, while
`frappe.qb.get_query(..., order_by=DefaultOrderBy)` and the `get_all`/`get_list` path emit
`ORDER BY \`creation\` DESC`. The row now distinguishes the two. The practical advice (order
explicitly where order matters) is unchanged.

### F2-06 — Validator crashed on an invalid marketplace manifest (Medium) — **fixed**

`check_manifests()` re-parsed `marketplace.json`/`plugin.json` with a bare `json.loads` after already
reporting parse errors, so an invalid manifest produced a traceback instead of a clean failure. A
`load_json()` helper now returns `None` and dependent checks are skipped. Covered by
`test_invalid_json_manifest_fails`.

### F2-07 — No automated tests; the claimed fault injection was not reproducible (Medium) — **fixed**

`implementation-roadmap.md` claimed "Fault injection, 13 cases — all behaved as expected", but no
test harness was committed. A reviewer could not reproduce the claim, and the validator itself had
no regression protection. Added `scripts/tests/test_validate_repo.py` (stdlib `unittest`, runs on
throwaway copies): a passing baseline, one failing case per structural check, white-label coverage
cases, metadata cases, secret cases, and consistency checks for CI and the skill description. CI now
runs the suite.

### F2-08 — README overclaimed template evidence fields (Low) — **fixed**

The root README said "Every template asks for evidence". Ten of the 25 templates (for example
`data-mapping.md`, `requirements-and-acceptance.md`) are specification forms that legitimately have
no "evidence" field. The claim now states that templates recording a check carry an evidence field.

### F2-09 — Safe-change classification did not separate all five mechanisms (Low) — **fixed**

The brief requires the guide to distinguish standard settings, supported custom-app mechanisms,
hooks/fixtures, patches/migrations, and framework forks. The table had four rows and merged hooks and
fixtures into the custom-app row. It now has five rows, with the fixture/record difference (fixtures
fail at sync, hooks fail at import) called out.

### F2-10 — Portal branding pointed at a desk-only asset hook (Low) — **fixed**

The navbar/brand-colors row suggested `app_include_css` for "desk + portal". `app_include_css` is
desk-only; website/portal needs `web_include_css` (§3.7 already said so). The row now names both.

## 3. Claims checked and found correct (no change)

Verified against installed source and/or runtime, not just the previous report:

| Claim | Evidence |
|---|---|
| Python 3.14+, Node 24+ for v16 | `pyproject.toml` `requires-python = ">=3.14,<3.15"`; `package.json` `"node": ">=24"`; v16 migration guide |
| `bench version` defaults to plain output | `bench version` printed `frappe 16.52.0 version-16 (4515014)` |
| Desk route `/desk`; `/app` and `/apps` redirected | `frappe/hooks.py` website_redirects |
| `bench setup-chrome` exists | `frappe/commands/utils.py:1095` |
| Chromium PDF, classic-format deprecation | v16 migration guide; `create_custom_format(beta=False)` throws |
| New print CSS hooks `.print-format-doc`, `.field .label` | `frappe/templates/print_format/print_format_doc.css` |
| `extend_doctype_class` is v16-only | present in `base_document.py`; absent from version-15 file |
| `override_doctype_class` must subclass | `issubclass` guard in `base_document.py` |
| `has_permission` hook must return explicit `True` | v16 `has_controller_permissions` denies falsy/`None`; v15 returns `True` on `None` |
| `frappe.permissions.has_permission` dropped `raise_exception` for `print_logs` | signatures in both branches |
| `frappe.has_permission(..., throw=True)` is valid | wrapper in `frappe/__init__.py` accepts `throw` in both branches |
| `get_all`/`get_list` reject SQL-function strings in v16 | runtime `ValidationError: SQL functions are not allowed as strings in SELECT`; dict `{"SUM": ..., "as": ...}` works |
| `fields=["distinct x"]` rejected in v16 | runtime `PermissionError: Invalid field format for SELECT` |
| Default order is `creation desc` in v16, `modified desc` in v15 | runtime SQL; version-15 `db_query.py` |
| Single DocType values are cast in v16 | `get_single_value` → `cast_fieldtype` |
| `sendmail(now=True)` no longer commits | v16 `frappe/email/__init__.py` adds to `after_commit` |
| `has_permission`/`get_website_user_home_page`/`role_home_page` hooks exist | source usage |
| `default_mail_footer`, `get_sender_details`, `override_email_send` exist | source usage |
| `add_to_apps_screen` exists in v15 and v16 | both `apps.py` files |
| `app_logo_url`, `brand_html`, `website_context` exist | source usage |
| `user_data_fields`, `before_tests`, file-I/O hooks exist | source usage |
| `bench data-import`, `show-config`, `set-config`, `doctor`, `show-pending-jobs`, `ready-for-migration`, `purge-jobs`, `clear-website-cache`, `enable-scheduler`, `run-parallel-tests`, `backup --with-files` | `bench --help` on 16.52 |
| `run-tests --module` / `--doctype` | `bench run-tests --help` |
| v15 tests use `frappe.tests.utils.FrappeTestCase`; v16 uses `frappe.tests.IntegrationTestCase`/`UnitTestCase` | version-15 `tests/utils.py`; v16 `tests/classes/` |
| `never_skip_patches` is v16-only | `patch_handler.py` both branches |
| Migration/runbook/secret/safety guidance | reviewed; no unsafe instruction found |

## 4. Engineering, security, and delivery review

### 4.1 Frappe/ERPNext engineering

Placement guidance is correct for both versions: own-DocType logic in the DocType files, other apps
extended via `doc_events` / `doctype_js` / overrides / `extend_doctype_class` / fixtures, no vendor
edits. Lifecycle hook guidance (validate/on_update/on_submit/on_cancel, `db_set` semantics) is
accurate. Transactions are handled correctly (`savepoint`, `for_update`, no commit in handlers,
`enqueue_after_commit`). Query guidance matches the v16 query-builder rewrite, and the runtime checks
above confirm the failure modes described. Report/print guidance matches the v16 Chromium/Print
Format Editor changes. Fixtures and the Single-DocType caveat are correctly hedged. No API, hook, or
command in the references was found to be non-existent after the fixes above, except where explicitly
labelled unverified.

### 4.2 White-labeling

After F2-01, F2-09, and F2-10 the guide covers desk, login, navbar/workspace, website/portal, app
metadata, logo/favicon/assets, email/notifications, print/PDF, translations, PWA (hedged), tenancy,
upgrade/asset rebuild, and the licensing/trademark boundary. For each surface it names a mechanism, a
location, a v15/v16 difference where relevant, and a verification step, and it requires the exact
`fieldname` to be confirmed in the installed DocType JSON rather than asserted. That is the correct
posture; the remaining uncertainty (exact fieldnames per patch level) is stated in the guide and the
README.

### 4.3 Deployment, migration, security, support

Deployment guidance is safe: backups before schema changes, restore drills as the only proof, rollback
as a decision with a stated data-loss window, scheduler/worker/queue checks, and v16-specific runtime
and PDF requirements. Migration guidance correctly rejects "no import errors" as success and requires
reconciliation of counts, relationships, financials, and stock. Security guidance is layered and
concrete (authorization vs authentication, permlevel, SQL parameterization, uploads, secrets,
tenancy, privacy, AI tool boundaries). Support guidance puts data integrity and evidence before
cosmetic fixes. No instruction permits production mutation, destructive operations, or unverified
sign-off.

## 5. Residual uncertainty

- Exact branding fieldnames and their v15/v16 stability are still not enumerated; the guide correctly
  delegates to the installed DocType JSON. Not a defect, but not fully resolvable from here.
- Single-DocType fixture round-tripping remains unverified; the guide offers the patch/`after_install`
  alternative.
- PWA support per patch level remains unverified.
- v15 runtime behaviour was verified from source, not executed.
- Scheduler, workers, email, and PDF were not exercised (Redis not running; no mail/Chromium setup).
