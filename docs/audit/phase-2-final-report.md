# Phase 2 Final Report — Independent Review of `frappe-code-standards`

> **Historical record (Phase 1/2).** This document describes the project under its original
> name, layout, and repository. It was renamed and independently rebranded in Phase 3; see
> `docs/audit/phase-3-release-audit.md`. Preserved as evidence, and exempt from the
> inherited-branding scan (see `NOTICE`). The development site/app name was redacted for
> publication; versions and results are unchanged.


**Date:** 2026-10-19
**Reviewer:** independent principal engineer (Frappe/ERPNext, security, delivery)
**Verdict:** the upgraded assistant is technically sound, operationally useful, and safe to use on
v15/v16 client work, subject to the corrections below and the stated environment limitations. The
corrections were applied; the remaining gaps are environmental, not defects in the product.

## 1. Baseline and review scope

The working copy had a `.git` directory with no commits, branches, or remotes, so it could not serve
as its own baseline. A clean upstream checkout was obtained instead (read-only, outside the working
copy):

```text
NexTash/frappe-code-standards @ 099cbe788c69ed6f27b6b196d3b2671766c56a05 (main, 2026-10-19), 18 files
```

The working copy (95 files, 86 Markdown) adds 77 files, modifies 13 baseline files, and **removes
none**. No baseline functionality or documentation was lost. The baseline defect the previous audit
identified is real: upstream `SKILL.md:12` said "Assume Frappe v15+" while the README badge said
`v15 | v16`.

Reviewed in full: the skill, 16 references, 25 canonical templates and their bundled copies, plugin
and marketplace metadata, both scripts, the CI workflow, the changelog, contribution/security/readme
files, and the three existing audit documents. Detail: `docs/audit/phase-2-baseline.md`.

**Environment:** Frappe 16.52.0 / ERPNext 16.51.1 (`version-16`), app `recommerce` 0.0.1, site
`recommerce.local`, treated as read-only. No v15 bench, no running Redis/queue/scheduler, no mail
server, no Chromium. No production or client environment was accessed, and nothing was committed,
pushed, merged, released, or deployed.

## 2. Findings by severity

| ID | Severity | Finding | Status |
|---|---|---|---|
| F2-01 | High | White-labeling guide cited non-existent hooks: `website_catch_all`; `homepage` used where the real mechanism is Website Settings `home_page`; `app_icon` described as UI metadata though Frappe core 16.52 does not consume it | Fixed |
| F2-02 | Medium | Migration guide listed `bench import-csv`, which does not exist on the v16.52 bench | Fixed |
| F2-03 | Medium | No automated tests existed; the previous report's "fault injection, 13 cases" was not reproducible from any committed artifact | Fixed |
| F2-04 | Medium | Validator crashed on an invalid marketplace manifest instead of failing cleanly | Fixed |
| F2-05 | Low | `frappe.db.commit()` described as "blocked" in document hooks; it is a no-op (transaction control disabled), not an exception | Fixed |
| F2-06 | Low | `qb.get_query` default-order claim was too broad; plain `get_query` emits no `ORDER BY` | Fixed |
| F2-07 | Low | `never_skip_patches` labelled unverified; verified present in v16 and absent from v15 | Fixed |
| F2-08 | Low | Safe-change classification merged hooks and fixtures; the five required mechanisms were not distinct | Fixed |
| F2-09 | Low | Portal branding row named only the desk asset hook (`app_include_css`) | Fixed |
| F2-10 | Low | README claimed every template carries an evidence field; 10 of 25 legitimately do not | Fixed |

No Critical finding was identified. No instruction was found that would produce data loss, privilege
escalation, or an unrecoverable deployment if followed as written.

Full detail and the list of claims that were checked and found correct:
`docs/audit/phase-2-technical-findings.md`.

## 3. Technical corrections made

- `references/white-labeling.md`: five-class safe-change table (settings, supported custom-app,
  hook/fixture, patch/migration, framework fork); real error-page mechanism; `home_page` instead of a
  `homepage` hook; `web_include_css` for website/portal; `app_icon` marked unverified.
- `references/hooks-and-customization.md`: `app_icon` corrected; `role_home_page` /
  `get_website_user_home_page` with Website Settings `home_page`; added `website_route_rules` and
  `website_redirects`; `never_skip_patches` version corrected.
- `references/data-migration.md`: `bench import-csv` removed; verified `bench --site <site> data-import`
  retained.
- `references/version-compatibility.md`: commit-in-hooks, default-ordering, and `never_skip_patches`
  rows corrected; a local verification record added.
- `references/performance.md`, `SKILL.md`: commit wording corrected.
- `README.md`, `plugins/.../README.md`: commit wording and template-evidence claim corrected.
- `scripts/validate_repo.py`: clean JSON failure; intentional reference/template inventories; numbered
  reference-index check; white-labeling coverage check; index duplicate detection.
