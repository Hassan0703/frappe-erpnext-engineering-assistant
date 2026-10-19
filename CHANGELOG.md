# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The version in `plugins/frappe-erpnext-engineering-assistant/.claude-plugin/plugin.json` must match the first
heading below.

## 2.0.0-beta.1 — 2026-10-19

First public preview. This is the Phase 2 scope and capability work plus the Phase 3 rebrand, release
audit, and publication package. The product covers the full delivery lifecycle for Frappe/ERPNext v15
and v16 projects and requires evidence before an agent reports work as done. It is a preview because
runtime validation is limited to the checks recorded in `docs/audit/` — it is not a stability claim.

### Rebranding and identity (Phase 3)

- Renamed the product to **Frappe ERPNext Engineering Assistant**, the skill to
  `frappe-erpnext-engineering-assistant`, and the marketplace to `frappe-erpnext-assistant`.
- Replaced all inherited product branding, slogans, author lines, and repository URLs in the README,
  plugin README, manifests, project templates, issue templates, and documentation.
- Added `NOTICE` with provenance and attribution; the original MIT license text and copyright notice
  are preserved unchanged in both license files.
- Replaced the inherited icon with a neutral generated mark.
- Rewrote the root README as a product landing page: capabilities by use case, honest evidence levels,
  installation for each host, quick start, white-labeling walkthrough, safety principles, testing,
  limitations, support, and license.
- Added a dated clarification to the historical audit documents so they are read as records of the
  project under its previous name, not as current branding.
- Added `.gitignore` for caches, virtual environments, editor state, and agent tooling directories.

### Added

- **Project discovery and technical audit template** (`docs/templates/project-discovery.md`):
  versions, apps, DocType ownership, customizations, permissions, jobs, integrations, data volume,
  deployment, and risk — the inventory a change plan should start from.
- **Production change risk classification** in the deployment reference: four risk classes with
  required backup, approval, window, and rollback expectations.
- **Evidence levels** used consistently across references and the README: runtime-verified,
  source-verified, documentation-verified, unverified.
- **Phase 3 release audit** (`docs/audit/phase-3-release-audit.md`), a release checklist
  (`docs/audit/phase-3-release-checklist.md`), and release notes (`docs/release-notes/`).
- **White-labeling verification and upgrade checklists** are indexed as first-class templates in the
  template catalogue rather than being mentioned only inside the reference.

- **Version compatibility reference** with detection commands, a sourced v15/v16 difference matrix,
  upgrade-safety rules, and a confidence-labelling scheme (`references/version-compatibility.md`).
- **White-labeling reference** covering discovery, tenancy, surface inventory, safe-change
  classification, implementation sequence, verification, upgrade implications, and the
  licensing/trademark boundary (`references/white-labeling.md`).
- **ERP implementation reference**: discovery, requirements, fit-gap with a standard-first decision
  order, data-model review, workflows, permissions and segregation of duties, accounting/inventory
  cautions, UAT, and handover (`references/erp-implementation.md`).
- **Deployment and operations reference**: hosting patterns, runtime requirements, services, config,
  TLS, secrets, sizing, staging parity, release procedure, rollback, backups, restore drills, DR,
  v15→v16 upgrade planning, and monitoring (`references/deployment-and-operations.md`).
- **Data migration reference**: profiling, cleansing, mapping, sequencing, idempotency, run logs,
  reconciliation, cutover, and post-go-live checks (`references/data-migration.md`).
- **Testing and QA reference**: test layers, version-specific test classes, permission tests, job and
  integration failure tests, UAT, delivery test notes, and evidence rules (`references/testing-and-qa.md`).
- **Security reference**: authorization layers, whitelisted-endpoint rules, SQL injection, XSS and
  sanitization, file uploads, secrets, logging, dependencies, multi-tenancy, privacy, AI security, and
  licensing (`references/security.md`).
- **AI features reference**: use cases with measurable criteria, tool registries, least privilege,
  prompt injection, output validation, human approval, audit, cost/retry/timeout handling, evaluation,
  and ownership (`references/ai-features.md`).
- **Support and incident reference**: intake, severity matrix, safe reproduction, RCA, minimal fixes,
  data-integrity review, regression tests, deployment, communication, and close-out
  (`references/support-and-incidents.md`).
- **26 client templates** in `docs/templates/`, also bundled with the skill so they are available when
  the plugin is installed: discovery (1), white-label (4), ERP (6), deployment/ops (5), migration (5),
  QA/handover (5).
- **Repository validation**: `scripts/validate_repo.py` (manifests, frontmatter, reference/template
  inventory, links, unsupported version phrasing, secrets) and `scripts/sync_templates.py` (keeps the
  bundled template copies in sync), wired into CI.
- `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`, a pull request template, and a GitHub Actions
  workflow.
