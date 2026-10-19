# Configuration Inventory

**Purpose:** list every configuration and customization that must exist for the system to work, how it
is reproduced, and who owns it. This is what makes a rebuild possible.

**How to use:** update whenever configuration changes. Flag anything applied manually — that is the
list that breaks a rebuild.

---

## 1. Context

| Item | Value |
|---|---|
| Client / project | |
| Environment(s) | |
| Frappe / ERPNext versions | |
| Owning app(s) | |
| Last verified on a fresh install | |
| Owner | |

## 2. Application code

| Item | Location | Source of truth | Deployed by |
|---|---|---|---|
| Custom app(s) | | repo + branch | release |
| Patches | `patches/` + `patches.txt` | repo | `migrate` |
| Client scripts (app) | | repo | release |
| Server scripts (app) | | repo | release |

## 3. Configuration records

Record how each is reproduced: fixture, patch, manual, or not reproducible (fix that).

| # | Item | DocType / setting | Reproduction method | Environment(s) | Owner | Reproducible? |
|---|---|---|---|---|---|---|
| 1 | Custom fields | Custom Field | fixture (module-filtered) | | | |
| 2 | Property setters | Property Setter | fixture | | | |
| 3 | Workflows | Workflow | fixture / patch | | | |
| 4 | Print formats | Print Format | app standard format | | | |
| 5 | Letterheads | Letter Head | fixture / patch | | | |
| 6 | Email templates | Email Template | fixture | | | |
| 7 | Notifications | Notification | fixture | | | |
| 8 | Roles / permissions | Role, DocPerm | fixture / patch | | | |
| 9 | Naming series | | patch / manual | | | |
| 10 | Company / chart of accounts | | manual / patch | | | |
| 11 | Taxes / UOM / warehouses | | fixture / manual | | | |
| 12 | Website/desk branding settings | Website Settings, Navbar Settings | patch / `after_install` | | | |
| 13 | Translations | app translation files | repo | | | |
| 14 | Scheduler events | `hooks.py` | repo | | | |
| 15 | Integrations / credentials | | secret store + settings | | | |

## 4. Manually applied configuration (risk list)

| # | Item | Where applied | Why manual | Risk on rebuild | Owner | Plan |
|---|---|---|---|---|---|---|
| 1 | | | | | | |

## 5. Environment-specific values

| Setting | Dev | Staging | Production | Stored where |
|---|---|---|---|---|
| Hostname | | | | |
| Email sender | | | | |
| Storage bucket | | | | |
| Provider keys | | | | |
| Branding assets | | | | |

## 6. Verification

| Check | Method | Date | Result |
|---|---|---|---|
| Fresh site + install app reproduces configuration | | | |
| Fixtures import without errors | | | |
| Patches run idempotently | | | |
| Permissions/workflows present after migrate | | | |

## 7. Sign-off

| Role | Name | Date |
|---|---|---|
| Implementer | | |
| Client owner | | |
