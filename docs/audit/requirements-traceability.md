# Requirements Traceability Matrix

> **Historical record (Phase 1/2).** This document describes the project under its original
> name, layout, and repository. It was renamed and independently rebranded in Phase 3; see
> `docs/audit/phase-3-release-audit.md`. Preserved as evidence, and exempt from the
> inherited-branding scan (see `NOTICE`). The development site/app name was redacted for
> publication; versions and results are unchanged.


**Repository:** `frappe-code-standards`
**Baseline:** working copy as audited in `repository-audit.md` (no `.git` metadata available)
**Date:** 2026-10-19
**Coverage status values refer to the BASELINE repository**, before implementation. Post-implementation
status is tracked in `implementation-roadmap.md`.

The matrix uses the column set required by the engagement brief: Requirement ID, Capability,
Existing coverage, Coverage status, Severity, Evidence, Proposed change, Validation.

## Legend

| Status | Meaning |
|---|---|
| **Complete** | Baseline fully satisfies the requirement with usable, accurate guidance |
| **Partial** | Topic is mentioned but lacks the specificity, workflow, or verification required |
| **Missing** | No coverage |
| **Incorrect** | Coverage exists but is wrong, unsafe, or contradicts the brief |
| **Unverified** | Claim exists but could not be confirmed against source/docs |

Severity: **C**ritical, **H**igh, **M**edium, **L**ow.
Coverage paths are relative to the repository root; `skill/` = `plugins/frappe-code-standards/skills/frappe-code-standards/`.

---

## A. Core Frappe engineering standards (FUN)

| Requirement ID | Capability | Existing coverage | Coverage status | Severity | Evidence | Proposed change | Validation |
|---|---|---|---|---|---|---|---|
| FUN-01 | Logic placed in the owning DocType's `.py`/`.js` | `skill/SKILL.md` Placement Rules; `skill/references/code-placement.md` | Complete | — | Decision tree with wrong/right examples | Keep; add `extend_doctype_class` branch | Review checklist item |
| FUN-02 | Other apps extended only via hooks/fixtures, never edited | `skill/SKILL.md`; `code-placement.md` | Complete | — | Explicit "never edit frappe/erpnext" | Keep | Checklist item |
| FUN-03 | Standard error/message APIs | `skill/SKILL.md`; `server-patterns.md` | Complete | — | `frappe.throw`, `msgprint`, exception classes | Keep; add v16 `has_permission` nuance elsewhere | Code review checklist |
| FUN-04 | Translation discipline | `SKILL.md`; `server-patterns.md`; `client-patterns.md` | Partial | M | Correct `_()`/`__()` rules; no v16 Gettext workflow | Add translation workflow to white-label reference | Link check + review |
| FUN-05 | Client form patterns (`set_query` in `setup`, `frm.call`) | `client-patterns.md` | Complete | — | Correct examples | Add v16 route/IIFE notes | Checklist item |
| FUN-06 | Server-side enforcement of business rules | `SKILL.md` Step 0; `client-patterns.md` | Complete | — | "Never rely on JS alone" | Keep | Checklist item |
| FUN-07 | Explicit fields, no N+1 | `SKILL.md`; `performance.md` | Complete | — | Before/after N+1 example | Add measurement method | Checklist item |
| FUN-08 | Child-table event placement | `SKILL.md`; `code-placement.md`; `client-patterns.md` | Complete | — | Parent-file example | Keep | Link check |
| FUN-09 | Whitelisted-method authorization | `server-patterns.md` | Partial | H | `has_permission` example; no `allow_guest`, rate-limit, or permlevel depth | Add security reference; cross-link | Security review checklist |
| FUN-10 | Reports and print formats | `reports-and-printing.md` | Partial | H | v15-centric; no v16 print/PDF migration | Rewrite with v15/v16 split | Reviewer sign-off |
| FUN-11 | Background jobs | `performance.md` | Partial | M | `frappe.enqueue` example; no failure/idempotency | Add retry/idempotency/failure guidance | Checklist item |
| FUN-12 | Fixtures and patches | `hooks-and-customization.md` | Partial | M | Good basics; no `never_skip_patches`, no Single DocType caveat | Extend hooks + migration references | Link check |
| FUN-13 | Naming/naming series | `server-patterns.md` | Complete | — | Autoname guidance | Keep | — |
| FUN-14 | App layout and code ownership | `code-placement.md` | Partial | L | No `services/`, `tests/`, `extend_doctype_class` modules | Extend layout tree | Link check |

