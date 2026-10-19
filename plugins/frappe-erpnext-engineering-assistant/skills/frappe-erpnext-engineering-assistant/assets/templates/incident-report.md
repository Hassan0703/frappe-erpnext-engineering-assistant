# Incident Report

**Purpose:** a complete, evidence-based record of a production incident: what happened, what was done,
why, and what changes to prevent recurrence.

**How to use:** open immediately on detection; fill in as you go. Do not wait until resolution to
start recording. Redact secrets and unnecessary personal data.

---

## 1. Summary

| Item | Value |
|---|---|
| Incident ID | |
| Detected at (timezone) | |
| Resolved at | |
| Duration | |
| Severity (S1–S4) | |
| Environment / site / versions | |
| Detected by | |
| Incident lead | |
| Status | open / mitigated / resolved / monitoring |

**One-line description:**

## 2. Impact

| Dimension | Detail |
|---|---|
| Users affected (who, how many) | |
| Business processes stopped/degraded | |
| Financial impact / risk | |
| Data integrity affected? | |
| Security/privacy affected? | |
| Regulatory/contractual notification required? | |
| Workaround available | |

## 3. Timeline

| Time | Event / action | Actor | Evidence |
|---|---|---|---|
| | | | |
| | | | |

## 4. Investigation

| Question | Answer |
|---|---|
| Reproduction steps | |
| Affected documents/records/scope | |
| Logs inspected (paths) | |
| Error Log entries | |
| Database/queue state | |
| Recent changes (release, config, data) | |
| Ruled out (with evidence) | |

## 5. Root cause

- **Trigger:**
- **Root cause:**
- **Contributing factors:**
- **Why it was not caught earlier:**
- **Same defect elsewhere?** (other DocTypes/jobs/sites)

Distinguish hypothesis from confirmed cause. Attach evidence.

## 6. Recovery actions

| Time | Action | Approved by | Result | Reversible? |
|---|---|---|---|---|
| | | | | |

Data repair performed (patch/script reference, dry run, scope, row counts, idempotency):

```text

```

## 7. Verification

| Check | Method | Result |
|---|---|---|
| Core process works | | |
| Data integrity reconciled | | |
| Permissions/security intact | | |
| Scheduler and queue healthy | | |
| Regression test added | test name / location | |
| Monitoring/alert added | | |

## 8. Communication log

| Time | Audience | Channel | Message summary |
|---|---|---|---|
| | | | |

## 9. Prevention

| # | Action | Owner | Due date | Status |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |

## 10. Closure

| Item | Value |
|---|---|
| Closed by / date | |
| Post-incident review scheduled | |
| Documentation/runbook updated | |
| Release notes updated | |
| Follow-up monitoring until | |
| Residual risk | |
