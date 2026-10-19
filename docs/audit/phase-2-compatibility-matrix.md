# Phase 2 v15/v16 Compatibility Matrix

> **Historical record (Phase 1/2).** This document describes the project under its original
> name, layout, and repository. It was renamed and independently rebranded in Phase 3; see
> `docs/audit/phase-3-release-audit.md`. Preserved as evidence, and exempt from the
> inherited-branding scan (see `NOTICE`). The development site/app name was redacted for
> publication; versions and results are unchanged.


**Date:** 2026-10-19
**Rule applied:** nothing is marked verified because the documentation describes it. Each row carries
the strongest evidence actually obtained.

## 1. Environments

| Environment | Version | Access | Used for |
|---|---|---|---|
| Development bench `the local bench root` | Frappe 16.52.0, ERPNext 16.51.1, app `<dev-app>` 0.0.1 (all `version-16`) | Local, read-only commands and `bench console`/`execute`; **not mutated** | Runtime verification on v16 |
| Site `<dev-app>.local` | Frappe 16.52.0 | `bench --site` read-only commands | App discovery, query behaviour |
| Upstream source `frappe/frappe` `version-15` | branch head at review time | HTTPS file reads | v15 source comparison |
| Upstream `frappe/frappe` `version-16` (working tree) | 16.52.0 (commit 4515014) | Local read | v16 source verification |

**Not available:** a v15 bench or site; a running Redis/queue/scheduler stack; a configured mail
server; Chromium for PDF. No production or client environment was touched.

## 2. Evidence scale

| Level | Meaning |
|---|---|
| **Documentation-verified** | Stated in official Frappe documentation or the v16 migration guide |
| **Source-verified** | Confirmed by reading the installed/branch source |
| **Automated-test-verified** | Exercised by a committed test that runs in CI |
| **Runtime-verified** | Executed on a real bench/site and the output observed |
| **Not verified** | Neither of the above; stated as a limitation |

A row can hold several levels. "Documentation-verified" alone is not treated as proof of behaviour.

## 3. Matrix

