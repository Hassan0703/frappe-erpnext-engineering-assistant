<p align="center">
  <img src="plugins/frappe-erpnext-engineering-assistant/.claude-plugin/icon.png" alt="Frappe ERPNext Engineering Assistant" width="140">
</p>

<h1 align="center">Frappe ERPNext Engineering Assistant</h1>

<p align="center">
  A Frappe and ERPNext engineering assistant for <b>v15 and v16</b> — covering customization,
  white-labeling, implementation, data migration, testing, deployment, security, and AI-assisted
  development.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-preview-orange" alt="Preview">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-black" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/Frappe-v15%20%7C%20v16-red" alt="Frappe v15 | v16">
</p>

> [!IMPORTANT]
> **Preview release.** The product identity, scope, documentation, validator, and tests are complete
> and pass locally. Runtime behaviour is verified on Frappe 16.52 only; there is no v15 runtime bench,
> no live agent evaluation, and CI has not yet run on GitHub. Treat every version-sensitive claim
> according to its labelled evidence level (see [Verification status](#verification-status)).

## What this is

A skill (instruction set) that an AI coding agent loads before working on a Frappe/ERPNext project.
It makes the agent behave like an experienced Frappe team member: find the owning app first, respect
app boundaries, use supported extension points, keep business rules on the server, and **show
evidence before calling anything done**.

It is built for:

- Frappe/ERPNext developers who work with AI coding agents and want predictable, reviewable output.
- Implementation consultants and technical leads running client projects on v15/v16.
- ERP agencies and engineering teams standardising how agents touch shared codebases.
- Anyone doing white-label branding, data migration, upgrades, or production support on Frappe.

It is not a runtime library. There is no code to install, no network calls, and no data collection —
the shipped plugin is Markdown plus metadata.

## What it helps with

| Area | Examples |
|---|---|
| **Code placement and extension** | own-DocType logic in its own files; other apps extended through `doc_events`, `doctype_js`, overrides, `extend_doctype_class` (v16), fixtures — never by editing vendor apps |
| **DocTypes and metadata** | fields, child tables, Single DocTypes, naming, property setters, custom fields |
| **Permissions and security** | role/permission layers, `permlevel`, row-level scoping, authorization on every whitelisted method, SQL safety, uploads, secrets |
| **White-labeling** | desk, login, navbar, website/portal, email, print/PDF, favicon, translations, app metadata, upgrade-safe verification |
| **ERP implementation** | discovery, fit-gap, standard-first decisions, workflows, segregation of duties, UAT, handover |
| **Data migration** | profiling, mapping, idempotent loads, reconciliation, cutover, rollback |
| **Testing and QA** | unit/integration classes per version, permission and failure-path tests, delivery evidence |
| **Deployment and operations** | environments, config, TLS, backups, restore drills, releases, rollback, monitoring |
| **Support and incidents** | intake, severity, evidence-first diagnosis, root-cause analysis, minimal fixes |
| **AI-assisted development** | version detection, impact analysis, small changes, diff review, evidence-backed reports |

## Supported versions

| | Supported | Evidence level |
|---|---|---|
| Frappe Framework v16 | Yes | Runtime-verified on 16.52 for the query, hook, test-class and command claims; otherwise source-verified |
| ERPNext v16 | Yes (matching major) | Source-verified on 16.51.1 |
| Frappe Framework v15 | Yes | Source-verified against the `version-15` branch; not executed |
| ERPNext v15 | Yes (matching major) | Source-verified |
| v14 and earlier | Not supported | — |
| v17 and later | No support claimed | — |

Frappe and ERPNext must share a major version. Version-sensitive guidance is labelled, and anything
that was not confirmed against source, documentation, or a command is marked **unverified**.

## Install

### Claude Code (plugin)

```bash
claude plugin marketplace add Hassan0703/frappe-erpnext-engineering-assistant
claude plugin install frappe-erpnext-engineering-assistant@frappe-erpnext-assistant
```

Enable or disable it per project:

```bash
claude plugin disable frappe-erpnext-engineering-assistant@frappe-erpnext-assistant
claude plugin enable frappe-erpnext-engineering-assistant@frappe-erpnext-assistant
```

### Other agents (portable skill folder)

The skill is a standard `SKILL.md` folder, so it can be copied into another Agent Skills host:

```bash
git clone https://github.com/Hassan0703/frappe-erpnext-engineering-assistant
mkdir -p .opencode/skills
cp -r frappe-erpnext-engineering-assistant/plugins/frappe-erpnext-engineering-assistant/skills/frappe-erpnext-engineering-assistant .opencode/skills/
```

OpenCode's documented skill paths are `.opencode/skills/<name>/SKILL.md`,
`.claude/skills/<name>/SKILL.md`, and `.agents/skills/<name>/SKILL.md` (plus their global
equivalents). Other hosts use their own discovery paths — check the host's documentation.

**Integration status:** Claude Code packaging is the only integration tested here. Other agents are
supported only through the portability of the skill format, not by a maintained integration.

### claude.ai

Zip the skill folder and upload it under **Skills** in your claude.ai settings:

```bash
cd plugins/frappe-erpnext-engineering-assistant/skills
zip -r frappe-erpnext-engineering-assistant.zip frappe-erpnext-engineering-assistant
```

### Upgrading from the previous name

The plugin, skill, and marketplace were renamed in 2.0.0-beta.1, so an existing installation cannot
be updated in place:

```bash
claude plugin uninstall frappe-code-standards@nextash   # remove the old plugin
claude plugin marketplace remove nextash                # remove the old marketplace
claude plugin marketplace add Hassan0703/frappe-erpnext-engineering-assistant
claude plugin install frappe-erpnext-engineering-assistant@frappe-erpnext-assistant
```

Then update any project instructions that name the old skill.

## Quick start

1. Install the skill using one of the commands above.
2. Copy [`templates/CLAUDE.md`](templates/CLAUDE.md) (Claude Code) or
   [`templates/AGENTS.md`](templates/AGENTS.md) (any agent) into the root of your Frappe project.
3. Fill in the project facts: Frappe and ERPNext versions, your app(s), site name, custom-field
   prefix, test command, and how changes reach production.
4. Ask the agent for a task and watch it inspect before editing, detect versions, and report what it
   verified.

The project file is what tells the agent which DocTypes it may edit directly, which must be extended
through hooks, and what "done" means on your project.

## Example tasks

- "On Sales Order, only allow warehouses for the selected company and stop submit if the delivery
  date is in the past."
- "White-label this ERPNext site for our client without editing framework core, and give me a
  verification checklist."
- "We need a two-level purchase approval. Configure it as standard as possible and tell me what you
  changed."
- "Plan a migration of customers, items, and open invoices from our old system, with reconciliation
  and a rollback plan."
- "Why are scheduled reminders not sending? Gather evidence first, then propose the smallest fix."
- "Review this app for v15/v16 compatibility and list anything that will break on upgrade."

## White-labeling workflow (example)

The assistant treats white-labeling as a small project, not a logo swap:

1. **Discover** — versions, tenancy, in-scope and out-of-scope surfaces, assets, terminology,
   domains, licensing. Template: [`white-label-discovery.md`](docs/templates/white-label-discovery.md).
2. **Classify each change** — configuration, supported custom-app mechanism, hook/fixture,
   patch/migration, or framework fork (last resort). Decision tree in
   [`white-labeling.md`](plugins/frappe-erpnext-engineering-assistant/skills/frappe-erpnext-engineering-assistant/references/white-labeling.md).
3. **Implement in the right place** — a custom app and supported hooks, never vendor files.
4. **Verify every surface** — desk, login, website/portal, apps screen, email, notifications,
   print/PDF, favicon, translations, mobile viewport. Template:
   [`white-label-verification.md`](docs/templates/white-label-verification.md).
5. **Prove it survives upgrades** — `clear-cache`, `bench build`, `migrate`, and the upgrade
   checklist: [`white-label-upgrade-checklist.md`](docs/templates/white-label-upgrade-checklist.md).

## Safety and upgrade-compatibility principles

- **Inspect before editing.** Read the owning app, existing controller/JS, hooks, and project
  instructions first.
- **Respect app ownership.** Extend frappe/erpnext/other apps through hooks, fixtures, and custom
  fields — never by editing their files.
- **Smallest safe change.** Preserve existing behaviour unless the requirement changes it.
- **Business rules on the server.** Client JavaScript is UX, never enforcement.
- **Evidence, not optimism.** Distinguish facts, source-verified claims, runtime-verified claims,
  assumptions, and unverified items. Never claim a test passed unless it ran.
- **No production mutation, no destructive operations, no unrequested commits or deploys.**
- **Upgrade safety is designed in.** Prefer supported extension points, and record what an upgrade
  will overwrite.

## Verification status

This project labels every version-sensitive statement with one of: **runtime-verified**,
**source-verified**, **documentation-verified**, or **unverified**. The full matrix, including the
exact commands run on Frappe 16.52 and the provisioning plan for v15/v16 benches, is in
[`phase-2-compatibility-matrix.md`](docs/audit/phase-2-compatibility-matrix.md).

- Runtime-verified on v16: query field parsing, default sort, `sendmail` commit behaviour, Single
  value casting, `extend_doctype_class`, test classes, `bench setup-chrome`, `bench data-import`,
  and the operations commands used in the runbook.
- Source-verified: v15 and v16 library behaviour, hooks, permissions, and metadata.
- **Not verified:** v15 runtime execution, scheduler/workers, email delivery, PDF rendering, GitHub
  Actions execution, and live agent evaluation of the five scenarios in
  [`phase-2-agent-evaluation.md`](docs/audit/phase-2-agent-evaluation.md).

## Testing this repository

```bash
python3 scripts/validate_repo.py          # manifests, frontmatter, inventory, links, phrasing, secrets, branding
python3 scripts/sync_templates.py --check # bundled templates match docs/templates
python3 -m unittest discover -s scripts/tests -p "test_*.py"  # validator passing and failing cases
```

CI runs all three on push and pull request
([`.github/workflows/validate.yml`](.github/workflows/validate.yml)). The validator fails the build on
broken links, orphaned references, unsynced templates, unsupported version phrasing, inherited
branding, and committed secrets.

## What's inside

```
plugins/frappe-erpnext-engineering-assistant/
├── .claude-plugin/plugin.json
└── skills/frappe-erpnext-engineering-assistant/
    ├── SKILL.md                              Scope, workflow, verification gate, routing
    ├── assets/templates/                     Client templates, bundled for runtime use
    └── references/
        ├── code-placement.md                 Where every kind of code belongs
        ├── server-patterns.md                Controllers, transactions, whitelisting, DB
        ├── client-patterns.md                Form scripts, set_query, dialogs, list view
        ├── hooks-and-customization.md        hooks.py, fixtures, patches, scheduler, permissions
        ├── performance.md                    Queries, indexes, caching, jobs, measurement
        ├── reports-and-printing.md           Report types, script reports, print/PDF (v16)
        ├── version-compatibility.md          Detection + v15/v16 difference matrix
        ├── white-labeling.md                 Discovery, decision tree, surfaces, verification, legal
        ├── erp-implementation.md             Requirements, fit-gap, design, UAT, handover
        ├── deployment-and-operations.md      Services, secrets, backups, risk classes, rollback
        ├── data-migration.md                 Profiling, mapping, idempotency, reconciliation
        ├── testing-and-qa.md                 Test layers, permission tests, evidence
        ├── security.md                       Authorization, injection, uploads, privacy, licensing
        ├── ai-features.md                    Tool boundaries, injection, approval, evals
        ├── support-and-incidents.md          Intake, severity, RCA, minimal fix
        └── review-checklist.md               The gate before reporting a task complete

docs/templates/                               26 fillable client documents
docs/audit/                                   Phase 1–3 audits, traceability, roadmap, release audit
scripts/                                      Validator, template sync, and their tests (CI only)
```

## Documentation map

Start at the skill entry point:
[`SKILL.md`](plugins/frappe-erpnext-engineering-assistant/skills/frappe-erpnext-engineering-assistant/SKILL.md).
It routes to the reference that owns each topic. Reusable client documents live in
[`docs/templates/`](docs/templates/README.md) and are also bundled inside the skill so they are
available when the plugin is installed.

## Limitations and caveats

- Version differences are documented and sourced, but **not every patch release** is covered. When a
  decision depends on a patch level, read the installed source.
- Branding field names are described by purpose; confirm the exact `fieldname` in the installed
  DocType JSON before writing code.
- Fixture behaviour for Single DocTypes is unverified; the guidance recommends an idempotent
  patch/`after_install` instead.
- No client environment is bundled. Templates require the executing engineer to record real evidence.
- Claude Code packaging is the only tested integration.
- Nothing here is legal advice. Licensing and trademark questions are framed as questions for
  qualified counsel.

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the rule style,
validation commands, versioning, and template workflow. Use the issue templates for bug reports and
feature requests, and read [SECURITY.md](SECURITY.md) before reporting a security concern.

## Changelog and releases

See [CHANGELOG.md](CHANGELOG.md) and the release notes draft in
[`docs/release-notes/`](docs/release-notes/). The current release is a **preview** (`2.0.0-beta.1`);
no stability guarantee is implied.

## License and attribution

[MIT](LICENSE).

This project is an independent rebranded derivative of the MIT-licensed "Frappe Code Standards"
plugin. The original copyright notice and license text are preserved unchanged. See
[NOTICE](NOTICE) for provenance and attribution, and `docs/audit/` for the historical reviews under
the previous name.