---

## B. Version scope and compatibility (VER)

| Requirement ID | Capability | Existing coverage | Coverage status | Severity | Evidence | Proposed change | Validation |
|---|---|---|---|---|---|---|---|
| VER-01 | Support v15 and v16 only; no v14, no v17 claims | `SKILL.md:12` | Incorrect | C | "Assume Frappe v15+"; README says `v15 \| v16` | Explicit scope block; banned-phrase scan | Validator fails on `v15+` |
| VER-02 | Detect active Frappe/ERPNext versions before version-sensitive work | None | Missing | C | Template records only Frappe major | Add detection commands to `SKILL.md` + compatibility reference | Checklist gate |
| VER-03 | Document v15/v16 differences that affect implementation | None | Missing | C | Zero version-comparison content | New `version-compatibility.md` matrix with sources | Matrix reviewed against cited docs |
| VER-04 | Label unverified recommendations | None | Missing | H | No confidence labels anywhere | Add confidence/verification labels to version-sensitive rules | Reviewer sign-off |
| VER-05 | Version-aware bench commands | Partial | Missing | H | `migrate/build/clear-cache` only; no PDF/chrome, translations, tests | Add per-version command notes, verify-first framing | Link + manual review |
| VER-06 | Frappe/ERPNext/add-on major versions must match | None | Missing | H | — | Add compatibility rules to deployment + compatibility refs | Checklist |
| VER-07 | No invented APIs/hooks/commands | Implicit | Partial | M | Accurate baseline APIs, but `extend_doctype_class` hedged vaguely | Cite version for each hook; remove hedges where verified | Source-review table |
| VER-08 | Upgrade-safe guidance surfaced for every risky change | None | Missing | H | No upgrade-safety framing | Add change classification + upgrade checklist template | Template link check |

---

## C. White-labeling (WL)

| Requirement ID | Capability | Existing coverage | Coverage status | Severity | Evidence | Proposed change | Validation |
|---|---|---|---|---|---|---|---|
| WL-01 | Branding discovery and scoping checklist | None | Missing | H | `grep` for brand/logo/favicon = 0 matches | `white-label-discovery.md` + reference section | Template inventory check |
| WL-02 | Desk/navbar/login branding | None | Missing | H | — | Surface table with hooks/settings and verification | Manual review |
| WL-03 | Logos, favicons, icons, theme | None | Missing | H | — | Surface table; asset locations; cache/build steps | Manual review |
| WL-04 | Website and portal identity | None | Missing | H | — | Website Settings/`brand_html`/`website_context` guidance | Manual review |
| WL-05 | Browser titles and product naming | None | Missing | M | — | Guidance + "inspect templates" instruction | Manual review |
| WL-06 | Email, notifications, templates | None | Missing | H | — | `default_mail_footer`, templates, sender hooks | Manual review |
| WL-07 | Print formats, headers/footers, PDF | Partial | Missing | H | Printing ref covers formats, not branding or v16 PDF | Add print/PDF branding section incl. Chromium | Manual review |
| WL-08 | Workspaces and navigation | None | Missing | M | — | Workspace + apps-screen guidance; v16 sidebar | Manual review |
| WL-09 | Terminology and translations | Partial | Missing | H | Translation rules exist; no terminology process | Add CSV (v15) vs PO (v16) workflow | Manual review |
| WL-10 | Client CSS/JS/static assets | Partial | Partial | M | `public/js` mentioned for overrides only | Add branding asset/bundle guidance | Manual review |
| WL-11 | Custom app naming and packaging | Partial | Partial | M | `app_title` not covered; app layout exists | Add app metadata (`app_title`, `app_icon`, `app_color`) | Manual review |
| WL-12 | Removing/replacing upstream visible branding | None | Missing | H | — | Guidance + legal boundary, no core-edit shortcuts | Manual review |
| WL-13 | Branding verification after install/migrate/cache/upgrade | None | Missing | H | — | Verification template + post-upgrade checklist | Template inventory |
| WL-14 | Staging vs production branding parity | None | Missing | M | — | Environment comparison section in verification template | Template review |
| WL-15 | Automated branding checks where practical | None | Missing | L | — | Curl/asset checks in verification template | Template review |
| WL-16 | Classify changes (config/app/hook/patch/fork) | None | Missing | H | — | Classification table with risk/maintenance cost | Manual review |
| WL-17 | Licensing/trademark/attribution boundary | None | Missing | H | No license guidance | Legal-boundary section; questions for counsel | Manual review |

