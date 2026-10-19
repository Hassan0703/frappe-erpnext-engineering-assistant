# Repository Audit — `frappe-code-standards`

> **Historical record (Phase 1/2).** This document describes the project under its original
> name, layout, and repository. It was renamed and independently rebranded in Phase 3; see
> `docs/audit/phase-3-release-audit.md`. Preserved as evidence, and exempt from the
> inherited-branding scan (see `NOTICE`). The development site/app name was redacted for
> publication; versions and results are unchanged.


**Audit date:** 2026-10-19
**Audited revision:** working copy supplied as `frappe-code-standards-main` (extracted archive)
**Auditor role:** principal Frappe/ERPNext architect, security reviewer, DevOps engineer, QA lead
**Scope of the audited product:** a Markdown-only Claude Code plugin containing one agent skill that
steers AI coding assistants toward conventional Frappe/ERPNext implementation patterns.

> **Evidence limitation.** The supplied directory contains **no `.git` directory**, so branch,
> commit history, authorship, tags, and provenance could not be inspected. `git status`,
> `git log`, and `git branch` all fail with "not a git repository". Findings below describe the
> files on disk only. No claim is made about history, reviews, or prior releases.

---

## 1. Executive summary

The repository is a small, well-written, single-purpose skill: **18 files, ~1,126 lines**, of which
~1,000 lines are instructional Markdown. Its strongest asset is a clear, opinionated point of view —
*working code in the wrong file is a defect* — expressed with concrete right/wrong examples. The
placement rules, `frappe.throw` discipline, translation rules, `set_query` placement, and N+1
guidance are technically sound and match how experienced Frappe developers work.

It is, however, **a Frappe coding-style guide, not the production engineering assistant the brief
requires**. Measured against Sections 5–12 of the brief:

| Capability area | Coverage in baseline |
|---|---|
| Code placement, core APIs, errors, translations | **Good** (the reason the repo exists) |
| Frappe v15 **and** v16 compatibility | **Missing / incorrect** (`SKILL.md:12` says "Assume Frappe v15+") |
| White-labeling and branding | **Missing** (zero matches for brand/logo/favicon/white-label) |
| ERP implementation lifecycle | **Missing** |
| Deployment, backup, restore, rollback | **Missing** (zero matches for backup/restore/deploy/rollback) |
| Data migration and reconciliation | **Missing** (one incidental use of the word "migrations") |
| Testing and QA | **Missing** (zero matches for `run-tests`, `IntegrationTestCase`) |
| Security and permissions depth | **Very thin** (one `permlevel` sentence, one decorator) |
| AI feature standards | **Missing** |
| Support and incident management | **Missing** |
| Repository validation / CI | **Missing** (no workflows, no scripts, no tests) |

The most consequential defects are not factual errors in the existing prose — the existing prose is
mostly accurate for v15 — but **scope and verification gaps**: the skill permits an unsupported
version range, never tells the agent to establish the project's actual versions, never requires the
agent to execute a test or command before claiming success, and has no guidance at all for the
majority of the delivery lifecycle the brief targets.

**Verdict:** preserve the existing core and its voice; extend it into a routed, version-aware,
evidence-driven engineering assistant. Do not rewrite from scratch.

---

## 2. Repository architecture and inventory

### 2.1 Structural inventory

