# Implementation Roadmap

> **Historical record (Phase 1/2).** This document describes the project under its original
> name, layout, and repository. It was renamed and independently rebranded in Phase 3; see
> `docs/audit/phase-3-release-audit.md`. Preserved as evidence, and exempt from the
> inherited-branding scan (see `NOTICE`). The development site/app name was redacted for
> publication; versions and results are unchanged.


**Driven by:** `repository-audit.md` findings F-01…F-28 and `requirements-traceability.md`
**Ordering:** exactly the brief's Phase K priority list.
**Status values:** Planned · In progress · Done · Blocked (with reason) · Deferred (with reason).
**Rule:** no task is marked Done until its validation column has actually been executed or reviewed.

> Baseline note: the working copy has no `.git` directory, so no branch could be created. All edits
> are on the provided working copy. No commit, push, release, or visibility change was performed.

---

## P1 — Critical technical errors, security risks, misleading instructions

| # | Req | Problem | Proposed change | Files | Depends on | Risk | Validation | Status |
|---|---|---|---|---|---|---|---|---|
| 1.1 | VER-01 | `SKILL.md:12` says "Assume Frappe v15+", implying v17 support and contradicting the README badge | Replace with explicit v15/v16-only scope, an unknown-version stop rule, and a detection protocol | `skill/SKILL.md` | — | Low | Banned-phrase validator; manual read | Done |
| 1.2 | AGT-01…11 | Skill tells the agent to *tell* the user commands, never to run tests or inspect the diff; can report unverified success | Rewrite workflow: inspect → version → owner → clarify → smallest change → implement → verify → diff review → evidence report | `skill/SKILL.md`, `review-checklist.md` | 1.1 | Low | Checklist contains all 10 steps; manual read | Done |
| 1.3 | SEC-04, DOC-15 | No secrets or production-boundary rule | Add non-negotiables: no secrets in repo/chat, no production mutation, no destructive DB ops, no commits/pushes without authorization | `skill/SKILL.md`, `references/security.md` | 1.2 | Low | Secret-scan validator; manual read | Done |
| 1.4 | AGT-04, AGT-11 | No stop-and-ask rule; no anti-fabrication rule | Add both, with examples of when to halt | `skill/SKILL.md` | 1.2 | Low | Manual read | Done |

## P2 — Missing foundational capabilities

| # | Req | Problem | Proposed change | Files | Depends on | Risk | Validation | Status |
|---|---|---|---|---|---|---|---|---|
| 2.1 | VER-03, VER-04 | No v15/v16 difference documentation | New compatibility reference: detection, matrix with source + confidence, upgrade-safety rules | `references/version-compatibility.md` | 1.1 | Medium (must not overclaim) | Each row cites a source; unverified rows labelled | Done |
| 2.2 | SEC-01…13 | Security coverage is two lines | New security reference: authz, permlevel, SQL, XSS, uploads, secrets, APIs, logging, dependencies, tenant isolation, privacy, licensing | `references/security.md` | — | Low | Checklist coverage review | Done |
| 2.3 | QA-01…14 | No testing guidance | New testing reference: v15/v16 test classes, permission tests, jobs, migration, UAT, evidence | `references/testing-and-qa.md` | 2.1 | Medium (v16 classes) | Sourced test import example | Done |
| 2.4 | SUP-01…12 | No support workflow | New support/incident reference with severity matrix and RCA | `references/support-and-incidents.md` | — | Low | Manual review | Done |
| 2.5 | FUN-09, QA-14 | Review checklist checks style, not evidence | Expand checklist into gated checks: placement, version, security, tests, evidence, docs | `references/review-checklist.md` | 2.2, 2.3 | Low | Checklist items map to requirement IDs | Done |

## P3 — White-labeling architecture and workflows