---

## D. ERP implementation (ERP)

| Requirement ID | Capability | Existing coverage | Coverage status | Severity | Evidence | Proposed change | Validation |
|---|---|---|---|---|---|---|---|
| ERP-01 | Business discovery and stakeholder requirements | None | Missing | H | — | `erp-implementation.md` + requirements template | Template inventory |
| ERP-02 | Existing-process analysis and fit-gap | None | Missing | H | — | Fit-gap method + template | Template inventory |
| ERP-03 | Standard ERPNext vs customization decision | None | Missing | H | — | Standard-first decision rules with cost framing | Manual review |
| ERP-04 | Data model and DocType design | Partial | Partial | M | Placement rules cover files, not schema design | Add design review prompts (naming, child tables, indexes) | Manual review |
| ERP-05 | Workflows, approvals, notifications, assignments | None | Missing | H | — | Add workflow matrix template | Template inventory |
| ERP-06 | Roles, permissions, segregation of duties | Partial | Partial | H | One `permlevel` line | Add permissions-matrix template + SoD guidance | Template inventory |
| ERP-07 | Reports, dashboards, workspaces, print formats | Partial | Partial | M | Report/print reference | Add implementation-level guidance | Link check |
| ERP-08 | Accounting and inventory implications | None | Missing | H | — | Add "involve accounting owner" checklist and reconciliation link | Manual review |
| ERP-09 | Integrations and failure handling | Partial | Partial | M | External-call error example only | Add integration section + contract doc | Manual review |
| ERP-10 | Configuration management/reproducibility | Partial | Partial | H | Fixtures/patches covered | Add configuration inventory template | Template inventory |
| ERP-11 | UAT and sign-off | None | Missing | H | — | UAT template | Template inventory |
| ERP-12 | Training, rollout, handover | None | Missing | H | — | Handover checklist + runbook | Template inventory |

---

## E. Deployment and operations (DEP)

| Requirement ID | Capability | Existing coverage | Coverage status | Severity | Evidence | Proposed change | Validation |
|---|---|---|---|---|---|---|---|
| DEP-01 | Infrastructure/hosting requirements | None | Missing | H | — | Deployment reference: bench, Docker, managed | Manual review |
| DEP-02 | Supported deployment patterns + version constraints | None | Missing | H | — | Pattern table; v16 Python 3.14/Node 24 | Sourced claims table |
| DEP-03 | Environment prep and dependencies | None | Missing | H | — | Runbook step 0 | Template review |
| DEP-04 | Bench/site configuration | None | Missing | H | — | `site_config` vs `common_site_config`, verify-first commands | Manual review |
| DEP-05 | Database and Redis requirements | None | Missing | H | — | Reference section | Manual review |
| DEP-06 | Web/worker/scheduler/background health | None | Missing | H | — | `bench doctor`, pending jobs, scheduler enablement | Manual review |
| DEP-07 | Domains, DNS, reverse proxy, TLS | None | Missing | H | — | Runbook section + expiry check | Template review |
| DEP-08 | Secrets and env-specific configuration | None | Missing | C | No secret rule anywhere | Deployment + security references | Validator secret scan |
| DEP-09 | Email, storage, monitoring, logging, alerting | None | Missing | H | — | Reference section; error-log monitoring | Manual review |
| DEP-10 | Resource sizing/capacity | None | Missing | M | — | Guidance + "measure, don't guess" | Manual review |
| DEP-11 | Staging vs production | None | Missing | H | — | Environment inventory template | Template review |
| DEP-12 | Release and rollback | None | Missing | C | Zero rollback guidance | `release-and-rollback.md`; patches are one-way | Template review |
| DEP-13 | Scheduled backups and retention | None | Missing | C | Zero backup guidance | Backup section + template | Template review |
| DEP-14 | Off-site backup storage | None | Missing | H | — | Template field + reference | Template review |
| DEP-15 | Restore drills with documented results | None | Missing | C | — | `backup-restore-test.md` requiring executed evidence | Template review |
| DEP-16 | DR objectives and incident response | None | Missing | H | — | RTO/RPO fields + incident template | Template review |
| DEP-17 | Upgrade planning and post-upgrade verification | Partial | Missing | H | Schema-change commands only | Upgrade section + compatibility ref | Manual review |

