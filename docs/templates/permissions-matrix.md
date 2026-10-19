# Permissions and Workflow Matrix

**Purpose:** the single approved reference for who can do what, and how documents move between states.
Used for configuration, testing, audit, and handover.

**How to use:** fill with the business owner. Verify by testing with real restricted users — a matrix
that was never tested is a hypothesis.

---

## 1. Context

| Item | Value |
|---|---|
| Client / project | |
| Frappe / ERPNext versions | |
| Companies / entities in scope | |
| Prepared by / date | |
| Approved by (business) | |
| Segregation-of-duties reviewer | |

## 2. Roles

| Role | Purpose | Real job title(s) | Company scope | Territory/other scope |
|---|---|---|---|---|
| | | | | |

## 3. DocType permissions

| DocType | Role | Read | Write | Create | Submit | Cancel | Delete | permlevel | Report | Export | Import | Share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | |

Field-level restrictions (permlevel):

| DocType | Field | permlevel | Roles with access | Reason |
|---|---|---|---|---|
| | | | | |

## 4. Row-level scoping

| DocType | Rule | Mechanism | Tested with user | Result |
|---|---|---|---|---|
| | company/territory/user scoped | user permission / `permission_query_conditions` / `has_permission` | | |

## 5. Workflow states and transitions

| State | Allowed roles | Next states | Actions available | Notifications |
|---|---|---|---|---|
| Draft | | | | |
| Pending Approval | | | | |
| Approved | | | | |
| Rejected | | | | |
| Cancelled | | | | |

| Transition | From → To | Who | Conditions | Enforced where | Reject path |
|---|---|---|---|---|---|
| | | | | server | |

## 6. Segregation of duties

| Control | Intent | Who performs | Who approves | Conflict risk | Mitigation |
|---|---|---|---|---|---|
| Payment approval | creator ≠ approver | | | | |
| Permission changes | not self-approved | | | | |
| Master data changes | reviewed | | | | |

## 7. Verification

| # | Scenario | User (role) | Expected | Actual | Pass/Fail | Evidence |
|---|---|---|---|---|---|---|
| 1 | User cannot read other company's document | | denied | | | |
| 2 | Approver can submit, clerk cannot | | | | | |
| 3 | Sensitive field hidden at permlevel | | | | | |
| 4 | Whitelisted method denied to unauthorized user | | | | | |
| 5 | Workflow bypass attempt via API denied | | | | | |

## 8. Sign-off

| Role | Name | Date | Notes |
|---|---|---|---|
| Business owner | | | |
| Security/SoD reviewer | | | |
| Implementer | | | |
