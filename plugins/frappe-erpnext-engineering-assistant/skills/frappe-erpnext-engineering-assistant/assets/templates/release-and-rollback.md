# Release and Rollback

**Purpose:** record what shipped, how it was verified, and exactly how to undo it.

**How to use:** one record per release. Complete the rollback section **before** deploying, not after
something breaks. Patches and migrations are generally forward-only — state the data-loss window
explicitly.

---

## 1. Release identity

| Item | Value |
|---|---|
| Release / ticket ID | |
| Version / tag | |
| Branch / commit | |
| Planned window | |
| Environments | staging → production |
| Release owner | |
| Approver | |
| Change type | code / schema (patch) / configuration / branding / data migration |

## 2. Contents

| # | Change | Requirement ID | Risk | Rollback impact |
|---|---|---|---|---|
| 1 | | | low/med/high | |
| 2 | | | | |

## 3. Pre-flight

```text
[ ] CI green; review approved
[ ] Release notes / changelog written
[ ] Versions and app branches match each other
[ ] Backup taken: DB + files + config; size and completion verified
[ ] Restore drill current (required for major or schema releases)
[ ] Staging rehearsal completed with the same artifacts
[ ] Migrations reviewed for idempotency and runtime
[ ] Expected downtime and maintenance-mode decision agreed
[ ] Rollback path confirmed and understood by the operator
[ ] Stakeholders notified
```

## 4. Deployment record

| Step | Command | Started | Finished | Result |
|---|---|---|---|---|
| Backup | | | | |
| Maintenance mode on | | | | |
| Deploy revision | | | | |
| Dependencies | | | | |
| `migrate` | | | | |
| `build` | | | | |
| Restart services | | | | |
| Smoke test | | | | |
| Branding check | | | | |
| Maintenance mode off | | | | |

Smoke test results: see `deployment-runbook.md` §5. Outcome: pass / fail

## 5. Post-release monitoring

| Window | Signal | Result |
|---|---|---|
| 30 min | 5xx rate, latency | |
| 1 h | Error Log, queue depth, scheduler | |
| 1 day | Business reconciliation, user reports | |

## 6. Rollback plan (complete before deploying)

| Item | Value |
|---|---|
| Rollback type | code-only / forward-fix / full restore |
| Why this type | |
| Code rollback steps | |
| Schema/data changed? | yes/no |
| If yes: restore source backup + timestamp | |
| **Data-loss window if restored** | |
| User-visible impact of rollback | |
| Estimated time to roll back | |
| Approval required from | |
| Trigger conditions for rollback | |
| Verified? (staging rehearsal / drill) | |

```text
Code-only:
[ ] Deploy previous revision/tag
[ ] bench build
[ ] restart services
[ ] smoke test

Full restore:
[ ] Maintenance mode on
[ ] Restore DB + files from <backup id>
[ ] Deploy previous code revision
[ ] migrate if required for the old code
[ ] build, restart
[ ] smoke test
[ ] Reconcile data written after the backup with the business owner
[ ] Maintenance mode off
```

## 7. Outcome

| Item | Value |
|---|---|
| Deployed successfully? | |
| Rollback used? | yes/no — if yes, which type |
| Incidents during/after | link to `incident-report.md` |
| Follow-up actions | |
| Released by / date | |