---

## F. Data migration (MIG)

| Requirement ID | Capability | Existing coverage | Coverage status | Severity | Evidence | Proposed change | Validation |
|---|---|---|---|---|---|---|---|
| MIG-01 | Source discovery and access constraints | None | Missing | H | — | New migration reference §1 | Manual review |
| MIG-02 | Source-data profiling | None | Missing | H | — | §2 + mapping template | Template review |
| MIG-03 | Duplicate detection and cleansing | None | Missing | H | — | §3 | Manual review |
| MIG-04 | Field mapping and transformations | None | Missing | H | — | `data-mapping.md` | Template review |
| MIG-05 | Parent-child and dependency handling | None | Missing | H | — | §4 | Manual review |
| MIG-06 | Master/transaction sequencing | None | Missing | H | — | §4 | Manual review |
| MIG-07 | Attachments and file migration | None | Missing | M | — | §5 + checksum verification | Manual review |
| MIG-08 | Reference integrity and naming rules | None | Missing | H | — | §6 + reconciliation queries | Manual review |
| MIG-09 | Import methods and performance | Partial | Missing | M | `bench data-import` not mentioned | §7 | Manual review |
| MIG-10 | Dry runs and repeatability | None | Missing | H | — | §8 + run log | Template review |
| MIG-11 | Error logs and rejected-record reports | None | Missing | H | — | §8 + run log fields | Template review |
| MIG-12 | Idempotency and safe retries | None | Missing | H | — | §8 | Manual review |
| MIG-13 | Cutover and rollback | None | Missing | H | — | Cutover checklist | Template review |
| MIG-14 | Financial/operational reconciliation | None | Missing | C | — | `migration-reconciliation.md` with counts, balances, stock, exceptions | Template review |

---

## G. Custom development and AI (DEV/AI)

