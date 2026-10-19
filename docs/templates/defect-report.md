# Defect Report

**Purpose:** capture enough information to reproduce, triage, and fix a defect without a round trip.

**How to use:** fill from the reporter's information; do not accept "it doesn't work". Redact secrets
and unnecessary personal data from logs and screenshots.

---

## 1. Identification

| Item | Value |
|---|---|
| Defect ID | |
| Reported by / date | |
| Reporter role / client | |
| Severity (S1–S4) | |
| Component / DocType / feature | |
| Found in | production / staging / dev |
| Version under test | Frappe / ERPNext / apps |

## 2. Environment

| Item | Value |
|---|---|
| Site / URL | |
| Company / entity | |
| User + roles | |
| Browser / device | |
| Timezone | |
| First observed (with timezone) | |
| Intermittent or consistent? | |

## 3. Reproduction

| # | Step | Expected | Actual |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

Affected documents (names/IDs) — no unnecessary personal data:

```text

```

Cannot reproduce? State what evidence is missing.

## 4. Evidence

| Type | Reference / attachment |
|---|---|
| Error text / traceback | |
| Screenshot | |
| Error Log entry | |
| Server log excerpt (redacted) | |
| Browser console/network | |
| Related recent changes | |

## 5. Impact

| Dimension | Assessment |
|---|---|
| Users affected | |
| Business process affected | |
| Data integrity at risk? | |
| Security/privacy at risk? | |
| Financial impact | |
| Workaround available | |

## 6. Analysis (filled by the implementer)

| Item | Value |
|---|---|
| Confirmed severity | |
| Root cause (or hypothesis) | |
| Affected scope (records/companies/sites) | |
| Related defects / same pattern elsewhere | |
| Fix approach | |
| Data repair required | |
| Regression test added | |
| Rollback/backout considerations | |

## 7. Resolution

| Item | Value |
|---|---|
| Fix reference (commit/patch/release) | |
| Verified by / date | |
| Verification evidence | |
| Deployed to | |
| Client informed | |
| Documentation/runbook updated | |
| Follow-up monitoring | |

## 8. Triage decision

| Item | Value |
|---|---|
| Priority | |
| Target release | |
| Owner | |
| Accepted risk (if deferred) — approved by | |