| # | Req | Problem | Proposed change | Files | Depends on | Risk | Validation | Status |
|---|---|---|---|---|---|---|---|---|
| 3.1 | WL-01…17 | Zero branding coverage | New white-label reference: discovery, surface table, safe-change classification, v15/v16 differences, verification, upgrade impact, legal boundary | `references/white-labeling.md` | 2.1 | Medium (fieldnames unverified) | Every surface has change method + verification; uncertainty labelled | Done |
| 3.2 | WL-01 | No discovery artifact | `white-label-discovery.md` | `docs/templates/` | 3.1 | Low | Template linked from reference | Done |
| 3.3 | WL-16, DOC-01 | No implementation plan artifact | `white-label-implementation-plan.md` | `docs/templates/` | 3.1 | Low | Template linked | Done |
| 3.4 | WL-13, WL-15, QA-07 | No verification artifact | `white-label-verification.md` incl. post-migrate/build/cache checks | `docs/templates/` | 3.1 | Low | Template linked | Done |
| 3.5 | WL-08, WL-13 | No upgrade artifact | `white-label-upgrade-checklist.md` | `docs/templates/` | 3.1, 2.1 | Low | Template linked | Done |

## P4 — v15/v16 compatibility and verification across existing guidance

| # | Req | Problem | Proposed change | Files | Depends on | Risk | Validation | Status |
|---|---|---|---|---|---|---|---|---|
| 4.1 | VER-05, FUN-10 | Printing guidance would mislead on v16 | Rewrite reports/printing with v16 Print Format Editor, Chromium, `bench setup-chrome`, classic deprecation | `references/reports-and-printing.md` | 2.1 | Medium | Commands match PDF docs | Done |
| 4.2 | VER-05, FUN-11 | Client guidance predates v16 UI | Add `/desk`, IIFE report JS, list-view changes, and keep v15-safe patterns | `references/client-patterns.md` | 2.1 | Low | Manual review | Done |
| 4.3 | VER-03, FUN-12 | Hooks ref omits v16 `extend_doctype_class`, branding/privacy hooks | Extend hooks reference with version tags for each hook | `references/hooks-and-customization.md` | 2.1 | Medium | Every hook version-labelled | Done |
| 4.4 | VER-03, DEV-03 | Server ref lacks v16 behavior changes and transactions | Add strict `get_all` fields, default sort, commit-in-hooks ban, Single-cast, `savepoint`/`for_update` | `references/server-patterns.md` | 2.1 | Medium | Sourced claims | Done |
| 4.5 | VER-07 | Placement rules lack v16 extension branch | Add `extend_doctype_class` and modern layout | `references/code-placement.md` | 2.1 | Low | Manual review | Done |
| 4.6 | FUN-07, MIG-09 | Performance ref asserts rules without measurement | Add `EXPLAIN`, debug SQL, index and job checks | `references/performance.md` | 2.1 | Low | Manual review | Done |

## P5 — Deployment, migration, testing, operational reliability

| # | Req | Problem | Proposed change | Files | Depends on | Risk | Validation | Status |
|---|---|---|---|---|---|---|---|---|
| 5.1 | DEP-01…17 | No deployment/ops guidance | New deployment reference: patterns, services, TLS, secrets, backups, restore drills, upgrades, rollback, monitoring, v16 Chromium | `references/deployment-and-operations.md` | 2.1 | Medium (commands vary) | Commands marked verify-first; restore drill mandatory | Done |
| 5.2 | MIG-01…14 | No migration guidance | New migration reference: profiling → mapping → idempotent load → reconciliation → cutover | `references/data-migration.md` | 2.1 | Medium | Rejects "no errors = success" | Done |
| 5.3 | DEP-12, DEP-13, DEP-15 | No ops templates | `deployment-runbook.md`, `environment-inventory.md`, `backup-restore-test.md`, `incident-report.md`, `release-and-rollback.md` | `docs/templates/` | 5.1 | Low | All linked from index | Done |
| 5.4 | MIG-04…13 | No migration templates | `migration-plan.md`, `data-mapping.md`, `migration-run-log.md`, `migration-reconciliation.md`, `cutover-checklist.md` | `docs/templates/` | 5.2 | Low | All linked | Done |

## P6 — Documentation, handover, support