- `templates/AGENTS.md` for agent-neutral project instructions, alongside the existing `CLAUDE.md`.
- Skill frontmatter now declares a license and a description that covers branding, deployment,
  migration, testing, security, and support work.

### Changed

- **Scope fixed.** `SKILL.md` previously said "Assume Frappe v15+", which implied v17 support and
  contradicted the README. It now states v15/v16-only support, requires the version to be detected
  from the project, and requires version-sensitive claims to be labelled when unverified.
- **The skill now demands evidence.** The workflow is inspect → detect versions → identify the owning
  app → clarify → smallest change → implement → verify (run it) → review the diff → report what
  actually happened, with a list of what was not verified. "Tell the user which commands to run" is no
  longer sufficient.
- **Non-negotiables added**: no secrets in repo/prompts/logs, no production mutation, no destructive
  data operations, no commits/pushes/releases without authorization, no fabricated success.
- **Review checklist is now a gate** covering placement, APIs, data/performance, security, version
  compatibility, tests, white-labeling, migration, deployment, documentation, and diff hygiene.
- **Existing references updated** with verified v15/v16 behavior: strict `get_all` field parsing,
  default-sort change, commits blocked in document hooks, `extend_doctype_class` (v16),
  `override_doctype_class` inheritance, `has_permission` explicit returns, Single DocType type casting,
  Chromium PDF generation, translation format change, test class changes, IIFE report JS, and `/desk`.
- Absolute rules that are actually preferences were softened with the conditions under which the
  discouraged approach is acceptable (site-level scripts, `doc_events` on own DocTypes, `fields=["*"]`).
- README and plugin README refreshed; repository URLs standardised on `Hassan0703/frappe-erpnext-engineering-assistant`;
  multi-agent installation documented honestly (Claude Code packaging; portable `SKILL.md` for
  OpenCode/Cline with the discovery paths that are documented).
- `templates/CLAUDE.md` now captures ERPNext version, installed apps, test command, deployment
  constraints, and verification expectations, and no longer forbids using other skills outright.

### Fixed

- Contradiction between the README (`v15 | v16`) and the skill's unsupported version range.
- Missing guidance for white-labeling, deployment, migration, testing, security depth, AI features,
  support, and licensing — the gaps identified in `docs/audit/repository-audit.md`.
- No automated check for broken links, orphaned references, unsynced templates, or unsupported version
  claims.
- **Phase 2 audit corrections** (`docs/audit/phase-2-technical-findings.md`):
  - Removed invented hooks: `website_catch_all` (does not exist in v15 or v16) and the `homepage`
    hook (the real mechanism is Website Settings `home_page`); error pages now point at an app
    `www/404.html` override and `website_route_rules` / `website_redirects`.
  - Removed `bench import-csv` from the migration guide (not a command on a v16.52 bench); the
    verified `bench --site <site> data-import` remains.
  - Clarified that `app_icon` is declared by ERPNext but not consumed by Frappe core; `app_logo_url`
    and `add_to_apps_screen` are the supported visible-logo mechanisms.
  - Corrected "commit is blocked" in document hooks: in v16 transaction control is disabled, so the
    commit is a no-op with a warning rather than an exception.
  - Corrected the `qb.get_query` default-order claim (plain `get_query` has no implicit ordering;
    `get_all`, `get_list`, and `order_by=DefaultOrderBy` use `creation desc`).
  - Promoted `never_skip_patches` from unverified to verified for v16 (absent from v15).
  - Expanded the safe-change classification to the five required mechanisms (settings, supported
    custom-app, hook/fixture, patch/migration, framework fork) and named `web_include_css` for portal
    branding.
  - Corrected the README claim that every template asks for evidence.
- The validator now fails cleanly on an invalid manifest instead of raising, enforces the intended
  reference and template inventories, checks the numbered reference index, and checks white-labeling
  surface coverage.
- Added `scripts/tests/test_validate_repo.py` (23 stdlib tests) and a CI step for it, replacing the
  previous, unreproducible fault-injection claim in `docs/audit/implementation-roadmap.md`.

### Upgrade notes

- The plugin, skill, and marketplace names changed. An installed copy of the previous plugin is not
  upgraded in place: remove it, add the new marketplace, and install the new plugin (commands in the
  README). Project instruction files that name the old skill must be updated to
  `frappe-erpnext-engineering-assistant`.
- Guidance content is otherwise compatible; no reference was dropped, and no template was removed.

### Compatibility notes

- Guidance targets **Frappe/ERPNext v15 and v16**. v14 and earlier are out of scope; v17+ support is not
  claimed. Upstream-documented v17 removals are mentioned only to warn against deprecated patterns.
- The plugin remains Markdown-only at runtime: no scripts execute, no network calls are made, and no
  data is collected. The scripts in `scripts/` are repository tooling run by CI and contributors.

## 1.0.5

- Previous release: core placement, API, error-handling, performance, report, and review guidance.
