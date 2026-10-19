# ERP Implementation and Configuration

The goal is a system the client can operate, audit, and upgrade — not the maximum amount of custom
code. Most failed ERP projects over-customize and under-document.

This reference applies to ERPNext implementations and to equivalent client ERPs built on Frappe.
Version-specific APIs live in `version-compatibility.md`.

## 1. Discovery

Establish, in writing:

- Business model, entities, locations, currencies, fiscal calendar, and statutory requirements.
- Stakeholders and process owners (not just IT).
- Current process, volume, cycle time, pain points, and workarounds.
- Systems being replaced and their data/exit constraints.
- Non-negotiable requirements vs preferences.
- Constraints: go-live date, budget, integrations, hosting, data residency, licensing.
- Success measures: what must be true for the client to call this a success.

Do not design screens before understanding the process. Do not accept "make it like the old system"
without asking which behavior is actually required.

## 2. Requirements and acceptance criteria

Each requirement needs:

- ID, owner, business justification.
- Current behavior and desired behavior.
- Acceptance criteria that a tester can execute (given/when/then or a concrete scenario).
- Priority (must/should/could) and target release.
- Data implications (new fields, migration, reporting).

Use `assets/templates/requirements-and-acceptance.md`. A requirement with no acceptance criterion
cannot be signed off.

## 3. Fit-gap and the standard-first rule

For each requirement, evaluate in this order:

1. **Standard feature/configuration** — DocType settings, workflows, permissions, naming series,
   print formats, standard reports.
2. **Standard extension** — custom fields, property setters, fixtures, notifications, client scripts
   in the app.
3. **Small custom app logic** — controller hooks, whitelisted methods, reports.
4. **New DocType/app** — only when the domain genuinely has no equivalent.
5. **Framework/core modification** — last resort; not upgrade-safe; requires explicit approval.

| Gap type | Preferred response | Cost/risk |
|---|---|---|
| "We do it slightly differently" | Configure or change the process | Low |
| Missing field/validation | Custom field + server validation | Low |
| Different approval path | Workflow configuration | Low–medium |
| Missing report | Script report / query report | Low |
| Missing integration | Custom app + integration contract | Medium |
| Entirely new domain | New DocType/app | High |
| Core behavior change | Override/extend hook; fork only with approval | High–very high |

Challenge:

- Custom fields that duplicate standard fields.
- Separate DocTypes that duplicate standard documents.
- Client scripts that enforce rules the server must enforce.
- Reports built from raw SQL when a standard report exists.
- "We need a new app" when the change belongs in the existing client app.
- Workflows with no rejection path, no delegation, and no audit.

Record the decision and the rejected alternatives in `assets/templates/technical-design.md`.

## 4. Data model and DocType design

Review before creating schema:

- **Naming:** meaningful prefix/series; stable identifiers; legacy ID field for migration.
- **Parent/child:** child tables for rows owned by the parent; Link fields for independent records.
  Do not use a child table for something queried/reported independently.
- **Status:** use `docstatus` for draft/submitted/cancelled; a separate status field for business
  state. Do not encode workflow state only in a free-text field.
- **Immutability:** submitted documents should not be silently edited; corrections via cancel/amend
  or a documented adjustment.
- **Multi-company/currency:** every transactional DocType must carry company and currency
  explicitly; permissions and reports must scope by company.
- **Indexes:** add `search_index` for fields used in frequent filters; do not index everything.
- **Audit:** who changed what, when; use standard tracking before inventing a log table.
- **Deletion:** define what happens to links; use `on_trash` checks and prevent orphaning.

Schema changes after go-live are migrations. Plan them like code changes.

## 5. Workflows, approvals, notifications, assignments

- Model states and transitions explicitly; document who can move each transition.
- Include rejection, cancellation, and resubmission paths.
- Ensure approvals cannot be bypassed by direct document edits or API calls; enforce in the
  controller/workflow, not only the UI.
- Notifications: who, when, channel, and what action is expected. Avoid alert fatigue.
- Assignments/escalation: define timeouts and an owner for stuck approvals.
- Test each transition as each role, including the denial path.
- Record the workflow matrix in `assets/templates/permissions-matrix.md`.

## 6. Roles, permissions, and segregation of duties

- Start from job roles, not from people.
- Least privilege: read-only where writing is not required; company/territory scoping.
- Segregation of duties: the person who creates a payment should not be the only approver; the person
  who configures permissions should not silently approve their own transactions.
- Use `permlevel` for sensitive fields (cost, margin, bank details, salary).
- Use User Permissions / `permission_query_conditions` for row-level scope.
- Test with real restricted users, not Administrator.
- Document the matrix and get business approval; permission changes are security changes.