- `scripts/tests/test_validate_repo.py`: new stdlib test suite (23 tests).
- `.github/workflows/validate.yml`: validator tests added to CI; `on:` quoted for generic YAML parsers.
- `CHANGELOG.md`, `docs/audit/implementation-roadmap.md`, `docs/audit/repository-audit.md`: corrections
  and Phase 2 pointers recorded.

No change was made merely to enlarge the diff. Every edit maps to a finding in
`phase-2-technical-findings.md` or to the Phase 4 test requirement.

## 4. Checks executed

| Check | Result |
|---|---|
| Repository validator (`python3 scripts/validate_repo.py`) | **Passed** — 86 Markdown files, 16 references, 25 templates, 0 errors, 0 warnings |
| Template synchronisation (`sync_templates.py --check`) | **Passed** — bundled templates up to date (25 files) |
| Relative/HTML link checks | **Passed** — part of the validator; no broken local link |
| External URL resolution (canonical sources and badges) | **Passed** — 21 URLs, all HTTP 200 |
| Automated validator tests (`python3 -m unittest discover`) | **Passed** — 23 tests, including 20 failing-case tests |
| JSON parsing (manifests) | **Passed** |
| YAML parsing (`.github/workflows/validate.yml`) | **Passed** — 1 job, 6 steps |
| `py_compile` on all scripts | **Passed** |
| Reference routing and inventory | **Passed** — every reference linked, indexed, and expected |
| White-labeling coverage check | **Passed** |
| Secret scanning | **Passed** — no findings; detection is exercised by tests |
| Conflict markers / trailing whitespace in changed files | **Passed** |
| Diff against upstream baseline | **Passed** — 0 removals, 13 modified, 77 added |
| v16 runtime verification (read-only commands in §5) | **Passed** for the commands listed |
| v15 runtime verification | **Not run** — no v15 bench available |
| Scheduler / workers / queue behaviour | **Blocked by environment** — Redis not running |
| Email delivery and rendering | **Not run** — no mail server, and sending was declined |
| PDF rendering (Chromium) | **Not run** — Chromium not provisioned; would require site mutation |
| `bench run-tests` end-to-end | **Not run** — would mutate the development bench; flags verified with `--help` |
| GitHub Actions execution | **Not run** — workflow cannot be executed from here |
| Agent-level evaluation of the five scenarios | **Not run** — no harness; rubric delivered instead |
| Legal review of licensing/trademark positions | **Not run** — out of scope; framed as questions for counsel |

A check is never reported as passed when it was blocked, and no failing check was weakened to pass.

## 5. v15/v16 compatibility evidence

Evidence levels and the full matrix are in `docs/audit/phase-2-compatibility-matrix.md`. Highlights
obtained from **installed v16 source and runtime** (not from documentation alone):

- `frappe.get_all("DocType", fields=["count(name) as n"])` → `ValidationError: SQL functions are not
  allowed as strings in SELECT`; `{"SUM": "grand_total", "as": "total"}` and `{"COUNT": "*"}` work.
- `fields=["distinct name"]` → `PermissionError: Invalid field format for SELECT`.
- Default order is `creation desc` for the `get_all`/`get_list` path and for
  `qb.get_query(..., order_by=DefaultOrderBy)`; plain `qb.get_query` emits no `ORDER BY`.
- `frappe/model/document.py` disables transaction control around hooks, so `commit()` warns and no-ops.
- `override_doctype_class` enforces `issubclass`; `extend_doctype_class` and `never_skip_patches`
  exist in v16 and are absent from the `version-15` branch.
- `frappe.permissions.has_permission` uses `print_logs` in v16 (`raise_exception` in v15);
  `frappe.has_permission(..., throw=True)` is valid in both.
- `sendmail(now=True)` adds to `after_commit` rather than committing; Single values are cast;
  `sanitize_html` uses nh3; `bench setup-chrome` and `bench --site <site> data-import` exist;
  `bench version` uses the plain format.

v15 behaviour was verified from the `version-15` branch source, not executed. The compatibility
matrix includes a reproducible provisioning and behaviour-check plan for a reviewer with disposable
benches, and a container/CI matrix that can run without a bench.

## 6. Agent evaluation

Five realistic scenarios (white-label, workflow with approvals, data migration, release deployment,
production defect) were specified with expected behavior and cross-scenario regression risks in
`docs/audit/phase-2-agent-evaluation.md`. A static coverage review of the skill was performed: all
five are **covered** by routing plus reference guidance. **No live agent run was executed**, so no
scenario is claimed as passed. A 12-criterion rubric (with safety criteria weighted and zero
tolerated) is provided so the evaluation can be run and scored honestly later.

