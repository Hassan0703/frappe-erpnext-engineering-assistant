# UAT and Sign-off

**Purpose:** record business acceptance testing executed by the client, with real evidence and an
explicit decision. UAT is not a developer smoke test.

**How to use:** scripts are written in business language; the client's named users execute them; the
implementer observes and records. Do not record sign-off that did not happen.

---

## 1. Context

| Item | Value |
|---|---|
| Client / project | |
| Release / version under test | |
| Environment / URL | |
| Frappe / ERPNext versions | |
| UAT window | |
| Test coordinator | |
| Business owner (signer) | |
| Test data used | production-like / anonymized / synthetic |

## 2. Scope

| In scope | Out of scope |
|---|---|
| | |

## 3. Participants

| Name | Role | Module(s) tested | Signature date |
|---|---|---|---|
| | | | |

## 4. Scripts and results

| # | Scenario (business language) | Role | Steps | Expected result | Actual result | Status | Evidence |
|---|---|---|---|---|---|---|---|
| 1 | Create and approve a purchase order | Approver | | | | pass/fail/blocked | |
| 2 | Reject an order and verify notification | Approver | | | | | |
| 3 | Verify a user cannot see another company's invoices | Sales user | | | | | |
| 4 | Print an invoice PDF with correct letterhead | Finance | | | | | |
| 5 | Run the outstanding report and compare to source | Finance | | | | | |
| 6 | Receive a purchase and check stock | Store keeper | | | | | |

Status values: `pass`, `pass with observation`, `fail`, `blocked`, `not tested`.

## 5. Defects

| # | Defect | Severity | Steps | Impact | Owner | Status | Retest result |
|---|---|---|---|---|---|---|---|
| 1 | | | | | | | |

## 6. Non-functional checks

| Check | Result | Evidence |
|---|---|---|
| Response time acceptable on realistic data | | |
| Permissions verified with restricted users | | |
| Reports match expected figures | | |
| Print/PDF correct | | |
| Integration flow end-to-end | | |
| Branding surfaces correct | | |

## 7. Open items and risks

| # | Item | Impact | Owner | Target date | Accepted by client? |
|---|---|---|---|---|---|
| 1 | | | | | |

## 8. Decision

| Item | Value |
|---|---|
| UAT outcome | approved / approved with conditions / rejected |
| Conditions | |
| Go-live readiness | |
| Outstanding risks accepted by | |

## 9. Sign-off

| Role | Name | Date | Signature / confirmation reference |
|---|---|---|---|
| Business owner | | | |
| Test coordinator | | | |
| Implementer | | | |