| Component | Path | Purpose | Quality / notes |
|---|---|---|---|
| Marketplace manifest | `.claude-plugin/marketplace.json` | Declares marketplace `nextash`, one plugin, source `./plugins/frappe-code-standards` | Valid JSON; minimal but correct |
| Plugin manifest | `plugins/frappe-code-standards/.claude-plugin/plugin.json` | Name, display name, `1.0.5`, description, author, repo, MIT, keywords | Valid; no release notes/changelog |
| Plugin icon | `plugins/frappe-code-standards/.claude-plugin/icon.png` | Marketplace/plugin icon | Binary; not inspected |
| Skill entry point | `plugins/frappe-code-standards/skills/frappe-code-standards/SKILL.md` | Activation description + core rules | 88 lines; strong content, unsupported version claim |
| Reference: placement | `.../references/code-placement.md` | App layout, decision tree, child tables, wrong/right | 77 lines; accurate, slightly absolute |
| Reference: server | `.../references/server-patterns.md` | Controllers, errors, whitelisting, DB, QB, naming | 140 lines; best file in the repo; missing transaction/version depth |
| Reference: client | `.../references/client-patterns.md` | Form scripts, `set_query`, calls, dialogs | 111 lines; accurate for v15; no v16 note |
| Reference: hooks | `.../references/hooks-and-customization.md` | `hooks.py`, `doc_events`, fixtures, patches, settings, permissions | 88 lines; omits v16 `extend_doctype_class` and branding/privacy hooks |
| Reference: performance | `.../references/performance.md` | Queries, writes, jobs, client | 54 lines; good basics; no measurement method |
| Reference: reports/printing | `.../references/reports-and-printing.md` | Report types, script reports, print formats | 57 lines; v15-centric; v16 print regression risk |
| Reference: checklist | `.../references/review-checklist.md` | Pre-finish checklist | 28 lines; checks code style, not evidence |
| Root README | `README.md` | Marketing, install, before/after, layout | 179 lines; honest beta framing |
| Plugin README | `plugins/frappe-code-standards/README.md` | Short install/summary | Consistent with root |
| Project template | `templates/CLAUDE.md` | Project facts + skill activation | 17 lines; missing ERPNext version, commands, ownership detail |
| Issue templates | `.github/ISSUE_TEMPLATE/{bug_report,feature_request}.md` | Intake | Good bug template; asks for version |
| Licenses | `LICENSE`, `plugins/.../LICENSE` | MIT, NexTash, 2026 | Duplicate is acceptable; consistent |

### 2.2 Discovery and loading model

- Claude Code discovers the marketplace from `.claude-plugin/marketplace.json`, resolves the plugin
  from `source`, and auto-discovers skills under `skills/<name>/SKILL.md`.
- The skill is model-invoked: the `description` in YAML frontmatter is the only routing signal the
  agent sees before loading. All depth lives in `references/`, which is the correct
  progressive-disclosure pattern and should be preserved.
- `templates/CLAUDE.md` is a *copy-into-project* file, not auto-loaded by the plugin. The README
  correctly tells users to copy it into their project root.
- No hooks, commands, agents, MCP servers, or executable code are declared. The README's claim that
  the plugin "runs no scripts, makes no network calls and collects no data" is accurate for the
  packaged plugin **as it exists today**.

### 2.3 Dependencies and version requirements

- Runtime dependencies: none (Markdown only).
- Declared support: README badge `Frappe v15 | v16`; `SKILL.md:12` says `v15+`.
- No `package.json`, `pyproject.toml`, lockfile, CI, linter, or validation command exists in the
  repository root.

---

## 3. Existing strengths worth preserving

These should survive the upgrade unchanged in spirit:

1. **Placement-first framing.** "Working code in the wrong place is a defect" is the repo's
   differentiator and is correct. The placement table in `SKILL.md` and the decision tree in
   `code-placement.md` are the best parts of the product.
2. **Right/wrong examples.** Every rule has a concrete counter-example. This is what makes the
   guidance usable by an LLM; keep the format for all new references.
3. **Framework-native APIs.** `frappe.throw(_())`, `frappe.msgprint`, `frappe.qb`,
   `frappe.get_cached_value`, `frappe.enqueue`, `frm.set_query` in `setup` — all correct and
   idiomatic.
4. **Translation discipline.** `_()` / `__()` with `{0}` placeholders and no f-strings inside
   translation calls is accurate and frequently missed by generated code.
5. **N+1 and `fields=["*"]` guidance.** Correct, practical, and illustrated with a fix.
6. **The `templates/CLAUDE.md` idea.** Project facts in the repo root is the right mechanism; it
   only needs more facts and fewer prohibitions.
7. **Honest beta positioning.** The README does not overclaim. New material should keep that tone:
   label unverified claims rather than sounding authoritative.

---

## 4. Defects, contradictions, outdated practices, and gaps

Severity: **Critical** = causes wrong or unsafe output / violates the brief's hard scope;
**High** = major required capability absent; **Medium** = correctness or maintainability risk;
**Low** = polish or consistency.

### 4.1 Critical