| # | Req | Problem | Proposed change | Files | Depends on | Risk | Validation | Status |
|---|---|---|---|---|---|---|---|---|
| 6.1 | ERP-01…12 | No ERP implementation method | New ERP reference: standard-first, fit-gap, design review, SoD, accounting/inventory caution, UAT, handover | `references/erp-implementation.md` | — | Low | Manual review | Done |
| 6.2 | ERP-01…12, QA-13 | No discovery/design/UAT artifacts | `requirements-and-acceptance.md`, `fit-gap-analysis.md`, `technical-design.md`, `permissions-matrix.md`, `configuration-inventory.md`, `uat-signoff.md` | `docs/templates/` | 6.1 | Low | All linked | Done |
| 6.3 | QA-05…14 | No testing/delivery artifacts | `test-plan.md`, `regression-checklist.md`, `delivery-test-note.md`, `defect-report.md`, `handover-checklist.md` | `docs/templates/` | 2.3 | Low | All linked | Done |
| 6.4 | DOC-11, REPO-08 | No changelog, contribution or PR process | `CHANGELOG.md`, `CONTRIBUTING.md`, `.github/pull_request_template.md` | root, `.github` | — | Low | Link check | Done |

## P7 — Agent integration, discoverability, usability

| # | Req | Problem | Proposed change | Files | Depends on | Risk | Validation | Status |
|---|---|---|---|---|---|---|---|---|
| 7.1 | AGT-13 | `description` activates only for code standards | Rewrite description to cover branding, deployment, migration, testing, review, with v15/v16 scope | `skill/SKILL.md` | 1.1 | Low | Validator length + manual review | Done |
| 7.2 | AGT-12 | Only Claude documented | Add OpenCode/Cline/AGENTS.md paths honestly, with limitations | `README.md`, `templates/AGENTS.md` | — | Low | Paths match OpenCode docs | Done |
| 7.3 | AGT-01, DEV-08 | Project template lacks facts and over-restricts skills | Rewrite `templates/CLAUDE.md`; add `AGENTS.md` | `templates/` | — | Low | Fields reviewed | Done |
| 7.4 | AGT-13 | No routing from entry point to new material | Add task-routing table and reference index | `skill/SKILL.md` | all refs | Low | Validator: every reference linked | Done |

## P8 — Optional enhancements and polish

| # | Req | Problem | Proposed change | Files | Depends on | Risk | Validation | Status |
|---|---|---|---|---|---|---|---|---|
| 8.1 | REPO-01…06 | No repository validation | Stdlib-only Python validator: JSON, frontmatter, links, inventory, banned phrases, secrets | `scripts/validate_repo.py` | all files | Low | Run + fault injection | Done |
| 8.2 | REPO-07 | No CI | GitHub Actions workflow running the validator | `.github/workflows/validate.yml` | 8.1 | Low | YAML parse; local run | Done |
| 8.3 | REPO-09 | Version bump without release notes | Bump plugin to 2.0.0; add CHANGELOG with compatibility policy | `plugin.json`, `marketplace.json`, `CHANGELOG.md` | — | Low | JSON parse | Done |
| 8.4 | F-27 | README/marketplace copy drift | Refresh README and plugin README; align descriptions | `README.md`, plugin README | 7.1 | Low | Link check | Done |
| 8.5 | F-15 | Repo URL casing inconsistent | Standardize on `NexTash/frappe-code-standards` | README, plugin.json, marketplace | — | Low | Text search | Done |
| 8.6 | F-16 | Absolute rules that are preferences | Soften to "default / discouraged / never" with conditions | `code-placement.md`, `hooks-and-customization.md`, `performance.md` | — | Low | Manual review | Done |
| 8.7 | REPO-08 | No security reporting path | Add `SECURITY.md` | root | — | Low | Link check | Done |

---

## Deferred / out of scope (explicit)

| Item | Reason |
|---|---|
| Automated test suite for the *plugin* beyond structural validation | The product is instructional Markdown; runtime behavior is model-driven and cannot be asserted deterministically. Structural + link validation is the meaningful automated check. Deferred. |
| v17 guidance | Brief forbids claiming v17 support. Forward-looking v17 removals are mentioned only where upstream documents them (e.g. wkhtmltopdf). |
| Client-environment execution (bench commands, restores, branding checks) | No Frappe bench or client access in this environment. Templates require the executing engineer to record real evidence. |
| Git branch/commit | No `.git` directory; committing was not authorized. |
| Legal review of branding/licensing | Requires qualified counsel; repository states questions, not conclusions. |