| # | Claim | v15 | v16 | Evidence obtained |
|---|---|---|---|---|
| 1 | Runtime floor | v15 floor | **Python 3.14+, Node 24+** | Documentation-verified (migration guide) + Source-verified (`pyproject.toml`, `package.json`) |
| 2 | `bench version` default output | legacy | **plain** (app, version, branch, commit) | Documentation-verified + Runtime-verified (`bench version`) |
| 3 | Desk route | `/app` | **`/desk`**; `/app`, `/apps` redirected | Documentation-verified + Source-verified (`frappe/hooks.py`) |
| 4 | `frappe.get_all`/`get_list` field strings | raw SQL tolerated | **SQL-function strings rejected**; use dict/pypika | Documentation-verified + Source-verified (`database/query.py`) + Runtime-verified (error observed) |
| 5 | `fields=["distinct x"]` | tolerated | **rejected**; use `distinct=True` | Documentation-verified + Runtime-verified |
| 6 | Dict function syntax `{"SUM": "grand_total", "as": "total"}` | n/a | **works** | Runtime-verified |
| 7 | Default ordering | `modified desc` | **`creation desc`** for `get_all`, `get_list`, `db.get_value(s)`, `qb.get_query(order_by=DefaultOrderBy)`; plain `qb.get_query` unordered | Documentation-verified + Source-verified + Runtime-verified (SQL `ORDER BY \`creation\` DESC`) |
| 8 | `frappe.db.commit()` in document hooks | possible (defect) | **transaction control disabled; commit is a no-op** | Documentation-verified + Source-verified (`model/document.py`) |
| 9 | `override_doctype_class` | replaces class | **must subclass** the overridden class | Documentation-verified + Source-verified (`issubclass` guard) |
| 10 | `extend_doctype_class` | absent | **present** | Source-verified (present in v16 `base_document.py`, absent from version-15) + Runtime-verified (hook registered by ERPNext) |
| 11 | `has_permission` hook return | `None` allows | **must return explicit `True`** | Documentation-verified + Source-verified (v15 returns `True` on `None`; v16 denies) |
| 12 | `frappe.permissions.has_permission` params | `raise_exception` | `print_logs` | Source-verified (both branches) |
| 13 | `frappe.has_permission(..., throw=True)` | supported | supported | Source-verified (wrapper in both branches) |
| 14 | `sendmail(now=True)` commit | commits | **does not commit**; added to `after_commit` | Documentation-verified + Source-verified |
| 15 | Single DocType `db.get_value` | strings | **cast** | Documentation-verified + Source-verified (`cast_fieldtype`) |
| 16 | `get_doc(doctype, name, field=value)` mutation | mutates | **no longer mutates** | Documentation-verified |
| 17 | `sanitize_html` implementation | bleach | **nh3** (strips forbidden tags) | Documentation-verified + Source-verified (`import nh3`) |
| 18 | Translation format | CSV | **Gettext PO/MO** | Documentation-verified + Source-verified (`bench generate-pot-file`, `migrate-csv-to-po`, `compile-po-to-mo`, `update-po-files`) |
| 19 | Test classes | `frappe.tests.utils.FrappeTestCase` | **`frappe.tests.IntegrationTestCase` / `UnitTestCase`** | Documentation-verified + Source-verified (v15 `tests/utils.py`; v16 `tests/classes/`) |
| 20 | `frappe.flags.in_test` | supported | **deprecated → `frappe.in_test`** | Documentation-verified + Source-verified (`in_test = False`) |
| 21 | Print formats | classic + HTML | **classic deprecated**, Print Format Editor, Chromium | Documentation-verified + Source-verified + Runtime-verified (`bench setup-chrome` exists) |
| 22 | Print CSS hooks | classic selectors | `.print-format-doc`, `.field .label`, `.field .value` | Documentation-verified + Source-verified (`print_format_doc.css`) |
| 23 | `create_custom_format(beta=False)` | n/a | **throws** | Documentation-verified + Source-verified |
| 24 | Report/dashboard/page JS | inline global | **IIFE** | Documentation-verified |
| 25 | Workspace edits | persist | **overwritten on migrate** | Documentation-verified |
| 26 | Removed modules (Blog, Newsletter, Energy Points, Backup Integrations) | present | removed | Documentation-verified |
| 27 | Site/common config cache | immediate | **~1 minute** | Documentation-verified |
| 28 | `never_skip_patches` | absent | **present** | Source-verified (v16 `patch_handler.py`; absent from version-15) |
| 29 | `bench data-import` | n/a | **present**; `bench import-csv` absent | Runtime-verified (`--help`, and the command error) |
| 30 | Operations commands (`doctor`, `show-pending-jobs`, `ready-for-migration`, `purge-jobs`, `clear-website-cache`, `enable-scheduler`, `show-config`, `set-config`, `backup --with-files`, `run-parallel-tests`) | assumed | **present** | Runtime-verified (`bench --help`) |
| 31 | Scheduler/worker/queue behaviour | — | — | **Not verified** — Redis was not running |
| 32 | Email delivery and rendered templates | — | — | **Not verified** — no mail server used; sending was declined |
| 33 | PDF rendering (Chromium) | — | — | **Not verified** — Chromium not provisioned, no site mutation |
| 34 | `bench run-tests` end-to-end | — | — | **Not run** — running the framework suite would mutate the development bench; the flags were verified with `--help` instead |
| 35 | Exact branding `fieldname`s per patch | — | — | **Not verified** — guide correctly requires reading the installed DocType JSON |

## 4. Commands actually executed (v16)

Read-only; no site mutation, no `migrate`, no `build`, no test run, no email, no backup/restore.

