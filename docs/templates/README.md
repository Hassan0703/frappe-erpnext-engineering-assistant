# Client Templates

Reusable artifacts for real Frappe/ERPNext engagements. Copy the template into the client project,
fill it with real evidence, and keep it under version control.

**Canonical location:** this directory (`docs/templates/`).
**Bundled with the skill:** `plugins/frappe-erpnext-engineering-assistant/skills/frappe-erpnext-engineering-assistant/assets/templates/`
— a byte-identical copy so the templates are available when the plugin is installed outside this
repository. Run `python3 scripts/sync_templates.py` after editing a template here; CI verifies they
match.

> Never fill a template with invented results. If a check did not run, write "not run" and why.

---

## Discovery and audit

| Template | Use when |
|---|---|
| [`project-discovery.md`](project-discovery.md) | Before planning a change on an existing project, or before a large release or upgrade — inventory versions, apps, customizations, permissions, jobs, and risks |

## White-labeling

| Template | Use when |
|---|---|
| [`white-label-discovery.md`](white-label-discovery.md) | Before any branding work — scope surfaces, assets, terminology, licensing |
| [`white-label-implementation-plan.md`](white-label-implementation-plan.md) | After discovery is signed off — classification, files, testing, rollback |
| [`white-label-verification.md`](white-label-verification.md) | After implementing branding, and after every upgrade |
| [`white-label-upgrade-checklist.md`](white-label-upgrade-checklist.md) | Before and after any version upgrade or environment rebuild |

## ERP implementation

| Template | Use when |
|---|---|
| [`requirements-and-acceptance.md`](requirements-and-acceptance.md) | Turning business needs into testable requirements |
| [`fit-gap-analysis.md`](fit-gap-analysis.md) | Deciding standard vs configure vs extend vs build |
| [`technical-design.md`](technical-design.md) | Recording design decisions and rejected alternatives |
| [`permissions-matrix.md`](permissions-matrix.md) | Defining and testing roles, permissions, workflows, SoD |
| [`configuration-inventory.md`](configuration-inventory.md) | Making a rebuild possible; tracking manual configuration |
| [`uat-signoff.md`](uat-signoff.md) | Business acceptance testing and sign-off |

## Deployment and operations

| Template | Use when |
|---|---|
| [`deployment-runbook.md`](deployment-runbook.md) | Operating the system: provisioning, deploy, smoke test, recovery |
| [`environment-inventory.md`](environment-inventory.md) | Recording versions and differences across environments |
| [`backup-restore-test.md`](backup-restore-test.md) | Proving a backup restores — required, not optional |
| [`release-and-rollback.md`](release-and-rollback.md) | Each release, including the rollback plan written before deploy |
| [`incident-report.md`](incident-report.md) | Any production incident, from detection to prevention |

## Data migration

| Template | Use when |
|---|---|
| [`migration-plan.md`](migration-plan.md) | Scoping a migration, snapshot, sequencing, acceptance |
| [`data-mapping.md`](data-mapping.md) | Field-level mapping and transformation rules |
| [`migration-run-log.md`](migration-run-log.md) | One entry per load run (rehearsal or production) |
| [`migration-reconciliation.md`](migration-reconciliation.md) | Proving equivalence: counts, relationships, money, stock |
| [`cutover-checklist.md`](cutover-checklist.md) | The final move, including go/no-go and rollback triggers |

## Testing, QA, and handover

| Template | Use when |
|---|---|
| [`test-plan.md`](test-plan.md) | Planning what will be tested and at which layer |
| [`regression-checklist.md`](regression-checklist.md) | Before releases and after upgrades |
| [`delivery-test-note.md`](delivery-test-note.md) | Every delivery — commands, results, gaps, limitations |
| [`defect-report.md`](defect-report.md) | Reporting and analysing a defect |
| [`handover-checklist.md`](handover-checklist.md) | Handing the system to another team |

---

## Related references

The reasoning behind these templates lives in the skill references:

- `white-labeling.md` — surfaces, safe change classification, verification, legal boundary
- `deployment-and-operations.md` — services, secrets, backups, restore drills, releases, rollback
- `data-migration.md` — profiling, idempotency, reconciliation, cutover
- `testing-and-qa.md` — test layers, version-specific test classes, evidence
- `erp-implementation.md` — discovery, fit-gap, design, UAT, handover
- `support-and-incidents.md` — intake, severity, RCA, communication
