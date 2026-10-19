# Support and Incident Management

After go-live, the priority order changes: **preserve data integrity and service availability first**;
cosmetic refactoring can wait. A production fix that loses a transaction is worse than the bug.

## 1. Intake

Every issue starts with enough information to reproduce it:

```text
Reporter / client / role:
Environment: production | staging | local   URL:
Versions: Frappe <x> / ERPNext <y> / apps <...>
First observed (with timezone):
Steps to reproduce (numbered):
Expected result:
Actual result (error text, screenshot, trace):
Affected documents/users/companies:
Business impact:
Recent changes/releases:
Attachments (logs, screenshots) — no secrets or unnecessary PII:
```

Use `assets/templates/defect-report.md`. If the report says "it doesn't work", ask for the exact
action, document, and time before investigating.

## 2. Severity and impact

Agree the matrix with the client up front; do not invent response targets after an incident.

| Severity | Definition | Examples | Response posture |
|---|---|---|---|
| **S1 Critical** | Data loss/corruption, security breach, or core business stopped for many users | Cannot submit invoices; wrong ledger postings; production down; unauthorized data access | Immediate; incident lead; stakeholder updates; consider maintenance mode |
| **S2 High** | Major function broken, workaround painful or risky | Approvals stuck; PDF generation failing; integration down | Same-day triage; workaround documented |
| **S3 Medium** | Limited function degraded, workaround acceptable | One report wrong; a permission too broad but unexploited | Planned fix; track |
| **S4 Low** | Cosmetic, usability, documentation | Label typo; alignment | Backlog |

Consider: users affected, money at risk, data integrity, security/privacy, regulatory deadline,
and whether a workaround exists. Re-classify as facts change, and record why.

## 3. Reproduce safely

- Reproduce on staging or a restored copy, not on production.
- Use the smallest dataset that shows the bug; do not copy customer data unnecessarily.
- Capture the exact document names, user roles, timestamps, and version.
- If the bug depends on data, snapshot the relevant rows before changing anything.
- If it cannot be reproduced, say so and gather more evidence; do not "fix" by guesswork.

## 4. Evidence to collect

| Source | What to look for |
|---|---|
| Error Log (Desk) | Traceback, timestamp, method, doctype |
| `logs/web.log`, `logs/worker.log`, `logs/scheduler.log` | 5xx, worker failures, job errors |
| Browser console/network | Failed requests, 403/500, payload shape |
| Background jobs | Pending/failed jobs, queue age |
| Database | Slow queries, locks, connection limits |
| Proxy | 502/504, TLS, upload limits, timeouts |
| Scheduler | Enabled? recent runs? |
| Recent changes | Release tag, patches, config changes |

Redact secrets and personal data before sharing logs.

## 5. Root-cause analysis

- Build a timeline with timestamps and timezone.
- Distinguish trigger, root cause, and contributing factors.
- Ask why until you reach a controllable cause: missing validation, wrong permission, race condition,
  bad deployment step, missing index, unhandled external failure.
- Check whether the same defect exists elsewhere (same pattern in other DocTypes/jobs).
- Record evidence for the conclusion; "probably" is a hypothesis, not an RCA.
- Avoid blame; fix the system and the process.

## 6. Minimal corrective change

- Fix the cause, not the symptom.
- Change the fewest files; avoid refactoring during an incident.
- Prefer a server-side guard or a data repair patch with a dry run over manual DB edits.
- If data is already wrong, write a corrective patch that is idempotent, logged, and reversible
  where possible. Do not hand-edit production rows without a backup, a script, and approval.
- Never run a blind retry of a write operation; check whether the first attempt partially applied.
- If the fix needs a longer design, ship a safe interim guard and a follow-up task.

## 7. Data integrity and security review

For every production fix, ask:

- Did the defect write incorrect data? Which tables/documents? What is the scope?
- Are links, totals, ledger entries, or stock balances affected?
- Did it expose data to the wrong user/company/tenant? Revoke access and rotate credentials if so.
- Are logs, backups, or exports affected?
- Does the fix need a reconciliation/backfill with sign-off?

Security incidents follow a different path: contain, preserve evidence, assess scope, notify per the
contract/regulation, rotate secrets, and involve the client's security owner. Do not investigate by
emailing production data around.

## 8. Regression test

Add a test that fails before the fix and passes after. For data defects, add a reconciliation check
or a patch test. Re-run the affected suite and the smoke list. Record the commands and results in
`assets/templates/delivery-test-note.md`.

## 9. Deployment and rollback

- Deploy through the normal release path, even for a hotfix.
- Take a backup before migrate if schema/data changes.
- Have a backout plan: revert code, restore DB/files, or forward-fix. State the data-loss window.
- For S1, consider maintenance mode to stop further damage while preserving evidence.
- After deploy, monitor errors, queue, scheduler, and the affected flow.

## 10. Client communication

Provide:

- Acknowledgment with severity and owner.
- Regular updates at the agreed cadence — even "no change yet".
- Clear workaround and impact statement.
- Resolution summary: cause, fix, verification, residual risk.
- Post-incident review for S1/S2 with preventive actions and owners.

Do not speculate publicly about cause before evidence. Do not promise a fix time you cannot meet.

## 11. Close-out

- Update release notes and documentation.
- Update the runbook if a check was missing.
- Add monitoring/alerting for the failure mode.
- Link the defect, RCA, patch, test, and release.
- Schedule a follow-up review for contributing factors.
- Keep the incident record per the client's retention policy.

## 12. Emergency rules

- Stabilize before diagnosing: stop the bleeding, preserve evidence, communicate.
- No destructive DB operations, no `reinstall`, no `drop-site`, no restore over production without
  explicit approval and a verified backup.
- No direct production code edits; deploy the reviewed fix.
- No secrets in tickets, chat, or logs.
- If you cannot verify the fix, say so and keep the incident open.

## 13. Checklist

- [ ] Intake complete: environment, versions, steps, expected/actual, impact.
- [ ] Severity assigned and communicated; owner named.
- [ ] Reproduced on a non-production copy, or evidence gap stated.
- [ ] Logs/traces collected and redacted.
- [ ] Root cause distinguished from trigger; contributing factors recorded.
- [ ] Minimal fix; data repair scripted, idempotent, and approved.
- [ ] Data integrity and security impact assessed.
- [ ] Regression test added; affected suite and smoke run.
- [ ] Backup taken; rollback path stated.
- [ ] Client updated; post-incident review scheduled for S1/S2.
- [ ] Docs, runbook, monitoring, and release notes updated.
