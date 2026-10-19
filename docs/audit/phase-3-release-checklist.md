# Phase 3 Release Checklist

**Release:** `2.0.0-beta.1` — Frappe ERPNext Engineering Assistant
**Date:** 2026-10-19
**Rule:** a box is checked only when the check was executed and observed. "Not run" and "Blocked" are
recorded as they are; they are never converted into a pass.

## 1. Identity and branding

- [x] Product, skill, plugin, and marketplace names agree across manifests, README, templates, and CI.
- [x] No inherited organisation name, product slug, or author credit outside the documented
      exemptions (licence, NOTICE, changelog, audit history, validator patterns, upgrade commands).
- [x] Inherited icon replaced.
- [x] Every repository URL points at the new destination.
- [x] Install and upgrade commands tested for internal consistency (the plugin/marketplace names match
      the manifests).
- [x] Dated historical-record banner on each Phase 1/2 audit document.
- [x] `NOTICE` present at the root and inside the plugin directory.

## 2. Licensing and attribution

- [x] MIT licence text and copyright notice unchanged in both licence files.
- [x] Derivative status and substantive changes stated in `NOTICE`.
- [x] Rename recorded in `CHANGELOG.md`.
- [x] No third-party code, private asset, client datum, or credential copied into the repository.
- [x] Frappe/ERPNext trademark boundary stated; no endorsement implied.
- [x] No licensing blocker identified.

## 3. Content and packaging

- [x] `SKILL.md` frontmatter `name` matches the skill directory.
- [x] All 16 references linked from `SKILL.md` and indexed in order; no orphans.
- [x] All 26 templates present in `docs/templates/`, listed in the index exactly once, and
      byte-identical to the bundled copies.
- [x] Bundled templates verified with `sync_templates.py --check`.
- [x] Both manifests parse; plugin source path resolves; `author`, `homepage`, `repository`, and
      `license` present.
- [x] Manifest version matches the first changelog heading.
- [x] Project templates updated to the new skill name and a brand-neutral field prefix.
- [x] Issue and PR templates request version, evidence, and agent information.

## 4. Technical revalidation

- [x] White-labeling hook and setting names checked against installed v15 and v16 source.
- [x] `app_icon` / `app_color` consumption corrected (not read by Frappe core 15.94/16.16).
- [x] `get_translated_dict` status corrected (deprecation shim in v16.16, removal slated for v17).
- [x] Error-page override mechanism checked (`www/404.html` resolved by the not-found renderer).
- [x] `add_to_apps_screen` fields and `has_permission` support checked in both versions.
- [x] Evidence scale defined once and cross-referenced from the README and version reference.
- [ ] Execute the runtime behaviour checks on disposable v15/v16 benches — **not run**
      (no disposable bench; the shared benches were inspected read-only).
- [ ] Live agent evaluation of the five scenarios — **not run** (no independent harness).

## 5. Automated gates

- [x] `python3 scripts/validate_repo.py` — 0 errors, 0 warnings.
- [x] `python3 scripts/sync_templates.py --check` — 26 files up to date.
- [x] `python3 -m unittest discover -s scripts/tests -p "test_*.py"` — 28 tests, OK.
- [x] JSON parsing — both manifests.
- [x] YAML parsing — workflow.
- [x] `python3 -m py_compile` — all scripts.
- [x] Conflict-marker scan — none.
- [x] Secret scan — no findings.
- [x] Branding scan — no findings outside exemptions.
- [x] Local-path scan — no developer paths in shipped files.
- [x] External canonical links — HTTP 200.
- [x] Git whitespace — clean (see publication record).
- [x] GitHub Actions on the new repository — run 39230198197, **success**, all steps executed.

## 6. Publication safety

- [x] `.gitignore` covers Python caches, virtual environments, editor state, and agent tooling
      directories.
- [x] No cache, bytecode, log, backup, database, or unrelated local file staged.
- [x] Full staged file list reviewed before the commit.
- [x] No secrets, tokens, or credentials in the tree or in the commit message.
- [x] No local absolute paths in shipped documentation.
- [x] No forced operation used; no upstream repository touched.
- [x] Repository name availability checked before creation; no conflicting destination found.
- [x] Repository visibility and description set deliberately.
- [x] Push verified against the remote, not assumed from the local exit code.
- [x] README renders on GitHub and key links resolve (post-publication).

## 7. Release decision

- [x] Version reflects the actual evidence state (`2.0.0-beta.1`, preview).
- [x] Release notes describe user-facing changes, not file counts.
- [x] Known limitations are in the README, the changelog, and this audit.
- [x] No tag or release created beyond the preview positioning.
- [x] Final status chosen from the allowed set and justified.

**Result:** all mandatory gates passed, including CI on the published commit. Two runtime-dependent
gates remain open and are recorded as not run: disposable-bench behaviour checks and live agent
evaluation. The release is published as a preview, not as stable.