**F-01 — Unsupported version range.**
`SKILL.md:12`: *"Assume Frappe v15+ unless the project shows otherwise."* The `+` implies v17 and
later, which the brief explicitly forbids, and it directly contradicts the README badge
(`v15 | v16`). It also tells the agent to *assume* instead of *verify*. There is no protocol for
detecting the Frappe or ERPNext version, and `templates/CLAUDE.md` captures only the Frappe major.
This is the single most dangerous line in the repository: version-blind guidance produces
copy-paste code that breaks on upgrade.

**F-02 — No verification or evidence discipline.**
`SKILL.md` "Finishing a task" instructs the agent to *tell the user which commands are needed* —
never to run them, never to run a test, never to inspect the diff, never to distinguish "I ran this"
from "this should work". The brief requires the opposite (§9.3, §10, §16.10). No reference mentions
`bench run-tests`, test classes, or evidence capture. An AI assistant operating under this skill can
plausibly report success without executing anything.

**F-03 — No project-inspection protocol.**
Step 0 identifies the owning app and reads existing files, which is good, but there is no
instruction to check working-tree state, read project instructions, identify installed apps,
confirm versions, or stop when requirements are ambiguous. There is also no boundary against
destructive or production operations, secrets handling, or unauthorized commits/pushes.

### 4.2 High — missing required capabilities

| ID | Capability | Evidence |
|---|---|---|
| **F-04** | White-labeling and branding | `grep -rniE "white.?label\|brand\|logo\|favicon\|rebrand"` over the skill returns **zero** matches. No discovery, surfaces, implementation methods, verification, or upgrade checklist. |
| **F-05** | Deployment and operations | Zero matches for `backup`, `restore`, `deploy`, `rollback`. No hosting, services, TLS, secrets, monitoring, retention, or restore drills. |
| **F-06** | Data migration and reconciliation | Only incidental: `SKILL.md:38` (patches as "migrations") and `code-placement.md:75` ("deployable"). No profiling, mapping, idempotency, cutover, or reconciliation. |
| **F-07** | Testing and QA | No `run-tests`, no test class conventions, no permission tests, no UAT, no delivery test note. `test_<doctype_snake>.py` appears only in the directory tree. |
| **F-08** | Security depth | One sentence ("Don't hide fields in JS … use permlevel") and one decorator. Missing: authorization on whitelisted methods beyond one line, `permlevel` mechanics, `permission_query_conditions`, XSS/Jinja escaping, file upload controls, secret storage, API auth, CSRF, dependency risk, privacy/`user_data_fields`. |
| **F-09** | ERP implementation lifecycle | Absent. No discovery, fit-gap, standard-vs-custom decision framework, workflow/permission matrices, configuration inventory, UAT, or handover. |
| **F-22** | Licensing/trademark for branding | Absent. Removing upstream branding has legal constraints that differ between the MIT framework and GPLv3 ERPNext; the repo is silent. |

### 4.3 Medium — correctness, maintainability, and agent behavior

**F-10 — No AI feature standards.** No prompt-injection, tool-boundary, human-approval, evaluation,
cost, or audit guidance, despite the brief requiring it.

**F-11 — No support/incident workflow.** No intake, severity, RCA, minimal-fix, regression, or
client-communication guidance. The skill stops at delivery.

**F-12 — No documentation/handover standards and no contribution infrastructure.** No
`CONTRIBUTING.md`, no PR template, no changelog, no release process beyond "bump `version`".

**F-13 — No validation of the repository itself.** Nothing checks JSON validity, frontmatter,
broken relative links, orphaned references, template inventory, or unsupported version claims.
A documentation product without link checks drifts silently — the target audience is exactly the
audience least likely to notice.