```text
bench version
  erpnext 16.51.1 version-16 (5af6561)
  frappe  16.52.0 version-16 (4515014)
  <dev-app> 0.0.1 version-16 (5e799d0)

bench --site <dev-app>.local list-apps
  frappe 16.52.0, <dev-app> 0.0.1, erpnext 16.51.1

bench --site <dev-app>.local execute frappe.get_all --kwargs '{"doctype":"DocType","fields":["name"],"limit_page_length":1}'
  [{"name": "Recommerce Grade Profile"}]

bench --site <dev-app>.local execute frappe.get_all --kwargs '{"doctype":"DocType","fields":["count(name) as n"]}'
  ValidationError: SQL functions are not allowed as strings in SELECT: count(name) as n.
  Use dict syntax like {'COUNT': '*'} instead.

... --kwargs '{"doctype":"DocType","fields":[{"COUNT":"*","as":"n"}]}'
  [{"n": 844}]

... --kwargs '{"doctype":"DocType","fields":["distinct name"]}'
  PermissionError: Invalid field format for SELECT: distinct name.

bench console:
  frappe.qb.get_query("DocType", fields=["name"]).get_sql()
    SELECT `name` FROM `tabDocType`
  frappe.qb.get_query("DocType", fields=["name"], order_by=DefaultOrderBy).get_sql()
    SELECT `name` FROM `tabDocType` ORDER BY `creation` DESC
  DatabaseQuery("DocType").execute(fields=["name"], run=False).get_sql()
    SELECT `name` FROM `tabDocType` ORDER BY `creation` DESC
  frappe.get_hooks("extend_doctype_class")
    {'Address': ['erpnext.accounts.custom.address.ERPNextAddress']}

bench --help / <command> --help
  data-import, import-csv(absent), setup-chrome, doctor, show-pending-jobs,
  ready-for-migration, purge-jobs, clear-website-cache, enable-scheduler,
  show-config, set-config, run-parallel-tests, backup --with-files  → presence confirmed
```

`bench --site <dev-app>.local doctor` and `show-pending-jobs` reported that Redis at
`127.0.0.1:11004` was not reachable. That is an environment condition, recorded rather than worked
around; starting services on the user's bench was outside this review's scope.

## 5. Reproducible test plan for a full matrix

A reviewer with disposable environments should run this. Each step is isolated and reversible.

### 5.1 Provisioning (disposable only)

```bash
# v16
bench init --frappe-branch version-16 /tmp/bench-v16
cd /tmp/bench-v16 && bench new-site v16.test --no-mariadb-socket
bench --site v16.test install-app erpnext

# v15
bench init --frappe-branch version-15 /tmp/bench-v15
cd /tmp/bench-v15 && bench new-site v15.test --no-mariadb-socket
bench --site v15.test install-app erpnext
```

Do not point either bench at production credentials or customer data. Record the exact patch
versions in `docs/templates/environment-inventory.md`.

### 5.2 Container/CI matrix (no test bench required)

A minimal GitHub Actions matrix can exercise the parts that do not need ERPNext data:

```yaml
strategy:
  matrix:
    frappe: [version-15, version-16]
steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-python@v5
    with: { python-version: "3.14" }        # v15 job uses its supported floor
  - run: python3 scripts/validate_repo.py
  - run: python3 -m unittest discover -s scripts/tests -p "test_*.py" -v
```

This validates the repository, not the guidance's runtime behaviour. Runtime claims still need a
bench.

### 5.3 Behaviour checks to run on each bench

| Check | Command / action | Expected evidence |
|---|---|---|
| Version detection | `bench version`, `bench --site <site> list-apps` | exact versions recorded |
| App discovery | `bench --site <site> list-apps` | app list matches hooks |
| Test command | `bench --site <site> run-tests --app <app> --module <module>` | pass/fail output captured |
| Hooks | add a `doc_events`, `doctype_js`, and `extend_doctype_class` sample in a scratch app | behaviour observed on a form and in the DB |
| Fixtures | `bench --site <site> export-fixtures --app <app>` then install on a fresh site | records reproduced |
| Patch | add an idempotent patch, `bench migrate`, run twice | second run is a no-op |
| Query behaviour | `get_all` strict fields, default order | SQL/error observed (as in §4) |
| Branding | follow `white-label-verification.md` on the scratch site | per-surface checklist with results |
| Email | send to a sink mailbox | rendered header/footer inspected |
| PDF | render one document | PDF inspected; Chromium path recorded |
| Upgrade | take a v15 backup, restore into a v16 site on staging, migrate | smoke + branding + reconciliation |

### 5.4 Exit criteria

A row moves from "source/documentation-verified" to "runtime-verified" only when the command was run
on a disposable bench and the output is attached to the delivery test note. Rows 31–35 in §3 remain
unverified until that happens.
