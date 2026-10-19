# Phase 3 Publication Record

**Status:** published (preview)
**Recorded:** 2026-10-19, after verifying the remote and the CI run

A publication record cannot contain a commit hash before the commit exists. The pre-publication values
were checked first; the post-push values below were verified against GitHub, not inferred from local
`git` exit status.

## Verified before the push

| Item | Value | How |
|---|---|---|
| Authenticated account | `Hassan0703` | `gh auth status` (credential never printed) |
| Repository name available | yes | `gh api repos/Hassan0703/frappe-erpnext-engineering-assistant` returned 404 |
| SSH push access | yes | `ssh -T git@github.com` authenticated as `Hassan0703` |
| Visibility | public | deliberate choice for discoverability |
| Default branch | `main` | local branch, pushed as `main` |
| Release candidate version | `2.0.0-beta.1` | `plugin.json`, changelog heading |
| Local gates | passed | validator (0/0), template sync (26), 28 tests, JSON/YAML, `py_compile`, scans |
| Staged file review | passed | 105 files, no cache, bytecode, backup, or local artifact |
| Whitespace | passed | `git diff --cached --check` clean |

## Published identifiers

| Item | Value |
|---|---|
| Repository | <https://github.com/Hassan0703/frappe-erpnext-engineering-assistant> |
| Owner | `Hassan0703` (user account) |
| Visibility | public |
| Default branch | `main` |
| Initial commit | `f1c058006cd3f85c4f2922293344119605e301e9` |
| Commit subject | Release 2.0.0-beta.1 as Frappe ERPNext Engineering Assistant |
| Files in the initial commit | 105 (13,404 insertions) |
| Remote | `origin` → `git@github.com:Hassan0703/frappe-erpnext-engineering-assistant.git` |
| Remote `main` | identical to the local commit (`git ls-remote`) |
| Remote blob count | 105 (GitHub tree API) |

## CI

| Item | Value |
|---|---|
| Workflow | `validate` |
| Run | 39230198197 (push to `main`) |
| Result | **success**, 15 s |
| Steps executed | checkout, setup-python, validator, template sync check, validator tests, manifest JSON parse — all success |

The workflow ran on a clean GitHub checkout, so it confirms the repository validates without the local
environment.

## Post-publication checks

| Check | Result |
|---|---|
| Repository page | HTTP 200 |
| README on `main` | HTTP 200 |
| Skill file on `main` | HTTP 200 |
| README image and relative links | resolve to files present in the pushed tree |
| Install commands | identifiers match `plugin.json` and `marketplace.json` as pushed |

## Release

| Item | Value |
|---|---|
| Tag | `v2.0.0-beta.1` |
| Release type | prerelease (preview), with release notes from `docs/release-notes/v2.0.0-beta.1.md` |
| Stability claim | none — preview |

## Rules applied

- No force-push, no push to the upstream repository, and no import of upstream history.
- The remote was added only as part of creating the new repository from the reviewed local commit.
- Verification was performed against GitHub, not assumed from the local command exit status.
