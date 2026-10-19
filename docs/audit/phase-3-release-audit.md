# Phase 3 Release Audit — Frappe ERPNext Engineering Assistant

**Date:** 2026-10-19
**Auditor:** implementation agent (release engineering), working from the Phase 2 audit evidence
**Subject:** independent rebrand and publication of the repository formerly published as
`frappe-code-standards`
**Release candidate:** `2.0.0-beta.1`
**Decision:** **PUBLISHED — PREVIEW** (identifiers in `docs/audit/phase-3-publication-record.md`)

> This audit records what was done and what was actually verified in Phase 3. Phase 1/2 documents
> remain historical records of the project under its previous name; they were not rewritten. Their
> findings, test evidence, and environment limitations are preserved.

## 1. Scope

Phase 3 covered five things:

1. Rebrand the working copy as an independent product with a new name, identity, packaging, and
   documentation.
2. Add capabilities the Phase 2 review identified as missing, without adding documentation volume for
   its own sake.
3. Revalidate the highest-risk technical guidance against the installed v15 and v16 source.
4. Run the full repository gate set, including the validator, template sync, the test suite, manifest
   and syntax parsing, secret/branding/path scans, and link checks.
5. Create and publish a new public GitHub repository, then verify the pushed content and CI.

Out of scope, and stated as such: a v15/v16 runtime bench provisioned for destructive framework tests,
live agent evaluation, legal review, and any change to the upstream repository.

## 2. Identity decision

| Item | Value |
|---|---|
| Product name | Frappe ERPNext Engineering Assistant |
| Skill name | `frappe-erpnext-engineering-assistant` |
| Marketplace name | `frappe-erpnext-assistant` |
| Repository | `frappe-erpnext-engineering-assistant` |
| Visibility | Public |
| Version | `2.0.0-beta.1` |

Before the rebrand, the intended name was checked on the authenticated account: no repository with
that name existed, and no similarly named project with the same purpose was found in the account.
The old marketplace and plugin identifiers were not reused, so the rename is unambiguous.

The repository was prepared from the local working copy only. The upstream project was not modified,
and no upstream history was imported; carrying the original commit history into a new repository
would misrepresent authorship of the derivative work. Provenance is recorded in `NOTICE` instead.

## 3. Rebranding inventory

| Area | What changed |
|---|---|
| Product identity | Name, tagline, descriptions, and audience across README, plugin README, manifests |
| Skill and plugin names | Directory, frontmatter `name`, manifest `name`, marketplace entry, project templates |
| Marketplace | New marketplace identifier and owner; single plugin entry; no duplicate listing |
| Author metadata | `author`, `homepage`, `repository` now point at the publishing account and repository |
| Repository URLs | Install commands, documentation links, issue links, contribution links |
| Icons | Inherited 1024×1024 icon replaced with a neutral generated mark |
| Project templates | `templates/CLAUDE.md`, `templates/AGENTS.md`: new skill name, install table, brand-neutral field prefix |
| Issue and PR templates | Rebranded, made agent-neutral, and corrected to request version/evidence data |
| CI | Workflow paths updated to the new plugin directory; unchanged job structure |
| Documentation | Root README rewritten; template index, contributing, security, changelog updated |
| Audit documents | Dated historical-record banner added to each Phase 1/2 document (Phase 3 links here) |
| Licence and attribution | `LICENSE` and plugin `LICENSE` unchanged; `NOTICE` added at root and inside the plugin |

Every occurrence of the inherited organisation name, old product slug, and inherited author credit
was inspected individually. The remaining occurrences are one of: the MIT copyright line (legally
required), the provenance statement in `NOTICE`, the changelog's rename record, the historical audit
documents, the validator's own pattern list, or exact removal commands in the upgrade instructions.
A blind global replacement was not performed.

## 4. Licensing and attribution position

- The project is MIT licensed; the original copyright notice and permission text are preserved
  unchanged in both licence files.
- `NOTICE` states that this is an independent rebranded derivative, names the original project and
  copyright holder, and lists the substantive changes made in the derivative.
- The changelog records the rename so the relationship is discoverable without reading Git history.
- No private company assets, client data, credentials, or confidential material were found or copied.
- Frappe and ERPNext are used descriptively. No upstream trademark or endorsement is claimed. ERPNext
  is GPLv3 and Frappe Framework is MIT; the white-labeling reference states that boundary and refers
  licensing questions to qualified counsel.
- **No licensing blocker was identified.** The MIT terms permit rebranding and redistribution provided
  the copyright and permission notice are retained, which they are.

## 5. Feature inventory

The shipped product is a Markdown skill plus its packaging. It runs no code at runtime.

