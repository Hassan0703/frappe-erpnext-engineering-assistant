# Test Plan

**Purpose:** define what will be tested for a delivery, at which layer, by whom, and with what
evidence.

**How to use:** write before implementation finishes; keep it small enough to execute. For v15/v16 test
conventions, see `testing-and-qa.md` in the skill references.

---

## 1. Context

| Item | Value |
|---|---|
| Feature / release | |
| Requirement IDs | |
| Frappe / ERPNext versions | |
| Test environment / site | |
| Branch / revision | |
| Test owner | |
| Target test date | |

## 2. Scope

| In scope | Out of scope |
|---|---|
| | |

## 3. Risk assessment

| Area | Risk | Test depth | Reason |
|---|---|---|---|
| Money/ledger | high | unit + integration + reconciliation | Financial correctness |
| Permissions | high | integration as restricted user | Data exposure |
| Migration | high | dry run + reconciliation | Data loss |
| UI | medium | manual checklist | Usability |
| Reporting | medium | integration with real data | Wrong decisions |

## 4. Test cases

| # | Layer | Case | Preconditions | Steps | Expected | Actual | Status |
|---|---|---|---|---|---|---|---|
| 1 | unit | | | | | | |
| 2 | integration | | | | | | |
| 3 | permission | | | | | | |
| 4 | regression | | | | | | |
| 5 | manual | | | | | | |

Layers: unit, integration, permission, workflow/business rule, regression, migration, API failure,
background job, UI/branding, deployment smoke, backup/restore, performance, security.

## 5. Environment and data

| Item | Value |
|---|---|
| Test site (never production) | |
| Seed data / `before_tests` hook | |
| Anonymization required | |
| Versions of add-on apps | |
| PDF engine / Chromium available | |

## 6. Commands

```bash
bench --site <test_site> run-tests --app <app>
bench --site <test_site> run-tests --app <app> --module <app>.path.test_module
bench --site <test_site> run-tests --app <app> --doctype "<DocType>"
```

## 7. Entry and exit criteria

| Gate | Criteria |
|---|---|
| Entry | Code complete, review passed, environment ready |
| Exit | All in-scope cases executed; no open critical/high defects; failures documented |
| Evidence | Command output, screenshots, PDFs, reconciliation attached |

## 8. Defect handling

| Severity | Definition | Action |
|---|---|---|
| Critical | Data loss, security, or core flow broken | Block release |
| High | Major function broken | Fix or explicit acceptance |
| Medium | Degraded, workaround exists | Schedule |
| Low | Cosmetic | Backlog |

## 9. Results summary

| Item | Value |
|---|---|
| Cases planned / executed / passed / failed | |
| Skips and why | |
| Not run | |
| Open defects | |
| Residual risk | |
| Tested by / date | |