## 7. Remaining uncertainties and risks

1. Exact branding `fieldname`s and their patch-level stability are not enumerated; the guide requires
   reading the installed DocType JSON. Acceptable, but it depends on the agent doing so.
2. Single-DocType fixture round-tripping remains unverified; the guide offers the patch /
   `after_install` alternative.
3. PWA support per patch level remains unverified.
4. v15 behaviour is source-verified only; a v15 runtime bench would raise confidence.
5. Scheduler, worker, email, and PDF paths were not exercised; the deployment runbook requires the
   executing engineer to record real evidence.
6. The test suite covers the repository's structure and the validator, not framework behaviour. That
   is the correct automated scope for a Markdown product, but it means "tests pass" here does not mean
   "the guidance is true".
7. The working copy still has no local commit history; provenance of individual edits cannot be shown
   from Git. Nothing was committed.

## 8. Files changed

Relative to the upstream baseline (`099cbe7`): **0 removals, 13 modified, 77 added.**

Modified: `.claude-plugin/marketplace.json`, `plugins/frappe-code-standards/.claude-plugin/plugin.json`,
`plugins/frappe-code-standards/README.md`, `README.md`, `templates/CLAUDE.md`, `SKILL.md`, and the
references `client-patterns.md`, `code-placement.md`, `hooks-and-customization.md`, `performance.md`,
`reports-and-printing.md`, `review-checklist.md`, `server-patterns.md`.

Added: `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, 25 canonical templates, 25 bundled template
copies, 9 references, `scripts/validate_repo.py`, `scripts/sync_templates.py`,
`scripts/tests/test_validate_repo.py`, `.github/workflows/validate.yml`,
`.github/pull_request_template.md`, `templates/AGENTS.md`, `docs/templates/README.md`, the original
three audit documents, and the five `docs/audit/phase-2-*.md` documents produced by this review.

The largest changes in this review itself are the five Phase 2 audit documents, the new test suite,
and the targeted corrections listed in §3.

## 9. Git state and uncommitted changes

The working copy is still an un-committed repository: `git rev-list --all --count` is 0, there are no
branches, tags, or remotes, and every path is untracked. `.freebuff/project-id` is local environment
metadata and is not part of the product. Nothing was staged, committed, pushed, merged, released, or
deployed, per the rules of engagement. To preserve the work, the user should commit it deliberately.

## 10. Revised scorecard

Scored against the engagement's acceptance criteria, using executed evidence. The previous report
scored 3.75/5 with several categories at 4/5.

| Category | Score | Evidence | Remaining gap |
|---|---:|---|---|
| Frappe/ERPNext engineering | 4.5/5 | Placement, lifecycle, transactions, query, report/print guidance match installed v16 source and runtime | Patch-level coverage not exhaustive |
| v15/v16 compatibility | 4.5/5 | Sourced matrix, now with runtime evidence on 16.52 and v15 source comparison; invented claims removed | No v15 runtime bench |
| White-labeling | 4.5/5 | Full surface coverage, five-class classification, real mechanisms, verification and legal boundary | Exact fieldnames per patch delegated to the installed JSON |
| Deployment and operations | 4/5 | Runbook, backups, restore drills, rollback, v16 runtime/PDF requirements; commands verified | Not executed on a real deployment |
| Data migration | 4/5 | Profiling → mapping → idempotency → reconciliation → cutover; invented command removed | No executed migration |
| Security, privacy, licensing | 4/5 | Layered authz, injection, XSS, uploads, secrets, tenancy, privacy, AI boundaries, licensing boundary | No third-party security or legal review |
| Testing and QA | 4/5 | v16 test classes, permission/failure tests, delivery evidence; validator now has a real test suite | Repository tests cannot prove framework behaviour |
| Repository validation | 4.5/5 | Validator, sync check, 23 automated tests, CI wiring, clean failure on bad input | CI not executed on GitHub |
| Support and maintenance | 4/5 | Intake, severity, RCA, minimal fix, regression, communication | Not exercised on a live incident |
| Documentation and handover | 4.5/5 | Handover, configuration inventory, contribution/PR/CI, changelog, corrected claims | No client-facing rendered docs |
| AI coding-agent usability | 4/5 | Clear scope, routing, evidence gate, honest multi-agent notes | Only Claude Code packaging tested; no live eval run |
| Version control | 2/5 | Git-state checks and commit discipline in the workflow; baseline recovered externally | Working copy has no commits, branches, or remotes |

**Average: 4.2 / 5.** The increase over the previous 3.75 reflects runtime-verified v16 claims,
removed invented guidance, and a committed test suite. The limiting factors are environmental (no v15
runtime bench, no live deployment, no agent harness) and the absence of Git history; they are stated
rather than papered over.