| Requirement ID | Capability | Existing coverage | Coverage status | Severity | Evidence | Proposed change | Validation |
|---|---|---|---|---|---|---|---|
| DEV-01 | App boundaries and code ownership | Partial | Partial | M | Placement rules; no ownership discovery commands | Add to `SKILL.md` Step 0 | Checklist |
| DEV-02 | Lifecycle/hook selection | Complete | Complete | — | `server-patterns.md` hook list | Keep | — |
| DEV-03 | Transactions, concurrency, partial failure | None | Missing | H | No `savepoint`/`for_update`/retry guidance | Extend server patterns | Manual review |
| DEV-04 | REST APIs and external integrations | Partial | Partial | H | Whitelisted methods; no REST/auth/contract | Add integration section + security ref | Manual review |
| DEV-05 | Fixtures, patches, reproducible setup | Partial | Partial | M | Basic patches; no deployment parity | Extend hooks + deployment refs | Manual review |
| DEV-06 | Logging and observability | Partial | Partial | M | `log_error`/`logger` only | Add structured logging + correlation guidance | Manual review |
| DEV-07 | Version compatibility and upgrade safety | None | Missing | H | — | Compatibility ref + checklist | Link check |
| DEV-08 | No hardcoded app/site/prefix assumptions | None | Missing | M | Template asks for prefix but skill doesn't enforce | Add rule + project template fields | Review |
| AI-01 | Written use cases and acceptance criteria | None | Missing | H | — | New `ai-features.md` | Manual review |
| AI-02 | Tool/API access boundaries | None | Missing | H | — | §2 | Manual review |
| AI-03 | Authn/authz and least privilege for AI actions | None | Missing | C | — | §3 | Manual review |
| AI-04 | Input validation and output handling | None | Missing | H | — | §4 | Manual review |
| AI-05 | Prompt injection / untrusted content | None | Missing | C | — | §5 | Manual review |
| AI-06 | Sensitive-data minimization | None | Missing | H | — | §6 | Manual review |
| AI-07 | Human approval for consequential operations | None | Missing | C | — | §7 | Manual review |
| AI-08 | Audit logs and traceability | None | Missing | H | — | §8 | Manual review |
| AI-09 | Rate limits, cost, retries, timeouts, failure handling | None | Missing | H | — | §9 | Manual review |
| AI-10 | Evaluation datasets and regression testing | None | Missing | H | — | §10 + testing ref | Manual review |
| AI-11 | Monitoring, fallback, ownership | None | Missing | M | — | §11 | Manual review |

---

## H. Testing and QA (QA)

| Requirement ID | Capability | Existing coverage | Coverage status | Severity | Evidence | Proposed change | Validation |
|---|---|---|---|---|---|---|---|
| QA-01 | Unit tests | None | Missing | H | No test guidance; layout only | `testing-and-qa.md` with v16 test classes | Manual review |
| QA-02 | Integration tests | None | Missing | H | — | Same | Manual review |
| QA-03 | Permission/authorization tests | None | Missing | C | — | Same + security ref | Manual review |
| QA-04 | Workflow/business-rule tests | None | Missing | H | — | Same | Manual review |
| QA-05 | Regression tests | None | Missing | H | — | Regression checklist template | Template review |
| QA-06 | Migration tests and reconciliation | None | Missing | H | — | Migration ref §9 | Manual review |
| QA-07 | UI/branding verification | None | Missing | M | — | White-label verification template | Template review |
| QA-08 | API/integration failure scenarios | Partial | Partial | M | One exception example | Extend testing ref | Manual review |
| QA-09 | Background job/scheduler checks | Partial | Partial | M | `bench doctor` absent | Deployment + testing refs | Manual review |
| QA-10 | Deployment smoke tests | None | Missing | H | — | Runbook + release template | Template review |
| QA-11 | Backup/restore validation | None | Missing | C | — | `backup-restore-test.md` | Template review |
| QA-12 | Performance/security checks | Partial | Partial | M | Performance rules; no measurement | Add measurement + security checklist | Manual review |
| QA-13 | UAT | None | Missing | H | — | `uat-signoff.md` | Template review |
| QA-14 | Delivery test note with evidence | None | Missing | C | "Tell the user commands" only | `delivery-test-note.md` + evidence gate | Template review |

---

## I. Documentation, version control, support (DOC/SUP)

