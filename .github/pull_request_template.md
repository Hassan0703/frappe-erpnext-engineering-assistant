## What this changes

<!-- One or two sentences: what guidance/capability changes and why. -->

Requirement IDs (from `docs/audit/requirements-traceability.md`), if applicable:

## Type of change

- [ ] Fix to existing guidance (wrong, unsafe, or misleading)
- [ ] New reference or capability
- [ ] New/updated client template
- [ ] Repository tooling, CI, or metadata
- [ ] Documentation only

## Files

| File | Change |
|---|---|
| | |

## Version-claim checklist

- [ ] No support for v14 or earlier and no claim of v17+ support.
- [ ] No version ranges written as `v15+` / `v16+`; version-specific statements are explicit.
- [ ] Any new version-sensitive claim is verified against source or official docs, **or** explicitly
      labelled **Unverified** with what would confirm it.
- [ ] No invented APIs, hooks, config keys, commands, or file paths.

## Quality checklist

- [ ] Rule lives in the reference that owns the topic (no new file for a single rule).
- [ ] Includes a concrete example, and a right/wrong pair where useful.
- [ ] `SKILL.md` routes to the new material without duplicating it.
- [ ] Templates added to `docs/templates/README.md` and synced with
      `python3 scripts/sync_templates.py`.
- [ ] Existing useful content preserved; significant changes explained above.
- [ ] No secrets, credentials, customer data, or production exports.
- [ ] No unrelated reformatting or mass edits.

## Validation

```
$ python3 scripts/validate_repo.py
$ python3 scripts/sync_templates.py --check
```

Paste the output (or state why it could not be run):

```
```

## Versioning

- [ ] Version bumped in `plugins/frappe-erpnext-engineering-assistant/.claude-plugin/plugin.json`.
- [ ] `CHANGELOG.md` updated with a matching top version heading.
- [ ] Bump type is correct (major: scope/behavior change · minor: new capability · patch: wording).
