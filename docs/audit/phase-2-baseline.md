# Phase 2 Baseline — `frappe-code-standards`

> **Historical record (Phase 1/2).** This document describes the project under its original
> name, layout, and repository. It was renamed and independently rebranded in Phase 3; see
> `docs/audit/phase-3-release-audit.md`. Preserved as evidence, and exempt from the
> inherited-branding scan (see `NOTICE`). The development site/app name was redacted for
> publication; versions and results are unchanged.


**Review date:** 2026-10-19
**Reviewer role:** independent principal engineer (Frappe/ERPNext, security, delivery)
**Working copy:** `the project root`
**Product under review:** a Markdown-only Claude Code plugin containing one agent skill, 16
references, and 25 client templates. It ships no runtime code.

## 1. Repository and Git state

The working copy contains a `.git` directory but **no commits, branches, tags, or remotes**:

```text
git rev-list --all --count        -> 0
git branch -avv                   -> (no branches)
git remote -v                     -> (none)
git log --oneline                 -> fatal: current branch 'main' does not have any commits yet
```

This is not a usable history. The working tree is entirely untracked (`git status` shows every
top-level path as `??`). The `.git` directory was therefore not used as the review baseline.

The previous audit correctly recorded that the original archive had no `.git`. That condition is
still true in substance: there is no local history to compare against.

## 2. Recovered baseline

Because network access was available and the published repository is public, a separate clean
upstream checkout was obtained outside the working copy:

```text
git clone --depth 1 https://github.com/NexTash/frappe-code-standards /tmp/fcs-upstream
commit: 099cbe788c69ed6f27b6b196d3b2671766c56a05
date:   2026-10-19 07:40:29 +0500
branch: main
title:  Frappe Code Standards plugin
files:  18
```

The working copy was not replaced or reset. All comparison below is read-only.

### 2.1 Comparison result

| Measure | Count |
|---|---:|
| Upstream baseline files | 18 |
| Working-copy files (excluding `.git/` and the local `.freebuff/` metadata) | 89 |
| Added files | 71 |
| Removed baseline files | **0** |
| Modified baseline files | 13 |
| Markdown files in working copy | 81 |
| Reference documents | 16 |
| Canonical templates (`docs/templates/`, excluding index) | 25 |
| Markdown lines | 10,315 |

The 71 added files are the audit/traceability documents, 25 canonical templates, 25 bundled
template copies, 9 new references, the validator and sync script, CI workflow, contribution and
security files, and `templates/AGENTS.md`.

> Counts were captured before the Phase 2 deliverables were written. The review later added the five
> `docs/audit/phase-2-*.md` documents and `scripts/tests/test_validate_repo.py`, bringing the working
> copy to **95 files / 86 Markdown files**, of which 13 baseline files are modified and 77 are added.

No baseline file was deleted. The baseline skill and all eight original references still exist.
The original placement, error/translation, data-access, reporting, performance, and review
material is preserved in expanded form; nothing useful appears to have been dropped.

### 2.2 Baseline defect confirmed

The upstream `SKILL.md:12` does contain the unsupported range:

```text
Assume Frappe v15+ unless the project shows otherwise.
```

The upstream README badge says `v15 | v16`. The contradiction recorded by the previous audit is
therefore real, and the working copy's replacement scope statement is a genuine correction rather
than a stylistic rewrite.

## 3. Inventory of the working copy

### 3.1 Skill and references

- Entry point: `plugins/frappe-code-standards/skills/frappe-code-standards/SKILL.md` (302 lines).
- Frontmatter: `name: frappe-code-standards` (matches directory), `description` 557 characters
  (limit 1,024), `license: MIT`.
- References: 16 files, all linked from the routing table and listed in the numbered reference
  index. No orphan was found by inspection.
- Bundled templates: 25 files under `assets/templates/`, byte-identical to `docs/templates/`
  (`scripts/sync_templates.py --check` passes).

### 3.2 Metadata

- `.claude-plugin/marketplace.json`: valid JSON, marketplace `nextash`, one plugin, source
  `./plugins/frappe-code-standards` exists and contains `.claude-plugin/plugin.json`.
- `plugins/frappe-code-standards/.claude-plugin/plugin.json`: valid JSON, version `2.0.0`,
  required keys present, `license: MIT`, repository URL standardised on
  `NexTash/frappe-code-standards`.
- `CHANGELOG.md` first heading is `## 2.0.0 — 2026-10-19`, matching `plugin.json`.

### 3.3 Automation

- `scripts/validate_repo.py`: standard-library structural validator (manifests, frontmatter,
  reference/template inventory, links, version phrasing, secrets, local paths, required files).
- `scripts/sync_templates.py`: canonical-to-bundle mirror with `--check`.
- `.github/workflows/validate.yml`: one job, five steps (checkout, Python 3.12, validator, template
  sync check, JSON parse check). The YAML parses; GitHub Actions itself was not executed here.
- **No automated tests for the validator existed in the baseline or in the working copy.** The
  previous report's "fault injection, 13 cases" is not reproducible from committed artifacts.
  This is recorded as a finding and addressed in Phase 4.

## 4. Environment available for verification

A separate development bench exists at `the local bench root`:

```text
frappe    16.52.0  version-16  (4515014)
erpnext   16.51.1  version-16  (5af6561)
<dev-app> 0.0.1   version-16
site:     <dev-app>.local
```

This allowed **source- and runtime-verification of v16** without touching the working copy.
A v15 bench is not present. Redis queue/cache was not running, so scheduler, workers, email, and
PDF verification were not attempted. No production or client environment was accessed.

## 5. Review scope and limitations

Reviewed: the complete skill, all 16 references, all 25 templates, plugin and marketplace
metadata, both scripts, the CI workflow, the changelog, the contribution/security/readme files,
and the three existing audit documents.

Not available:

- A local commit history for the working copy (no commits).
- A v15 runtime bench.
- A running Redis/worker/scheduler stack for v16.
- A mail server or Chromium PDF provisioning.
- Any client environment or customer data.

The recovered upstream checkout removes the largest baseline limitation: the review can now state
what was added, modified, or removed relative to the published repository. It does not prove that
the working copy is the same revision the previous report used, but no evidence of a different
baseline was found.