---

## Execution log

| Date | Task group | Result |
|---|---|---|
| 2026-10-19 | Audit (baseline) | Full 18-file read; upstream verification of v16 breaking changes, Query Builder refactor, printing/PDF, bench commands, hooks, licensing, OpenCode skill discovery |
| 2026-10-19 | P1 critical fixes | `SKILL.md` rewritten: v15/v16-only scope, detection protocol, 12 non-negotiables, inspect→verify→report workflow, evidence gate |
| 2026-10-19 | P2 foundations | 9 new references added; review checklist converted into a gated review with evidence requirements |
| 2026-10-19 | P3 white-label | `white-labeling.md` + 4 templates |
| 2026-10-19 | P4 compatibility | 7 existing references updated with verified v15/v16 behavior; version phrasing normalized to prevent ambiguous ranges |
| 2026-10-19 | P5 ops/migration | `deployment-and-operations.md`, `data-migration.md` + 10 templates |
| 2026-10-19 | P6 docs/handover | `erp-implementation.md`, `support-and-incidents.md`, `ai-features.md`, `security.md`, `testing-and-qa.md` + 11 templates |
| 2026-10-19 | P7 agent integration | Description rewritten for discoverability; `templates/AGENTS.md` added; multi-agent paths documented honestly |
| 2026-10-19 | P8 polish | Validator, template sync, CI workflow, CONTRIBUTING, SECURITY, CHANGELOG, PR template, README refresh, version bump to 2.0.0 |

## Validation actually executed

All commands were run in this working copy on 2026-10-19. No `bench` command was run — no Frappe
bench exists in this environment.

| # | Command / check | Result |
|---|---|---|
| 1 | `python3 scripts/validate_repo.py` | **0 errors, 0 warnings** — 81 markdown files, 16 references, 25 templates |
| 2 | `python3 scripts/sync_templates.py --check` | bundled templates up to date (25 files) |
| 3 | Fault injection, 13 cases (see below) | all behaved as expected |
| 4 | `yaml.safe_load` on `.github/workflows/validate.yml` | valid; 1 job, 5 steps |
| 5 | Repo-URL casing audit | no `Frappe-Code-Standards` references remain outside the audit's historical record |
| 6 | Reference/template inventory | every reference linked from `SKILL.md`; every template listed in the index and byte-identical to its bundled copy |

### Fault injection detail

Run against a throwaway copy of the repository, so the working copy was never mutated:

| Injected fault | Expected | Observed |
|---|---|---|
| Baseline (as shipped) | pass | exit 0 |
| `Assume Frappe v15+` added to a reference | fail | exit 1 |
| Link to a non-existent reference | fail | exit 1 |
| Reference removed from the `SKILL.md` list (orphan) | fail | exit 1 |
| Bundled template modified (drift) | fail | exit 1 |
| `api_key = "..."` added to `CONTRIBUTING.md` | fail | exit 1 |
| Truncated `plugin.json` | fail | exit 1 |
| CHANGELOG version ≠ plugin.json version | fail | exit 1 |
| Each fault reverted | pass | exit 0 |

> **Phase 2 correction (2026-10-19).** The fault injection above was performed interactively and no
> harness was committed, so a reviewer could not reproduce the claim. `scripts/tests/test_validate_repo.py`
> now implements passing and failing cases as a runnable stdlib suite, and CI runs it. The Phase 2
> review also corrected several guidance claims; see `docs/audit/phase-2-technical-findings.md` and
> `docs/audit/phase-2-final-report.md`.

### Checks that were NOT run (and why)

- Any `bench` command (`migrate`, `build`, `run-tests`, `backup`, `restore`): no Frappe bench or site
  exists in this environment.
- Any branding/reporting verification against a live site.
- `git diff` / branch review: the supplied directory has no `.git` directory.
- CI itself: the workflow is written and its commands pass locally, but it has not executed on GitHub.
