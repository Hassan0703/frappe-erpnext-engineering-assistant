# Frappe ERPNext Engineering Assistant

<p align="center">
  <img src="../../images/stand-alone-logo-square-format.png" alt="Frappe ERPNext Engineering Assistant" width="110">
</p>

Makes AI coding agents work on Frappe Framework and ERPNext **v15 and v16** projects the way an
experienced Frappe team would: in the right file, on the right version, with the framework's own
APIs, and with evidence before anything is reported as done.

**Version support:** Frappe Framework v15 and v16, each with the matching ERPNext major. v14 and earlier
are out of scope; no v17+ support is claimed. See the compatibility matrix in the
[repository audit](https://github.com/Hassan0703/frappe-erpnext-engineering-assistant/blob/main/docs/audit/phase-2-compatibility-matrix.md)
for what is runtime-verified versus source-verified.

## What it enforces

**Code**
- **Correct code placement.** Logic for your own DocTypes goes in the DocType's `.py` and `.js`.
  DocTypes from other apps (ERPNext, HRMS) are extended through `doc_events`, `doctype_js`,
  `overrides/`, `extend_doctype_class` (v16) and fixtures — never by editing the other app.
- **Standard framework APIs.** `frappe.throw`, `frappe.msgprint`, `_()` / `__()` translations,
  `frm.set_query` in `setup`, `frappe.qb`, `frappe.enqueue` and `frappe.log_error`.
- **Security and performance.** Authorization on every whitelisted method, no SQL interpolation,
  no queries in loops, explicit fields, background jobs for slow work, measured improvements.
- **A review gate** covering placement, version compatibility, tests, security, docs and diff hygiene
  — run before the agent reports a task complete.

**Version discipline**
- Detect the Frappe/ERPNext versions from the project instead of assuming them.
- A sourced v15/v16 difference matrix (strict query fields, default sort, commits disabled in
  document hooks, `extend_doctype_class`, `has_permission` returns, Chromium PDFs, Gettext
  translations, test classes, `/desk`) with confidence labels and explicit **Unverified** markers.

**Delivery lifecycle**
- White-labeling and branding (surfaces, safe change classification, verification, upgrade and legal
  boundary).
- ERP implementation, deployment and operations, data migration and reconciliation, testing and QA,
  AI-assisted development, and production support with incident response.
- 26 fillable client templates bundled with the skill, including project discovery, white-label
  discovery, verification, and upgrade checklists.

**Evidence, not optimism**
- The skill requires the agent to run the relevant check, read the result, review the diff, and state
  what it could not verify. "Tests pass" without output is prohibited.

The plugin is plain Markdown guidance. It runs no scripts, makes no network calls and collects no
data.

**Preview:** the product is functionally complete but runtime validation is limited to the checks
recorded in the audit documents. Review the agent's output as you would a teammate's. Issues and
suggestions are welcome on GitHub.

## Install (Claude Code)

```bash
claude plugin marketplace add Hassan0703/frappe-erpnext-engineering-assistant
claude plugin install frappe-erpnext-engineering-assistant@frappe-erpnext-assistant
```

Other agents can use the skill folder directly: copy
`skills/frappe-erpnext-engineering-assistant/` into the agent's skills directory (for OpenCode, one of
`.opencode/skills/`, `.claude/skills/`, or `.agents/skills/`). See the main README for details.

## Use in a project

Copy `templates/CLAUDE.md` or `templates/AGENTS.md` from the repository into your project root and fill
in your Frappe and ERPNext versions, your apps, your site, your custom field prefix, your test command,
and your deployment path.

Full documentation: <https://github.com/Hassan0703/frappe-erpnext-engineering-assistant>

> *"Any fool can write code that a computer can understand. Good programmers write code that humans can understand."*
> — Martin Fowler

MIT licensed. This project is an independent rebranded derivative of the MIT-licensed "Frappe Code
Standards" plugin; see [NOTICE](./NOTICE) for provenance and attribution.