| Requirement ID | Capability | Existing coverage | Coverage status | Severity | Evidence | Proposed change | Validation |
|---|---|---|---|---|---|---|---|
| DOC-01 | Architecture and app boundaries | None | Missing | M | — | Technical design template | Template review |
| DOC-02 | Install/environment setup | Partial | Partial | M | Install is for the plugin, not client apps | Deployment runbook | Template review |
| DOC-03 | Configuration/customization inventories | None | Missing | H | — | `configuration-inventory.md` | Template review |
| DOC-04 | Integration contracts | None | Missing | M | — | Technical design section | Template review |
| DOC-05 | Migration mappings and reconciliation | None | Missing | H | — | Migration templates | Template review |
| DOC-06 | Deployment and rollback procedures | None | Missing | H | — | Deployment templates | Template review |
| DOC-07 | Backup/restore instructions | None | Missing | H | — | Backup template + runbook | Template review |
| DOC-08 | Troubleshooting and support procedures | None | Missing | H | — | Support reference + incident template | Template review |
| DOC-09 | Test evidence | None | Missing | C | — | Delivery test note | Template review |
| DOC-10 | Known limitations and technical debt | None | Missing | M | — | Handover template section | Template review |
| DOC-11 | Release notes/upgrade instructions | None | Missing | M | No changelog | Release template + CHANGELOG | File check |
| DOC-12 | Handover to another developer | None | Missing | H | — | `handover-checklist.md` | Template review |
| DOC-13 | Git remote/branch/worktree verification | None | Missing | M | — | `SKILL.md` Step 0 + CONTRIBUTING | Manual review |
| DOC-14 | Small commits, meaningful messages | None | Missing | M | — | CONTRIBUTING + PR template | Manual review |
| DOC-15 | No secrets/customer data in repo | None | Missing | C | — | Security ref + validator scan | Validator test |
| DOC-16 | Code review and CI checks | None | Missing | M | No CI | GitHub Actions validator | CI run |
| DOC-17 | Reproducible setup | Partial | Partial | M | Fixtures mentioned | Deployment + config inventory | Manual review |
| SUP-01 | Issue intake and reproduction | None | Missing | H | — | Support reference + incident template | Template review |
| SUP-02 | Severity/impact assessment | None | Missing | H | — | Severity matrix | Manual review |
| SUP-03 | Environment/version identification | None | Missing | H | — | Reference section | Manual review |
| SUP-04 | Log/trace inspection | Partial | Partial | M | `log_error` only | Reference section | Manual review |
| SUP-05 | Root-cause analysis | None | Missing | H | — | Incident template RCA fields | Template review |
| SUP-06 | Minimal corrective change | None | Missing | H | — | Reference section | Manual review |
| SUP-07 | Regression tests after fix | None | Missing | H | — | Reference + testing ref | Manual review |
| SUP-08 | Data integrity/security review | None | Missing | H | — | Reference section | Manual review |
| SUP-09 | Deployment/rollback considerations | None | Missing | H | — | Reference section | Manual review |
| SUP-10 | Client-facing incident summary | None | Missing | M | — | Template section | Template review |
| SUP-11 | Release notes/doc updates | None | Missing | M | — | Template section | Template review |
| SUP-12 | Follow-up monitoring | None | Missing | M | — | Template section | Template review |

---

## J. Security, privacy, licensing (SEC)

| Requirement ID | Capability | Existing coverage | Coverage status | Severity | Evidence | Proposed change | Validation |
|---|---|---|---|---|---|---|---|
| SEC-01 | Authentication/authorization model | Partial | Partial | H | `has_permission` one-liner | New `security.md` | Manual review |
| SEC-02 | Permission checks and data exposure | Partial | Partial | H | `get_list` vs `get_all`, permlevel sentence | Expand with `permlevel`, `only_for`, `permission_query_conditions` | Checklist |
| SEC-03 | SQL injection / unsafe SQL | Complete | Complete | — | Parameterised SQL + QB rules | Keep | Checklist |
| SEC-04 | Secret handling | None | Missing | C | — | Security ref + deployment ref + validator | Validator test |
| SEC-05 | File upload/access controls | None | Missing | H | — | Security ref | Manual review |
| SEC-06 | XSS/unsafe rendering | None | Missing | H | — | Security ref (Jinja, `|safe`, nh3/bleach) | Manual review |
| SEC-07 | API abuse/rate limiting | None | Missing | H | — | Security ref | Manual review |
| SEC-08 | Sensitive logging | None | Missing | M | — | Security ref | Manual review |
| SEC-09 | Dependency/supply chain | None | Missing | M | — | Security ref | Manual review |
| SEC-10 | Backup access/retention | None | Missing | H | — | Deployment ref | Manual review |
| SEC-11 | Tenant isolation | None | Missing | H | — | Security ref + white-label discovery | Manual review |
| SEC-12 | AI security/privacy | None | Missing | C | — | `ai-features.md` | Manual review |
| SEC-13 | Licenses, attribution, trademarks | None | Missing | H | — | Security ref + white-label ref | Manual review |