**Entry point:** `SKILL.md` — scope, non-negotiables, six-step workflow, reference routing, evidence
levels, completion-report format, boundaries.

**16 references:** code placement, server patterns, client patterns, hooks and customization,
performance, reports and printing, version compatibility, white-labeling, ERP implementation,
deployment and operations, data migration, testing and QA, security, AI features, support and
incidents, review checklist.

**26 client templates:** discovery (1), white-label (4), ERP implementation (6), deployment and
operations (5), data migration (5), testing/QA/handover (5). Canonical copies in `docs/templates/`,
byte-identical bundled copies inside the skill.

**Capabilities added or completed in Phase 3:**

1. Project discovery and technical audit checklist (new template).
2. Production change risk classification: four classes with backup, approval, window, and rollback
   expectations (deployment reference).
3. Unified evidence scale: runtime-verified, source-verified, documentation-verified, unverified —
   defined in the version reference and used in the README.
4. White-labeling decision tree, surface inventory, verification procedure, and upgrade checklist,
   now indexed as first-class templates.
5. Change-planning step in the workflow: mechanism order, files, regression surface, risk class.
6. Evidence-gated verification step with a minimum-verification table per change type.
7. Completion report format for AI-generated changes.
8. Validator extensions: branding scan with per-line context handling, template inventory, reference
   routing, version-phrasing checks, secret and local-path scans.
9. 28 automated tests for the validator, including failing-case coverage.
10. Release audit, release checklist, release notes, NOTICE, and publication record.

Existing working capabilities were not duplicated. No new reference file was created for a single
rule; new material went into the reference that owns the topic.

## 6. Technical revalidation

Phase 2 verified claims against Frappe 16.52.0 / ERPNext 16.51.1. Phase 3 re-checked the highest-risk
white-labeling and version claims against two installed benches available at review time:

| Environment | Version | Use |
|---|---|---|
| Local v15 bench | Frappe 15.94.1 (`version-15`) | Read-only source inspection |
| Local v16 bench | Frappe 16.16.0 (`version-16`) | Read-only source inspection |

No command that mutates a site, database, asset bundle, or service was run on either bench.

| Claim checked | Result |
|---|---|
| `app_include_css`, `app_include_js`, `web_include_css`, `web_include_js` exist as hooks | Confirmed in both versions |
| `app_logo_url` is a core hook and feeds the desk logo | Confirmed in both versions (`hooks.py`, `boot.py`, Navbar Settings) |
| `add_to_apps_screen` supports `name`, `logo`, `title`, `route`, `has_permission` | Confirmed — v15 `apps.py` reads the entry and calls `has_permission`; v16 defines a core entry |
| `app_icon` / `app_color` are consumed by Frappe core for the app tile | **Not consumed.** Both are declared by ERPNext, but core 15.94 and 16.16 do not read them for the tile — corrected in two references |
| Navbar Settings exposes `app_logo` | Confirmed in both versions |
| Website Settings exposes `app_name`, `app_logo`, `brand_html`, `favicon`, `banner_image`, `splash_image`, `footer_logo`, `home_page`, `route_redirects`, `footer_powered` | Confirmed in both versions |
| `website_context` hook values reach the render context (including `favicon`) | Confirmed — merged in `website_settings.py` |
| `default_mail_footer`, `get_sender_details`, `override_email_send` exist | Confirmed in both versions |
| `portal_menu_items`, `standard_portal_menu_items`, `base_template`, `base_template_map`, `website_route_rules`, `website_redirects`, `role_home_page`, `get_website_user_home_page`, `webform_include_css` exist | Confirmed in both versions |
| A custom app can override the 404 page via `www/404.html` | Confirmed — not-found renderer resolves path `404`, and `www/404.html` exists in core |
| `get_translated_dict` was removed in v16 | **Deprecated, not removed.** v16.16 keeps a shim in `deprecation_dumpster.py` with removal slated for v17 — corrected |
| Login template is `apps/frappe/frappe/www/login.html` | Confirmed in both versions |

Two claims were corrected as a result (see §7). Both were already hedged in the guidance, but the
wording now matches the source instead of the earlier assumption.

## 7. Corrections made in Phase 3

