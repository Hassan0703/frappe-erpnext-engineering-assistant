# Delivery Test Note

**Purpose:** the short written record accompanying every delivery: what was tested, how, what actually
happened, and what was not tested.

**How to use:** one note per delivery/change. Fill it with observed results. If a check was not run,
write "not run" and why — never imply a pass.

---

## 1. Delivery

| Item | Value |
|---|---|
| Delivery / change ID | |
| Requirement IDs | |
| Environment | |
| Frappe / ERPNext versions | |
| Apps / revision / tag | |
| Date | |
| Delivered by | |

## 2. What changed

| File / artifact | Change | Why this location |
|---|---|---|
| | | |

## 3. Requirements tested

| Requirement ID | Acceptance criteria | Result | Evidence |
|---|---|---|---|
| | | pass / fail / partial | |

## 4. Test cases and results

| # | Type | Case | Expected | Actual | Result | Evidence |
|---|---|---|---|---|---|---|
| 1 | automated | | | | | |
| 2 | manual | | | | | |
| 3 | permission | | | | | |

Type: automated test, manual check, permission/authorization, migration, deployment smoke, UAT.

## 5. Commands and outputs

```bash
# paste the exact commands run and the observed result summary
bench --site <site> run-tests --app <app>
# result: <N tests, X failures — paste the failure text if any>
```

| Command | Exit status | Observed result |
|---|---|---|
| | | |

## 6. What was NOT tested

| Item | Why | Risk |
|---|---|---|
| | no bench available / no staging / out of scope | |

## 7. Failures, limitations, and outstanding risks

| # | Item | Severity | Impact | Owner | Target |
|---|---|---|---|---|---|
| 1 | | | | | |

## 8. Environments note

| Item | Value |
|---|---|
| Automated tests run? | yes/no |
| Manual checks run? | yes/no |
| Client UAT recorded separately? | link |
| Production verification | not performed / performed on <date> |

## 9. Post-delivery actions for the client

```text
[ ] bench --site <site> migrate
[ ] bench build
[ ] clear cache / restart services
[ ] other:
```

## 10. Sign-off

| Role | Name | Date |
|---|---|---|
| Developer | | |
| Reviewer | | |
