# Project instructions

This is a Frappe Framework / ERPNext project.

- For **all** code, configuration, and deployment work in this repository, load and follow the
  `frappe-erpnext-engineering-assistant` skill before writing anything. Its placement rules, version rules,
  error-handling rules, and review gate are mandatory.
- Other skills may still be used when they help (for example a testing, design, or communication
  skill). This skill's standards still apply to the code that results.

## Project facts

- Frappe version: `<15.x / 16.x>`
- ERPNext version: `<15.x / 16.x>`   ← must match the Frappe major
- Our app(s): `<app_name>`   ← DocTypes here are "ours" and may be edited directly
- Other installed apps: `<erpnext, hrms, ...>`   ← extend only via hooks/fixtures, never edit them
- Site for commands: `<site_name>`
- Field prefix for custom fields on other apps' DocTypes: `<your_prefix_>`
- Test command: `bench --site <site_name> run-tests --app <app_name>`
- Build/asset command: `bench build --app <app_name>`
- Deployment: `<how a change reaches staging/production, and who approves it>`
- Environments: `<staging host, production host>`

## Boundaries

- Do not edit files under `apps/frappe`, `apps/erpnext`, or another vendor app.
- Do not touch production data, credentials, DNS, or cloud resources.
- Do not put secrets, customer data, or production exports in the repository, logs, or chat.
- Do not commit, push, deploy, migrate production, or publish a release without explicit approval.

## What "done" means here

- The change is in the correct app and file for its DocType (see the skill's placement rules).
- Version-specific behavior matches the versions listed above.
- The relevant tests or bench command were **executed** and the result reported. If something could
  not be run, say so explicitly rather than reporting success.
- The final diff contains only the intended changes, and the files changed are stated with a one-line
  reason each.

## Project-specific rules

<!-- Add one line here every time the agent makes a mistake you don't want repeated. -->