| File | Correction | Evidence |
|---|---|---|
| `references/white-labeling.md` | App icon/colour row: `app_icon` and `app_color` are legacy ERPNext hooks not read by Frappe core 15.94/16.16; use `add_to_apps_screen` (`logo`) and `app_logo_url` | Source, both benches |
| `references/hooks-and-customization.md` | Same correction in the metadata hook table; version-support column set to source-verified | Source, both benches |
| `references/white-labeling.md` | `get_translated_dict`: described as a v16 deprecation shim (removal slated for v17), not a removal | `deprecation_dumpster.py`, 16.16.0 |
| `references/version-compatibility.md` | Translation row updated to match, with the shim and removal target | Same |
| `references/version-compatibility.md` | Added the mapping between the matrix's internal labels and the project-wide evidence scale | Consistency with README and audit |
| `scripts/validate_repo.py` | Branding scan is now line-based and allows removal/rename/upgrade context, so exact upgrade commands can name the old plugin | Needed for honest upgrade instructions |
| `scripts/tests/test_validate_repo.py` | Added the removal-instruction case; updated the version-mismatch fixture to the current version | Test suite follows the validator |

No guidance was deleted to remove a contradiction. No test was skipped or weakened.

## 8. Release gates executed

Run from the repository root on 2026-10-19. Exit status was captured for every command.

| Gate | Command | Result |
|---|---|---|
| Structure, links, inventory, phrasing, secrets, branding, local paths | `python3 scripts/validate_repo.py` | **Passed** — 88 Markdown files, 16 references, 26 templates, 0 errors, 0 warnings |
| Bundled template parity | `python3 scripts/sync_templates.py --check` | **Passed** — up to date (26 files) |
| Validator test suite | `python3 -m unittest discover -s scripts/tests -p "test_*.py"` | **Passed** — 28 tests, OK |
| Manifest JSON parsing | `json.load` on both manifests | **Passed** |
| Workflow YAML parsing | `yaml.safe_load` | **Passed** — 1 job, 5 steps |
| Python syntax | `python3 -m py_compile` on all three scripts | **Passed** |
| Conflict markers | repository-wide scan | **Passed** — none |
| Secret scan | validator patterns | **Passed** — no findings |
| Branding scan | validator, including the new plugin slug and author credit | **Passed** — no findings outside the documented exemptions |
| Local path / machine artifact scan | validator plus manual review of the tree | **Passed** — no developer home paths or bench names in shipped files |
| External links | HTTP status check of canonical URLs | **Passed** for the third-party canonical links; the new repository URLs were expected to 404 before publication and were re-checked afterwards (see the publication record) |
| Git whitespace | `git diff --check` after staging | **Passed** — see the publication record |
| Runtime v16 | Read-only source inspection only | **Not run** — no disposable bench was mutated |
| Runtime v15 | Read-only source inspection on 15.94.1 | **Partial** — source verified, not executed |
| GitHub Actions | `validate` on the new repository | **Passed** — run 39230198197, 15 s; checkout, validator, template sync, tests, and manifest parsing all succeeded |
| Live agent evaluation | Not run | **Not run** — no independent harness |

## 9. What is not verified

- v15 behaviour was read from source, not executed. No v15 site was used.
- Scheduler, worker, queue, email delivery, and PDF rendering remain unexercised.
- GitHub Actions passed on the pushed commit; it validates repository structure, not framework runtime behaviour.
- The five agent-evaluation scenarios were not executed. The rubric and scenarios remain in
  `phase-2-agent-evaluation.md`, and no scenario is claimed as passed.
- Exact branding fieldnames still vary by patch level; the guidance requires reading the installed
  DocType JSON, and that remains the correct instruction.
- Single DocType fixture round-tripping and per-patch PWA support remain unverified.
- No legal review was performed. The licensing position in §4 is a factual statement about the
  licences, not a legal opinion.

## 10. Version and positioning

`2.0.0-beta.1` is a **preview**, not a stable release:

- The identity, packaging, documentation, validator, and test suite are complete and pass locally.
- Runtime evidence exists only for the specific claims recorded in the Phase 2 matrix and the
  source-level checks above.
- CI was executed after publication and passed; it is a structural check, not a runtime or agent test.
- No independent user or agent evaluation has been completed.

A preview label is the honest description of that state. The product is usable today, and the
limitations are stated in the README rather than hidden behind a stable version number.

## 11. Publication

The repository was created under the authenticated account `Hassan0703`, public, default branch
`main`, from the local working copy. The initial commit is
`f1c058006cd3f85c4f2922293344119605e301e9` (105 files). The remote `main`, the GitHub tree, the README
render, and the CI run were verified after the push. Details:
[`phase-3-publication-record.md`](phase-3-publication-record.md).

## 12. Remaining work

1. Execute the five evaluation scenarios against a real agent and score them with the existing rubric.
2. Provision disposable v15/v16 benches and run the behaviour checks in the Phase 2 matrix,
   especially scheduler, email, PDF, and upgrade.
3. Re-run the white-labeling verification on a real client site and attach the completed checklists.
4. Re-check branding fieldnames on each patch level the project claims to support.
5. Add a CI matrix if a v15/v16 runtime job is ever justified; the current workflow is structural.
