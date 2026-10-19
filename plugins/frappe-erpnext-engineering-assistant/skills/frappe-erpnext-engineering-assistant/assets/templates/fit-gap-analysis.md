# Fit-Gap Analysis

**Purpose:** decide, per requirement, whether to use standard functionality, configure, extend, or
build — with the cost and upgrade risk recorded.

**How to use:** fill one row per requirement from `requirements-and-acceptance.md`. The standard-first
order is not a preference; deviations need a stated reason.

---

## Engagement

| Item | Value |
|---|---|
| Client / project | |
| Frappe / ERPNext versions | |
| Prepared by / date | |
| Business owners consulted | |

## Decision order

Always evaluate in this order and record where the requirement landed:

1. **Standard feature/config** — settings, workflows, permissions, naming series, print formats, reports.
2. **Standard extension** — custom fields, property setters, notifications, app client scripts.
3. **Small custom logic** — controller hooks, whitelisted methods, script reports.
4. **New DocType/app** — only when no equivalent exists.
5. **Core modification** — last resort; not upgrade-safe; explicit approval required.

## Analysis

| ID | Requirement | Standard fit? | Gap | Chosen response | Rejected alternatives + reason | Effort | Upgrade risk | Upgrade-safe? | Owner | Approved |
|---|---|---|---|---|---|---|---|---|---|---|
| R-001 | | yes/partial/no | | configure / field / workflow / report / custom logic / new DocType / core | | S/M/L | low/med/high | yes/no | | |
| R-002 | | | | | | | | | | |

## Customization summary

| Type | Count | Notes |
|---|---|---|
| Configuration only | | |
| Custom fields | | |
| Workflows | | |
| Reports | | |
| Custom app logic | | |
| New DocTypes | | |
| Core modifications | | |

> Core modifications require: the business justification, the maintenance cost, who owns the fork, and
> how upgrades will be handled. Record the approval.

## Challenges to raise with the client

| # | Proposed customization | Question to raise | Outcome |
|---|---|---|---|
| 1 | Custom field duplicating a standard field | Can standard be used? | |
| 2 | New DocType that mirrors a standard document | Which standard process is missing? | |
| 3 | Approval enforced only in JavaScript | Who must not be able to bypass it? | |
| 4 | Report duplicating a standard report | Which standard metric differs, and why? | |

## Risks introduced by customizations

| # | Risk | Impact | Mitigation | Owner |
|---|---|---|---|---|
| 1 | | | | |

## Approval

| Role | Name | Date |
|---|---|---|
| Business owner | | |
| Technical lead | | |