---

## K. Agent workflow and integration (AGT/REPO)

| Requirement ID | Capability | Existing coverage | Coverage status | Severity | Evidence | Proposed change | Validation |
|---|---|---|---|---|---|---|---|
| AGT-01 | Inspect before editing | Partial | Partial | H | Step 0 reads controller; no git/instructions | Rewrite Step 0 | Manual review |
| AGT-02 | Identify active versions | None | Missing | C | — | Detection protocol | Manual review |
| AGT-03 | Determine owning app/implementation | Complete | Complete | — | Placement decision tree | Keep | — |
| AGT-04 | Clarify missing requirements | None | Missing | H | — | Add stop-and-ask rule | Manual review |
| AGT-05 | Smallest safe implementation | None | Missing | M | — | Add rule | Manual review |
| AGT-06 | Identify affected files/regressions | None | Missing | H | — | Add workflow step | Manual review |
| AGT-07 | Implement | Complete | Complete | — | Existing skill | Keep | — |
| AGT-08 | Run tests/static checks | None | Missing | C | Only "tell the user" | Mandatory verification section | Manual review |
| AGT-09 | Review final diff | None | Missing | H | — | Add workflow step | Manual review |
| AGT-10 | Document evidence/limitations | Partial | Partial | H | "State where each change was made" | Expand to evidence + limitations | Manual review |
| AGT-11 | Never fabricate success | None | Missing | C | — | Explicit rule | Manual review |
| AGT-12 | Multi-agent compatibility documented honestly | Partial | Partial | M | Claude Code/claude.ai only | README + AGENTS.md; OpenCode paths cited | Link check |
| AGT-13 | Discoverability/routing for all capabilities | Incorrect | Incorrect | C | `description` covers only code standards | Rewrite `description` + routing table | Validator description length + review |
| REPO-01 | JSON/manifest validity | None | Missing | M | No checks | `scripts/validate_repo.py` | Run script |
| REPO-02 | Frontmatter validity (name/description/license) | None | Missing | M | No checks | Validator | Run script |
| REPO-03 | Relative link integrity | None | Missing | H | No checks | Validator | Run script + fault injection |
| REPO-04 | Reference/template inventory completeness | None | Missing | H | Orphans undetectable | Validator + index | Run script |
| REPO-05 | Unsupported version claim detection | None | Missing | C | `v15+` present | Validator banned phrases | Run script |
| REPO-06 | Secret scanning | None | Missing | H | — | Validator patterns | Fault injection |
| REPO-07 | CI on push/PR | None | Missing | M | No workflows | GitHub Actions workflow | CI run (repo host) |
| REPO-08 | Contribution/PR process | None | Missing | M | No CONTRIBUTING/PR template | Add both | Link check |
| REPO-09 | Release/versioning policy | Partial | Partial | L | "Bump version" only | CHANGELOG + policy | Link check |

---

## Coverage summary (baseline)

| Area | Complete | Partial | Missing | Incorrect | Total |
|---|---:|---:|---:|---:|---:|
| FUN | 9 | 5 | 0 | 0 | 14 |
| VER | 0 | 2 | 4 | 1 | 7 |
| WL | 0 | 3 | 14 | 0 | 17 |
| ERP | 0 | 5 | 7 | 0 | 12 |
| DEP | 0 | 1 | 16 | 0 | 17 |
| MIG | 0 | 1 | 13 | 0 | 14 |
| DEV/AI | 1 | 6 | 14 | 0 | 21 |
| QA | 0 | 3 | 11 | 0 | 14 |
| DOC/SUP | 0 | 3 | 21 | 0 | 24 |
| SEC | 1 | 3 | 9 | 0 | 13 |
| AGT/REPO | 2 | 5 | 15 | 1 | 23 |
| **Total** | **13** | **37** | **124** | **2** | **176** |

The 13 complete items are concentrated in core code placement and API usage — consistent with the
audit's conclusion that the repository is a good style guide with a large delivery-lifecycle gap.
