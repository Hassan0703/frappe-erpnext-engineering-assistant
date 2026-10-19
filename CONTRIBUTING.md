# Contributing

Thanks for improving these standards. The goal is guidance that a senior Frappe/ERPNext engineer
would recognize as correct and an AI agent can act on without guessing.

## Scope

Supported: **Frappe Framework v15 and v16** and the matching ERPNext majors.

Out of scope: v14 and earlier, and any claim of v17-or-later support. Forward-looking upstream notes
(for example "upstream states this stops working in v17") are acceptable when they are cited and
clearly labelled as upstream.

Do not add guidance for deprecated APIs without saying what replaces them and on which version.

## Repository layout

```
plugins/frappe-erpnext-engineering-assistant/          Claude Code plugin (the shippable product)
  skills/frappe-erpnext-engineering-assistant/
    SKILL.md                            Entry point: scope, workflow, routing
    references/*.md                     Detailed guidance, one topic per file
    assets/templates/*.md               Bundled copies of the client templates
docs/audit/                             Audit, traceability, roadmap (historical record)
docs/release-notes/                     User-facing notes per release
docs/templates/                         Canonical client templates
scripts/                                sync_templates.py, validate_repo.py
templates/                              Project instruction templates for client repos
```

## Changing or adding a rule

1. Put the rule in the reference that owns the topic. Do not create a new file for a single rule.
2. Follow the house style:
   - State the rule, then a concrete right/wrong example where it helps.
   - Say **where** the code goes, not just what it should do.
   - Mark version differences explicitly (`v15` / `v16`), never with a "+" range.
   - Prefer "discouraged, and here is when it is acceptable" over an absolute "never" for practices
     that depend on the client's deployment model.
3. Do not invent APIs, hook names, config keys, commands, file paths, or framework behavior. If you
   cannot verify a claim against source, official docs, or observed command output, label it
   **Unverified** and say what would confirm it.
4. Keep `SKILL.md` short. It routes to references; it does not duplicate them.
5. Keep existing useful content. Explain significant changes in the PR description.

## Adding or changing a template

1. Add the file to `docs/templates/`.
2. Add it to the index in `docs/templates/README.md` with when to use it.
3. Run `python3 scripts/sync_templates.py` to update the bundled copy inside the plugin.
4. Templates must be fillable forms with named fields — not prose essays. Never include fabricated
   example results.

## Validation

```bash
python3 scripts/validate_repo.py        # structure, links, inventory, phrasing, secrets
python3 scripts/sync_templates.py --check
python3 -m unittest discover -s scripts/tests -p "test_*.py"   # validator passing/failing cases
```

Adding a reference or a template is an intentional act: update `REQUIRED_REFERENCES` or
`REQUIRED_TEMPLATES` in `scripts/validate_repo.py`, add it to the `SKILL.md` reference index or the
template index, then run the commands above. The validator fails on an unexpected file, so the
inventory stays deliberate.

`validate_repo.py` checks, among other things:

- every `plugin.json` / `marketplace.json` parses and the plugin source exists,
- `SKILL.md` frontmatter has a valid `name` (matching the directory) and a 1–1024 character
  `description`,
- every reference file is linked from `SKILL.md` and vice versa (no orphans),
- every template is listed in the index and byte-identical to its bundled copy,
- all relative Markdown/HTML links resolve,
- no unsupported version phrasing (`v15+`, `v14+`, uncited v17/v18 claims),
- no secret-like values or leaked local paths.

Fix failures rather than weakening the check. If a rule must change, change it in the script with a
comment explaining why, and mention it in the PR.

### What the suite does *not* check

The validator and its tests are structural. They cannot judge whether guidance is technically correct,
and they do not attempt general contradiction detection — only narrow, reliable cases (a duplicated
index entry, an unsupported version range, a broken link). Semantic review of the prose, and
confirmation of every version-sensitive claim against source or documentation, remain human
responsibilities. Keep each rule in the one reference that owns its topic so contradictions have a
single place to surface.

## Versioning

`plugins/frappe-erpnext-engineering-assistant/.claude-plugin/plugin.json` carries the version; `CHANGELOG.md` must
start with the same version.

| Change | Bump |
|---|---|
| Scope change, removed capability, or guidance that changes existing behavior (e.g. the v15+ scope fix) | **major** |
| New reference, new template, new capability | **minor** |
| Wording, examples, typo, link, metadata | **patch** |

Installed copies pick up updates from the version bump, so every merged change needs one.

## Pull requests

Use the PR template. Keep changes focused: one topic per PR, no unrelated reformatting. Include the
validation output.

## Reporting problems

- Wrong or unsafe guidance: use the bug report issue template. Include the prompt, the output you got,
  and what the correct output should be, with a source link where possible.
- Security issue (for example guidance that would leak credentials or weaken authorization):
  see `SECURITY.md` and report privately.

## Branding and attribution

- Use the product name **Frappe ERPNext Engineering Assistant** and the skill name
  `frappe-erpnext-engineering-assistant` in new text and metadata.
- Inherited branding is allowed only in `LICENSE`, `NOTICE`, `CHANGELOG.md`, the historical audit
  documents, exact removal/upgrade commands, and the validator's own pattern list. The validator
  enforces this; do not work around it by renaming those files.
- Do not remove or alter the original copyright notice. If you add third-party material, record it in
  `NOTICE` and confirm its licence is compatible.

## Licensing

The plugin is MIT licensed. By contributing you agree your contribution is provided under the same
license. Do not paste code from a GPL or otherwise incompatible project into these files.
