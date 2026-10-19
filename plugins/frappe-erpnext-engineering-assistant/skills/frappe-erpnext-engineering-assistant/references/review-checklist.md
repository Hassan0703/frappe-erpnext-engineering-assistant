# Review Checklist — the gate before reporting a task complete

Run this before saying anything is done. If a box cannot be checked, say which one and why — an
honest gap is acceptable; a false check is not.

## 0. Evidence gate

- [ ] Every claim of success is backed by a command that ran and output I read (or an explicit "not run").
- [ ] No "should work", "tests pass", or "migration complete" without observed results.
- [ ] Limitations, unverified items, and skipped checks are stated.
- [ ] No secrets, credentials, customer data, or production dumps added to the repo, logs, or chat.

## 1. Context and scope

- [ ] Frappe and ERPNext versions detected and recorded (see `version-compatibility.md`).
- [ ] Project instructions (`AGENTS.md` / `CLAUDE.md` / README) read.
- [ ] Working tree state checked; unrelated user changes untouched.
- [ ] Owning app identified for every DocType touched.
- [ ] Ambiguities that affect correctness were raised rather than assumed.
- [ ] Scope of the change (and what was deliberately left out) is clear.

## 2. Placement

- [ ] Own DocType logic is in its own `.py` / `.js`; nothing in `hooks.py` or `public/js` for it.
- [ ] Other apps extended only via `hooks.py` + `overrides/`/`extensions/` + fixtures; no vendor files edited.
- [ ] `set_query` is in `setup`/`onload` of the correct form script.
- [ ] Business rules enforced server-side, not only in JS.
- [ ] No duplicate `frappe.ui.form.on` blocks or duplicate controller methods.
- [ ] Site-level Client/Server Scripts avoided, or documented with a backup if the deployment forces them.
- [ ] Change is reproducible on a fresh site (fixture/patch/app code, not manual steps).

## 3. Framework APIs

- [ ] Errors: `frappe.throw(_())`; info: `frappe.msgprint(_())` / `frappe.show_alert`.
- [ ] All user-facing strings use `_()` / `__()` with `{0}` placeholders.
- [ ] No `print`, `console.log`, `alert`, bare `except`, `raise Exception`.
- [ ] `flt`/`cint`/`getdate` used for doc values.
- [ ] Field behaviour (fetch from, depends on, mandatory) set in the DocType where possible.
- [ ] Correct lifecycle hook used (no submit logic in `validate`).
- [ ] No `frappe.db.commit()` in handlers/controllers/document hooks.

## 4. Data and performance

- [ ] No DB calls inside loops; bulk fetch and map.
- [ ] Explicit `fields`; no `*` in request paths or reports.
- [ ] Aggregates in SQL/Query Builder, not Python.
- [ ] Large/slow work enqueued; jobs log failures and are safe to retry.
- [ ] Cache usage is correct and invalidated on change; no permission-filtered data cached globally.
- [ ] Measured before/after where performance was the goal.
- [ ] Version-specific query syntax verified (v16 strict fields; explicit ordering where it matters).

## 5. Security and permissions

- [ ] Every whitelisted method checks permission, not just authentication.
- [ ] Writes use POST; `allow_guest` justified and rate-limited.
- [ ] Row-level scoping tested with a non-privileged user.
- [ ] `permlevel` used for sensitive fields; JS hiding is not the control.
- [ ] No SQL interpolation; dynamic field/sort names allowlisted.
- [ ] User HTML sanitized server-side; no unescaped output of user content.
- [ ] Uploads private by default, validated, access-checked.
- [ ] `ignore_permissions=True` justified with a comment, or absent.
- [ ] No sensitive data in logs; error messages don't leak internals.

## 6. Version compatibility

- [ ] v15/v16 differences relevant to this change were checked against the detected version.
- [ ] No v14-or-earlier patterns; no v17 support claimed.
- [ ] Unverified version-sensitive claims are labelled as such.
- [ ] Deprecated APIs avoided where the target version replaces them (test classes, print formats,
      field expressions, hooks).

## 7. Tests and verification

- [ ] Targeted test added/updated, or a documented reason there is none.
- [ ] Tests executed; output read; exit status respected (no filtered pipelines hiding failures).
- [ ] Permission/denial path tested where relevant.
- [ ] Failure path tested (invalid input, downstream error, duplicate delivery).
- [ ] Migrate/build/clear-cache run where the change requires it.
- [ ] UI/flow exercised where it changed.
- [ ] Delivery test note prepared (see `assets/templates/delivery-test-note.md`).

## 8. White-labeling (only if identity changed)

- [ ] All in-scope surfaces reviewed: desk, login, website/portal, emails, notifications, print/PDF, favicon, titles.
- [ ] Changes made through supported configuration/hooks, not vendor file edits.
- [ ] Verification table executed (`assets/templates/white-label-verification.md`).
- [ ] Survives `clear-cache`, `bench build`, and `migrate`.
- [ ] Licensing/trademark implications flagged for review.
- [ ] Upgrade checklist updated.

## 9. Migration (only if data moved)

- [ ] Mapping documented; transforms explicit.
- [ ] Load is idempotent; re-run does not duplicate.
- [ ] Run log records read/inserted/updated/skipped/rejected.
- [ ] Reconciliation covers counts, relationships, financials/stock, attachments, exceptions.
- [ ] Known differences approved by the business owner.
- [ ] Not declared successful merely because no errors were raised.

## 10. Deployment and operations (only if released/operated)

- [ ] Backup taken and verified before schema/data changes.
- [ ] Rollback path and data-loss window stated and approved.
- [ ] Smoke test executed post-deploy.
- [ ] Scheduler/workers/queue checked; config changes accounted for.
- [ ] Restore evidence current if recovery behavior changed.
- [ ] Runbook, environment inventory, and release notes updated.

## 11. Documentation and handover

- [ ] Docs updated where behavior, configuration, or operations changed.
- [ ] Configuration inventory updated for new settings/fields/fixtures.
- [ ] Permissions/workflow matrices updated if roles or states changed.
- [ ] Known limitations and technical debt recorded.
- [ ] Handover notes sufficient for another developer to continue.

## 12. Diff hygiene

- [ ] `git status` / `git diff` reviewed; only intended files changed.
- [ ] No debug output, commented-out code, or TODO without an owner.
- [ ] No unrelated reformatting or mass renames.
- [ ] No secrets, credentials, or customer data.
- [ ] Commit/push/deploy performed only if explicitly authorized.

## 13. Final report contents

```text
Changed: <file> — <why this location>
Versions: Frappe <x> / ERPNext <y> (detected from <evidence>)
Verified: <command> → <observed result>
Not verified: <what and why>
Risks/limitations: <...>
Next actions for you: <migrate/build/restart/deploy, if any>
```