## 7. Reports, dashboards, and workspaces

- Prefer standard reports; extend with filters or a script report rather than duplicating logic.
- Reports must respect permissions and company scope.
- Define the metric, date basis, currency, and inclusion rules. Two reports with the same name but
  different definitions destroy trust.
- Dashboards need owners and refresh expectations; an unowned dashboard rots.
- Workspaces should reflect the client's actual jobs-to-be-done, not the upstream demo layout.
  v16 overwrites modified standard workspaces on migrate — keep customizations in your app.

## 8. Accounting and inventory implications

Involve the finance/operations owner in any change that touches money or stock. Engineering alone
cannot sign off a ledger.

- Posting date, fiscal year, currency, exchange rate, and tax must be explicit.
- Do not insert general-ledger or stock-ledger entries directly; use standard documents and opening
  mechanisms.
- Backdated transactions can change valuation and closed periods; define policy and permissions.
- Negative stock, reorder levels, batches/serials, and valuation methods are business decisions with
  accounting consequences.
- Reconciliation is a business control: AR/AP aging, trial balance, stock valuation, and bank
  reconciliation must be owned and reviewed.
- Any migration of financial data follows `data-migration.md` and requires reconciliation sign-off.

## 9. Integrations

For each integration, write a contract:

- Direction, trigger, payload schema, auth, retry/timeout, idempotency key, error handling.
- Who monitors it and what happens when it fails.
- Data ownership and conflict resolution (which system wins).
- Test failure modes: downstream down, slow, duplicate, malformed, unauthorized.

Do not let an integration write directly into tables. Use whitelisted APIs or documented endpoints,
and log failures.

## 10. Configuration management

Everything that must exist in production must be reproducible:

- Custom Fields, Property Setters, Workflows, Print Formats, Reports, Notifications, Roles.
- Naming series, default settings, taxes, UOMs, warehouses, chart of accounts.
- Use fixtures/patches/custom app code; document anything applied manually.
- Record configuration in `assets/templates/configuration-inventory.md` with owner and environment.
- Verify a fresh site install reproduces the configuration before go-live.
- Changes to configuration follow the same review and release path as code.

## 11. UAT, training, and rollout

- UAT scripts are business scenarios with real data and expected results, executed by the client's
  named users. Use `assets/templates/uat-signoff.md`.
- Track defects with severity, owner, and target release. Do not hide known issues in a go-live
  meeting.
- Train by role, on the actual configured system, with the client's own data. Provide a quick
  reference and a support path.
- Rollout: pilot → department → company, or big-bang if the client accepts the risk. Define the
  cutover and rollback triggers.
- Hypercare: named support window, daily triage, and a stop condition.

## 12. Handover

Deliver:

- Architecture and app boundaries.
- Configuration and customization inventory.
- Integration contracts.
- Permissions matrix and workflow matrix.
- Migration mapping, run logs, and reconciliation.
- Runbook, backup/restore procedure, and monitoring.
- Known limitations, technical debt, and open risks.
- Release/upgrade instructions and support contacts.
- Test evidence and UAT sign-off.

Use `assets/templates/handover-checklist.md`. A handover without these is a dependency, not a
delivery.

## 13. Anti-patterns

- Designing from screens instead of processes.
- Customizing before checking standard behavior.
- New app for a field; new DocType for a report.
- Approvals enforced only in JavaScript.
- Permissions granted to "make it work" and never reviewed.
- Direct ledger/stock inserts.
- Manual production configuration with no record.
- Go-live with unapproved reconciliation differences.
- No named owner for reports, integrations, or approvals.
- Handover by verbal explanation only.

## 14. Implementation checklist

- [ ] Stakeholders, processes, scope, and success measures documented.
- [ ] Requirements have executable acceptance criteria and priorities.
- [ ] Fit-gap recorded with standard-first rationale and rejected alternatives.
- [ ] Data model reviewed (naming, parent/child, status, company/currency, indexes, audit).
- [ ] Workflow states, transitions, roles, notifications, and escalation tested.
- [ ] Permissions matrix approved; segregation of duties reviewed; tested as restricted users.
- [ ] Reports/dashboards have owners, definitions, and permission-scoped results.
- [ ] Finance/ops owner signed off accounting and inventory implications.
- [ ] Integrations have contracts, failure handling, and monitoring.
- [ ] Configuration is reproducible on a fresh site; inventory completed.
- [ ] UAT executed and signed off; defects triaged.
- [ ] Training delivered by role; hypercare owner named.
- [ ] Handover pack complete, including rollback and known limitations.