**F-14 — Project template is under-specified and over-restrictive.**
`templates/CLAUDE.md` says *"Do not use other skills for code in this repository unless I ask."*
This blocks legitimate skills (testing, security review, a client's own skill) and conflicts with
the new routing model. It captures Frappe version but not ERPNext version, installed apps beyond a
comment, test commands, deployment constraints, or verification expectations.

**F-15 — Repository URL casing is inconsistent.** Files use `NexTash/Frappe-Code-Standards`; the
brief names `NexTash/frappe-code-standards`. GitHub resolves case-insensitively, so installs work,
but canonical links and copy-paste commands should agree with the published repository name.

**F-16 — Absolute rules that are actually preferences.** The brief explicitly asks for this
distinction (§4.3). Examples:
- *"Never use Client Script / Server Script records"* — correct as a default because they are
  unversioned, but some delivery models (locked-down sites, no custom-app deployment) sanction them.
  The rule should be "discouraged; document and back up if unavoidable", not an absolute.
- *"No `doc_events` for DocTypes our app owns"* — a legitimate cross-cutting concern (audit trail,
  field-level history) may register `doc_events` for its own DocType. The real rule is "don't split
  one DocType's business logic across controller and hooks".
- *"Never `fields=["*"]` in production code"* — correct for request paths, but acceptable in
  one-off scripts, exports, and migration diagnostics. The rule should be contextual.

**F-17 — Server patterns lack transactional and concurrency guidance.** No `frappe.db.savepoint`,
`for_update`, retry/idempotency, `enqueue_after_commit` caveats (only mentioned once), or guidance on
partial failure in batch jobs.

**F-18 — Hooks reference omits v16-critical and branding-relevant hooks.** No
`extend_doctype_class` (v16+), `required_apps`, `never_skip_patches`, `app_logo_url`, `brand_html`,
`website_context`, `add_to_apps_screen`, `default_mail_footer`, `user_data_fields`.

**F-19 — Printing guidance is v15-centric and will mislead on v16.** v16 deprecates classic print
formats, moves PDF rendering to Chromium, and requires `bench setup-chrome` (or `chromium_path`) on
servers without internet. The reference recommends Jinja print formats (still valid for HTML) but
gives no migration or deployment warning.

**F-20 — Client guidance predates v16 UI changes.** No mention of `/desk` (v16 reroute from
`/app`), the deprecation of `/apps`, report/dashboard/page JS being evaluated as IIFEs, or the v16
list-view changes. None of these break existing code by themselves, but they change what "correct"
looks like, especially for list-view and report scripts.

**F-21 — Performance guidance lacks measurement.** It states rules but never says how to verify
them (`EXPLAIN`, `frappe.db.sql(..., debug=1)`, `bench --site x show-pending-jobs`, query timing,
index checks). The brief requires measured claims, not asserted ones.

**F-23 — Multi-agent support is undocumented.** The README documents Claude Code and claude.ai only.
The skill layout is portable: OpenCode discovers `.opencode/skills/<name>/SKILL.md`,
`.claude/skills/<name>/SKILL.md`, and `.agents/skills/<name>/SKILL.md`; the Agent Skills frontmatter
is the same format. No install path, no `AGENTS.md` template, and no honest statement of what is and
is not supported.

**F-24 — Versioning without a changelog.** `plugin.json` is `1.0.5`; the README instructs
contributors to bump it. There is no `CHANGELOG.md` and no compatibility policy tying skill versions
to Frappe versions.

**F-26 — Layout reference is incomplete for modern apps.** No mention of `extend_doctype_class`
extension modules, `services/`, `tests/`, `templates/emails/`, or where branding assets belong.

### 4.4 Low

**F-25 — No "stop and ask" rule.** The agent is never told to halt on ambiguous requirements that
affect correctness, nor to state unverified assumptions explicitly.

**F-27 — README/marketplace duplication.** Root README, plugin README, marketplace description, and
plugin description repeat the same sentence. Acceptable but should stay in sync; the validator
should check that the plugin source path exists and metadata parses.

**F-28 — No `SECURITY.md`.** For a repo whose guidance includes security rules and whose issue
templates invite public reports, a reporting path for vulnerabilities is missing.

---

## 5. White-labeling capability assessment

**Current state: absent.** Not "thin" — absent. A user asking "rebrand this ERPNext for a client"
would receive no guidance from this repository, and the skill's `description` would not even
activate for the task.

What the brief requires versus what exists:

| Surface | Required | Exists | Risk if unaddressed |
|---|---|---|---|
| Discovery and scope | Yes | No | Branding done piecemeal; missed surfaces found in UAT |
| Desk/navbar/login branding | Yes | No | Inconsistent identity at the most visible point |
| Website/portal identity | Yes | No | Client sees upstream brand on public pages |
| Email and notifications | Yes | No | Transactional email carries the wrong brand |
| Print/PDF output | Yes | No | Invoices and POs go to customers with mixed branding |
| Terminology/translations | Yes | No | v15 CSV vs v16 Gettext trap |
| Upgrade safety classification | Yes | No | Core edits presented as "fine because it works locally" |
| Verification after migrate/build | Yes | No | Assets silently revert on upgrade |
| Legal/trademark boundary | Yes | No | GPL/MIT/trademark confusion; unsupported claims |

The technical surface list is large and version-sensitive, which is exactly why it needs its own
reference and four templates rather than a paragraph in `SKILL.md`.

---

## 6. v15/v16 compatibility assessment

The baseline asserts a single version and contains no version-difference documentation. Verified
differences that materially affect the existing guidance (sources in §11):

| Area | v15 | v16 | Impact on this repo |
|---|---|---|---|
| Runtime | Python/Node per v15 | **Python 3.14+, Node 24+** | Deployment guidance must branch |
| `frappe.get_all` / `get_list` fields | Raw SQL strings in `fields` tolerated | **Strict parsing**; function strings break | Existing `reports`/`performance` examples are v15-safe; must warn |
| Default sort | Implicitly `modified desc` | **`creation desc`** | Reports/jobs relying on order silently change |
| `frappe.db.commit()` in doc hooks | Discouraged, possible | **Blocked** | The repo already says don't commit; now it is enforced |
| `override_doctype_class` | Replaces class | **Must subclass** the overridden class | Existing text says "subclass … call `super()`" — good, now mandatory |
| Class extension | `override_doctype_class` only | **`extend_doctype_class` added** | New hook belongs in placement/hooks references |
| `has_permission` hook | `None` tolerated as allow | **Must return explicit `True`** | Security guidance must state this |
| Print formats | Classic + HTML | **Classic deprecated**, Print Format Editor, Chromium PDFs | Printing reference needs a migration section |
| PDF engine | wkhtmltopdf | Chromium; `bench setup-chrome`, `chromium_path`; wkhtmltopdf removed in v17 | Deployment runbook needs a PDF step |
| Translations | CSV | **Gettext PO/MO** | White-label terminology workflow differs |
| Tests | `frappe.tests.utils.FrappeTestCase` | **`frappe.tests.IntegrationTestCase` / `UnitTestCase`**; `frappe.in_test` | Testing reference must not teach the deprecated class |
| Desk route | `/app` | **`/desk`**; `/apps` deprecated; persistent sidebar/desktop | Client docs, branding screenshots, redirects |
| Report/page JS | Inline global script | **IIFE** | Report JS must not rely on globals |
| `db.get_value` on Singles | Strings | **Type-cast values** | Validation code comparing to `"1"` breaks |
| HTML sanitization | bleach | **nh3** (strips forbidden tags) | XSS guidance and dependency notes |
| `sendmail(now=True)` | Committed implicitly | **Does not commit** | Notification/migration workflows |
| Single DocType / `get_doc` quirks | legacy behavior | `get_doc(..., field=value)` no longer mutates; `value_cache` shape changed | Advanced code review items |

Also verified: `bench version` output format changed (plain vs legacy), and translation and metadata
hooks were removed/changed (`get_translated_dict`, `frappe.get_lang_dict`).

**Assessment:** the baseline is effectively a v15 guide wearing a "v15+" label. Nothing in it is
*false* for v15, but several recommendations become wrong or incomplete on v16. This must be fixed
with an explicit compatibility matrix and a detection protocol, not by sprinkling "v16" into prose.

---

## 7. Security and operational-risk assessment

### 7.1 Guidance risks

| Risk | Where | Consequence |
|---|---|---|
| Permission checks presented as one line | `SKILL.md` security bullet, `server-patterns.md` | Agent may treat `frappe.whitelist()` as authenticated-and-authorized; it is not |
| No file-upload guidance | absent | Unrestricted extensions/MIME, public files, path traversal |
| No XSS/Jinja guidance | absent | `|safe` on user content, unescaped print formats |
| No secret-handling rule | absent | Keys pasted into `site_config.json` committed to Git, or into chat |
| No production boundary | absent | Agent may propose destructive DB edits or production commands |
| `ignore_permissions=True` guidance only says "add a comment" | `server-patterns.md` | Comment is not a control; no `frappe.only_for` / role check |
| API auth unaddressed | absent | Token/API-key handling, CSRF, guest endpoints |
| No privacy lifecycle guidance | absent | `user_data_fields`, retention, PII in logs |

### 7.2 Repository-own risks

- No CI or link validation, so a broken reference link is invisible until an agent tries to open it.
- No `SECURITY.md`, despite inviting issue reports.
- No automated check for secrets or customer data in commits.
- The plugin itself is inert Markdown, which is a genuine security strength; new artifacts must not
  introduce runtime network calls or bundled binaries.

### 7.3 Licensing risk for white-labeling

Verified: **Frappe Framework is MIT**, **ERPNext is GPLv3**, ERPNext documentation is CC-BY-SA-3.0,
and Frappe publishes a Logo and Trademark Policy. The repository currently gives no guidance on:
attribution preservation, GPL obligations when distributing modified ERPNext, or the difference
between removing a visible logo and removing copyright notices. This is a material gap for the
white-label use case and must be framed as *questions for counsel*, never as legal advice.

---

## 8. Coding-agent integration assessment

| Agent | Mechanism | Baseline support | Honest assessment |
|---|---|---|---|
| Claude Code | Marketplace + plugin + `skills/` | **Native, documented** | Works as designed; marketplace name `nextash`, install command consistent |
| claude.ai | Zip the skill folder | **Documented** | Works if the zip contains `SKILL.md` at the skill root |
| OpenCode | `.opencode/skills/<name>/SKILL.md`, `.claude/skills/...`, `.agents/skills/...` | **Undocumented but portable** | Same frontmatter contract; install = copy/symlink the skill directory. Not tested here |
| Cline / other Agent Skills hosts | `SKILL.md` | **Undocumented** | Portable in principle; discovery paths differ. Must be described as "adaptation required", not "supported" |
| Generic agents | `AGENTS.md` | **Missing** | No agent-neutral project template exists |

The skill's frontmatter (`name`, `description`) is valid Agent Skills. Adding `license` is portable.
No custom top-level keys should be introduced. Multi-agent claims must be precise: "portable skill,
Claude Code packaging; other agents require copying the skill folder into their discovery path."

---

## 9. Prioritized recommendations

Ordered exactly as the brief's Phase K priority list. Full task breakdown and validation live in
`implementation-roadmap.md`.

1. **Fix critical errors and misleading instructions.**
   Replace "v15+" with an explicit v15/v16-only scope and a verification-first detection protocol;
   add the inspect → clarify → smallest-change → verify workflow; add non-negotiable boundaries
   (no production mutation, no secrets, no unrequested commits); require executed evidence before
   claiming completion.
2. **Add foundational capabilities.**
   Version compatibility reference; security reference; testing reference; support/incident
   reference; expand the review checklist into a gate.
3. **White-labeling architecture and workflows.**
   One reference covering discovery, surfaces, safe-change classification, version differences,
   verification, upgrade implications, and legal boundaries; four templates.
4. **v15/v16 compatibility and verification.**
   Detection commands; difference matrix with sources and confidence; annotate every version-sensitive
   rule in existing references.
5. **Deployment, migration, testing, and operational reliability.**
   Deployment/ops reference; migration reference with reconciliation; five ops templates and five
   migration templates.
6. **Documentation, handover, and support.**
   ERP implementation reference; requirements/fit-gap/design/permissions/config/UAT templates;
   handover and delivery test notes; contribution and PR infrastructure.
7. **Agent integration, discoverability, and usability.**
   Rewrite the skill `description` to activate on branding/deployment/migration/testing tasks; add
   a routing table; add `AGENTS.md`; document OpenCode/Cline paths honestly.
8. **Polish.**
   Link checks, template index, changelog, README refresh, metadata bump.

---

## 10. Requirement → proposed file → validation mapping

Stable IDs are defined in `requirements-traceability.md`. Summary of where each class of requirement
will live after implementation:

| Requirement class | Primary artifact | Validation |
|---|---|---|
| VER (version scope/detection) | `references/version-compatibility.md`, `SKILL.md` | Forbidden-phrase scan; matrix reviewed against cited sources |
| WL (white-label) | `references/white-labeling.md`, 4 templates | Every surface has method + verification; template link check |
| ERP (implementation) | `references/erp-implementation.md`, 6 templates | Template inventory check; standard-first rule present |
| DEP (deployment/ops) | `references/deployment-and-operations.md`, 5 templates | Restore-drill requirement present; commands marked verify-first |
| MIG (migration) | `references/data-migration.md`, 5 templates | Reconciliation fields present; no "no errors = success" claim |
| DEV (custom dev/API) | existing references + `references/security.md` | Existing tests preserved; link check |
| AI (AI features) | `references/ai-features.md` | Prompt-injection and human-approval sections present |
| QA (testing) | `references/testing-and-qa.md`, 5 templates | Test classes match v16; evidence fields present |
| SEC (security/privacy/licensing) | `references/security.md` | Checklist covers authz, SQL, XSS, upload, secrets, privacy, license |
| SUP (support) | `references/support-and-incidents.md`, `incident-report.md` | Severity + RCA + rollback fields present |
| AGT (agent workflow) | `SKILL.md`, `templates/CLAUDE.md`, `templates/AGENTS.md` | Workflow steps 1–10 present; evidence rule present |
| REPO (repo validation) | `scripts/validate_repo.py`, CI workflow | Script exits non-zero on injected fault (manually tested) |

---

## 11. Verification status and sources

### Verified by direct inspection of this repository

All 18 files were read in full. Line-level claims above (e.g. `SKILL.md:12`) come from those reads.
Zero-match claims come from the `grep` runs recorded during the audit.

### Verified against upstream sources (as of 2026-10-19)

- Frappe v16 migration wiki: `github.com/frappe/frappe/wiki/Migrating-to-version-16`
- Query Builder refactor wiki: `github.com/frappe/frappe/wiki/query-builder-migration`
- Frappe hooks documentation: `docs.frappe.io/framework/user/en/python-api/hooks`
- Frappe Query Builder documentation: `docs.frappe.io/framework/user/en/api/query-builder`
- Frappe PDF generation documentation: `docs.frappe.io/framework/user/en/printing/pdf-generation`
- Frappe bench command documentation: `docs.frappe.io/framework/user/en/bench/frappe-commands`
- Apps page / `add_to_apps_screen`: `docs.frappe.io/framework/user/en/apps-page`
- OpenCode Agent Skills discovery: `opencode.ai/docs/skills`
- Licensing: `docs.frappe.io/legal/others/license-and-trademark`, `erpnext.com/license-trademark`,
  `github.com/frappe/erpnext` (README links the Logo and Trademark Policy)

### Explicitly unverified (do not treat as fact)

1. Exact branding fieldnames in `Website Settings` and `Navbar Settings` for v15 vs v16. The
   `Website Settings` docs page was too large to retrieve reliably; the references instruct the agent
   to read the installed DocType JSON instead of hardcoding fieldnames.
2. Whether `export-fixtures` handles Single DocTypes (e.g. `Website Settings`) reproducibly. Treated
   as unverified; the guidance recommends a patch/`after_install` with `frappe.db.set_single_value`
   and verification.
3. Whether the Claude Code marketplace auto-update flow behaves exactly as the README claims.
4. Exact `bench` flag availability on every v15/v16 patch release (`--with-files`,
   `--with-private-files`, `restore` variants). All such commands are presented as
   "confirm with `--help` on the target bench".
5. Whether every third-party agent (Cline, Cursor, etc.) discovers `SKILL.md` identically. Only
   OpenCode's documented paths are cited.
6. Production behaviour of any client system. No client environment was accessed for this audit.

### Not performed

- No execution of `bench` commands (no Frappe bench in this environment).
- No git history, branch, or diff review (no `.git` directory).
- No security scanning of dependencies (none exist).
- No legal review.

---

## 12. Post-implementation status

The findings above were addressed in the same working copy. Task-level status and the executed
validation are in `implementation-roadmap.md`; this section records the outcome and the residual
gaps, so the audit is not left implying the baseline defects still exist.

### What changed

| Finding | Resolution |
|---|---|
| F-01 unsupported version range | `SKILL.md` states v15/v16 only, requires version detection, and the validator fails on `v15+`-style ranges |
| F-02 no verification discipline | Workflow requires executed evidence, diff review, and an explicit "not verified" list; review checklist enforces it |
| F-03 no inspection protocol | Step 0 covers git state, project instructions, version detection, owning app, existing code, tests |
| F-04 white-labeling absent | `white-labeling.md` + 4 templates covering discovery → verification → upgrade |
| F-05 deployment absent | `deployment-and-operations.md` + 5 templates, including a mandatory restore drill |
| F-06 migration absent | `data-migration.md` + 5 templates; "no import errors" explicitly rejected as success |
| F-07 testing absent | `testing-and-qa.md` + 5 templates with v16 test classes and evidence fields |
| F-08 security thin | `security.md` covering authorization layers, injection, XSS, uploads, secrets, tenancy, privacy, licensing |
| F-09 ERP lifecycle absent | `erp-implementation.md` + 6 templates with a standard-first decision order |
| F-10 AI standards absent | `ai-features.md` |
| F-11 support absent | `support-and-incidents.md` + incident/defect templates |
| F-12 docs/contribution absent | CONTRIBUTING, PR template, CHANGELOG, SECURITY |
| F-13 no validation | `validate_repo.py`, `sync_templates.py`, CI workflow |
| F-14 template weak | `templates/CLAUDE.md` expanded; `templates/AGENTS.md` added |
| F-15 URL casing | standardised on `NexTash/frappe-code-standards` |
| F-16 absolutist rules | softened with the conditions where the discouraged approach is acceptable |
| F-17…F-28 | addressed in the corresponding references and metadata |

### Residual gaps (still true after this work)

1. Version differences are documented from upstream sources, not verified against every patch release.
2. Branding field names are described by purpose; the agent must confirm `fieldname`s in the installed
   DocType JSON.
3. Fixture behaviour for Single DocTypes remains **Unverified**.
4. No `bench` command, live site, or client environment was exercised here; every operational claim is
   guidance, not a tested result on a real deployment.
5. Only Claude Code packaging is tested; other agents rely on the portable `SKILL.md` format.
6. No legal review of licensing/trademark questions.
7. No git history/branch exists, so no commit-level review was possible.

### Final scorecard

Scored against the brief's acceptance criteria, using delivered artifacts and executed checks — not
file existence alone.

| Category | Score | Evidence | Remaining gap |
|---|---:|---|---|
| Frappe/ERPNext engineering | 4/5 | Placement, server/client, hooks, performance, reports rewritten with verified version behavior | Patch-level verification not performed |
| White-labeling | 4/5 | Full lifecycle reference + 4 templates + legal boundary | Exact settings fieldnames unverified per version |
| ERP implementation | 3/5 | Discovery, fit-gap, design, permissions/SoD, UAT, handover | Methodology-level; no ERPNext-specific module deep dive |
| Deployment and operations | 4/5 | Runbook, env inventory, backup/restore test, release/rollback, monitoring, v16 Chromium | Commands marked verify-first; nothing executed on a real bench |
| Data migration | 4/5 | Profiling → mapping → idempotency → reconciliation → cutover, with templates | No executed migration |
| Security | 4/5 | Authorization, injection, XSS, uploads, secrets, privacy, tenancy, licensing, secret scan in CI | No third-party security review |
| Testing and QA | 4/5 | Layers, v16 test classes, permission/job/failure tests, delivery note, UAT | Plugin itself has structural validation only |
| Documentation and handover | 4/5 | Handover checklist, configuration inventory, contribution/PR/CI, changelog | No client-facing rendered docs |
| Version control | 2/5 | Git state checks and commit discipline in the workflow; PR template and CI | No `.git` here; no commit, branch, or push performed |
| Support and maintenance | 4/5 | Intake, severity, RCA, minimal fix, regression, communication, follow-up | Not exercised on a live incident |
| v15/v16 compatibility | 4/5 | Sourced difference matrix with confidence labels; phrasing enforced by the validator | Not every patch release covered |
| AI coding-agent usability | 4/5 | Rewritten scope/workflow/routing; description covers all capabilities; AGENTS.md; honest multi-agent docs | Only Claude Code packaging tested |

**Average: 3.75 / 5.** The limiting factors are environmental (no bench, no git, no client site) rather
than missing artifacts; those limits are stated rather than papered over.

> **Phase 2 (independent review).** This audit is a record of the baseline and the implementation
> claims as of 2026-10-19. It was independently re-reviewed afterwards; the corrections and the
> evidence (including runtime verification against Frappe 16.52.0) are in
> `docs/audit/phase-2-technical-findings.md`, `phase-2-compatibility-matrix.md`,
> `phase-2-agent-evaluation.md`, and `phase-2-final-report.md`.
