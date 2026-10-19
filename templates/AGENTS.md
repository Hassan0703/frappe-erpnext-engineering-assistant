# Project instructions (agent-neutral)

This file targets any coding agent. Claude Code users can use `CLAUDE.md` instead (or symlink one to
the other) — the facts below are the same.

This is a Frappe Framework / ERPNext project.

## Required standards

Follow the **frappe-erpnext-engineering-assistant** skill for all code, configuration, and deployment work:
incorrect code placement, version-blind APIs, missing permission checks, and unverified claims of
success are defects.

How to make the skill available to your agent:

| Agent | Where the skill goes |
|---|---|
| Claude Code | Install the plugin (`claude plugin marketplace add Hassan0703/frappe-erpnext-engineering-assistant`, then `claude plugin install frappe-erpnext-engineering-assistant@frappe-erpnext-assistant`) |
| Claude Code (no plugin) | Copy `plugins/frappe-erpnext-engineering-assistant/skills/frappe-erpnext-engineering-assistant/` into `.claude/skills/frappe-erpnext-engineering-assistant/` |
| OpenCode | Copy or symlink it into `.opencode/skills/frappe-erpnext-engineering-assistant/`, `.claude/skills/`, or `.agents/skills/` |
| Other Agent Skills hosts | Copy it into the host's documented skills directory |

If the skill is not installed and cannot be, read the reference documents from
`plugins/frappe-erpnext-engineering-assistant/skills/frappe-erpnext-engineering-assistant/references/` in the plugin repository
before making version-sensitive changes.

## Project facts

- Frappe version: `<15.x / 16.x>`
- ERPNext version: `<15.x / 16.x>`   ← must match the Frappe major
- Our app(s): `<app_name>`   ← DocTypes here are "ours" and may be edited directly
- Other installed apps: `<erpnext, hrms, ...>`   ← extend only via hooks/fixtures
- Site for commands: `<site_name>`
- Custom field prefix for other apps' DocTypes: `<your_prefix_>`
- Test command: `bench --site <site_name> run-tests --app <app_name>`
- Deployment: `<how a change reaches staging/production, and who approves it>`

## Boundaries

- Never edit another vendor app's files; use hooks, fixtures, and custom fields.
- Never modify production data, credentials, DNS, or cloud resources.
- Never put secrets, customer data, or production exports in the repository, logs, or chat.
- Never commit, push, deploy, or publish without explicit approval.

## Verification expected

- Detect the Frappe/ERPNext versions before making version-sensitive decisions.
- Run the relevant tests or bench command and report the observed result.
- If a check could not be run, state that plainly — do not describe it as passing.
- State the files changed and why each location was correct.
