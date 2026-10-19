# Project Discovery and Technical Audit

Use before planning any change on an existing Frappe/ERPNext project, and again before a large
release or upgrade. Record what you observed and how you observed it. Never fill a field with an
assumption: write "unknown" and what would confirm it.

> Never paste credentials, API keys, database dumps, customer data, or full production config values
> into this document. Record where a secret lives, not its value.

## 1. Engagement and environment

| Item | Value | How verified |
|---|---|---|
| Client / project | | |
| Environment audited (dev / staging / production) | | |
| Site name (or "redacted") | | |
| Audit date | | |
| Auditor | | |
| Change or release this audit supports | | |

## 2. Versions and applications

Record the exact evidence (command output or file path), not just "latest".

| Item | Value | Evidence |
|---|---|---|
| Frappe version | | `bench version` |
| ERPNext version | | `bench --site <site> list-apps` |
| Custom app(s) and versions | | |
| Third-party apps (HRMS, Lending, Payments, …) | | |
| Database engine and version | | |
| Python / Node runtime | | |
| PDF engine / Chromium path | | |
| Redis and worker topology | | |

Frappe and ERPNext must share a major version; add-on apps must declare a compatible branch.

## 3. Repository and deployment state

| Item | Value | Notes |
|---|---|---|
| Owning repository / remote | | |
| Branch and commit under audit | | |
| Working tree clean? | | uncommitted work is a risk |
| Ownership of each app (ours vs vendor) | | |
| How changes reach staging/production | | CI, manual deploy, … |
| `developer_mode` state in production | | must be off |
| Backup schedule and last successful restore test | | a schedule is not a restore |

## 4. Customization inventory

List each customization, where it lives, and whether it is reproducible.

| # | Customization | Type (config / fixture / hook / app code / patch / site script) | Location | Reproducible on a fresh site? | Upgrade risk |
|---|---|---|---|---|---|
| 1 | | | | yes / no / unknown | |
| 2 | | | | | |

Watch for: Custom Fields, Property Setters, Workflows, Notifications, Print Formats, Reports,
Client Scripts, Server Scripts, custom apps, overrides, and manually applied settings.

## 5. DocTypes and data model

| Item | Value |
|---|---|
| DocTypes owned by the client's app | |
| Vendor DocTypes extended (and how) | |
| Single DocTypes carrying configuration | |
| Child tables and their parents | |
| Known integrity or reconciliation issues | |
| Data volume of the largest tables | |

## 6. Permissions and access control

| Item | Value |
|---|---|
| Roles in use | |
| Custom DocPerm / role changes | |
| User Permissions (row-level scope) | |
| `permlevel` fields protecting sensitive data | |
| Guest / website users and public endpoints | |
| Administrator-only areas and who else has access | |

## 7. Integrations, jobs, and scheduled work

| # | Integration / job | Direction | Auth | Retry / timeout | Owner | Monitoring |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |

Also record: scheduler enabled, job backlog, queues in use, and any job that writes data.

## 8. Reports, print, and output

| Item | Value |
|---|---|
| Critical reports and their owners | |
| Report scope (company / permissions) | |
| Print formats in use (classic vs editor/Jinja) | |
| Letterheads per company | |
| Emails and notification templates | |
| Exports used by the business | |

## 9. Branding surfaces (if in scope)

Use `white-label-discovery.md` for the full inventory. Record here only whether branding work is in
scope for this change: yes / no / unknown.

## 10. Testing and evidence

| Item | Value |
|---|---|
| Test command used by the team | |
| Existing automated tests (where, how many) | |
| Test site availability (disposable?) | |
| Manual/UAT owners | |
| Evidence stored where | |
| Last known good version/tag | |

## 11. Risk register

| # | Risk | Impact | Likelihood | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |

## 12. Unknowns and follow-ups

| # | Unknown | Impact if wrong | How to resolve | Owner | Due |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |

## 13. Audit conclusion

- Version-sensitive conclusions are based on: `<source / command / runtime evidence>`
- Unverified items carried forward: `<list>`
- Recommended change risk class (see `deployment-and-operations.md`): `<1–4>`
- Recommended next step and approver: `<...>`
