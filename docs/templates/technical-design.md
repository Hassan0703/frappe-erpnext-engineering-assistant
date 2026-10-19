# Technical Design

**Purpose:** record the technical decisions behind a change so the next developer understands what was
built, why, and what was rejected — including version-specific choices.

**How to use:** one document per significant feature or module. Keep it short but specific.

---

## 1. Summary

| Item | Value |
|---|---|
| Feature / module | |
| Requirement IDs | |
| Frappe / ERPNext versions | |
| Owning app | |
| Author / date | |
| Reviewers | |

## 2. Requirement

What business problem does this solve? Which requirements does it satisfy, and which does it
explicitly not address?

## 3. Options considered

| # | Option | Pros | Cons | Chosen? |
|---|---|---|---|---|
| 1 | Standard configuration | | | |
| 2 | Extend existing DocType | | | |
| 3 | New DocType/app | | | |
| 4 | Core modification | | | |

**Decision and reason:**

## 4. Data model

| DocType | New/modified | Key fields | Links | Naming | Notes |
|---|---|---|---|---|---|
| | | | | | |

Parent/child relationships, indexes, and status model (`docstatus` vs business status):

```text

```

## 5. Behaviour

| Event | Action | Where enforced (server/client) |
|---|---|---|
| validate | | |
| on_submit | | |
| on_cancel | | |
| scheduled / job | | |

## 6. Permissions

| Role | DocType | read | write | create | submit | cancel | permlevel | Notes |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

Row-level scoping (`permission_query_conditions`, user permissions, company scope):

```text

```

## 7. Version-specific decisions

| Area | v15 approach | v16 approach | What we implement | Why |
|---|---|---|---|---|
| Class extension | | | | |
| Query building | | | | |
| Print/PDF | | | | |
| Translations | | | | |
| Other | | | | |

## 8. Integration contracts

| Integration | Direction | Trigger | Payload | Auth | Retry/timeout | Idempotency | Failure handling | Owner |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

## 9. Security considerations

- Authorization checks:
- Data exposure:
- Secrets handling:
- Input validation / sanitization:
- Audit trail:

## 10. Testing plan

| Layer | Test | Location |
|---|---|---|
| Unit | | |
| Integration | | |
| Permission | | |
| Regression | | |

## 11. Deployment and rollback

| Item | Value |
|---|---|
| Patches/fixtures included | |
| Migration needed | |
| Post-deploy steps (migrate/build/restart) | |
| Rollback method | |
| Data-loss window | |

## 12. Known limitations and follow-ups

| # | Item | Impact | Owner | Target |
|---|---|---|---|---|
| 1 | | | | |

## 13. Approval

| Role | Name | Date |
|---|---|---|
| Technical reviewer | | |
| Business owner | | |
