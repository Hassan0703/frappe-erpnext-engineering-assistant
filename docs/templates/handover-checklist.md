# Handover Checklist

**Purpose:** ensure another team can operate, support, and change the system without the original
implementer.

**How to use:** complete before the final acceptance meeting. Each artifact must be in a location the
client controls, not only on a developer's machine.

---

## 1. Handover context

| Item | Value |
|---|---|
| Client / project | |
| Handover date | |
| Handing over from / to | |
| Frappe / ERPNext versions | |
| Environments covered | |
| Support model after handover | |

## 2. Documentation

```text
[ ] Architecture and app boundaries
[ ] Installation / environment setup steps
[ ] Configuration and customization inventory
[ ] Integration contracts and credentials ownership
[ ] Data model overview (key DocTypes and relationships)
[ ] Permissions and workflow matrices
[ ] Report and dashboard catalogue with definitions and owners
[ ] Migration mapping, run logs, and reconciliation (if data was migrated)
[ ] Deployment runbook, including rollback
[ ] Backup and restore procedure + last drill result
[ ] Monitoring, alerting, and escalation contacts
[ ] Troubleshooting / common failure modes
[ ] Known limitations and technical debt register
[ ] Release notes and upgrade instructions
[ ] Licensing/attribution notes (if white-labeled)
```

## 3. Repository and code

```text
[ ] Client owns/controls the repository (correct remote verified)
[ ] Default branch state is clean and tagged for the release
[ ] CI configured and passing
[ ] Custom app names and ownership recorded per DocType
[ ] No secrets in the repository or its history
[ ] Fixtures/patches reproduce configuration on a fresh site
[ ] README documents setup, test, and deploy commands
```

## 4. Test evidence

```text
[ ] Test plan and results
[ ] Delivery test notes for released changes
[ ] UAT scripts and client sign-off
[ ] Regression checklist results
[ ] Backup/restore drill record
[ ] Open defects with severity, owner, and target
```

## 5. Operations

```text
[ ] Runbook reviewed with the operating team (walkthrough done)
[ ] Access granted: host, database, secret store, monitoring, backups
[ ] Backup schedule verified by the receiving team
[ ] Restore performed by the receiving team (not just observed)
[ ] Scheduler and workers explained; failure modes covered
[ ] Upgrade procedure walked through (including v15→v16 considerations if relevant)
[ ] Maintenance-mode and incident procedures understood
[ ] On-call/escalation path agreed
```

## 6. Business

```text
[ ] Users trained by role; quick reference provided
[ ] Admin training: users, roles, permissions, workflows
[ ] Reports and their owners agreed
[ ] Data retention and privacy obligations understood
[ ] Open business decisions listed with owners
```

## 7. Open items

| # | Item | Type | Impact | Owner | Target date |
|---|---|---|---|---|---|
| 1 | | docs/code/ops/business | | | |

## 8. Sign-off

| Role | Name | Date | Notes |
|---|---|---|---|
| Client project owner | | | |
| Client IT/ops owner | | | |
| Outgoing implementer | | | |
