# White-label Implementation Plan

**Purpose:** the approved plan for making a Frappe/ERPNext deployment carry the client's product
identity, with change classification, affected files, testing, and rollback.

**How to use:** fill after `white-label-discovery.md` is signed off. Every change must be classified
before implementation. Keep this file under version control with the client project.

---

## 1. Summary

| Item | Value |
|---|---|
| Client / product name | |
| Engagement / ticket ID | |
| Frappe / ERPNext versions | |
| Environments in scope | |
| Target date | |
| Owner | |
| Discovery reference | |

## 2. Branding inventory

One row per asset or identity element. "Reproducible" means a fresh site gets it without manual steps.

| # | Asset / element | Source (file, URL, hex) | Target mechanism | Reproducible? | Environment(s) | Owner |
|---|---|---|---|---|---|---|
| 1 | Logo (desk) | | | yes/no | | |
| 2 | Logo (login) | | | | | |
| 3 | Favicon | | | | | |
| 4 | App icon / title | | | | | |
| 5 | Email footer | | | | | |
| 6 | Letterhead / print | | | | | |
| 7 | Terminology | | | | | |

## 3. Technical decisions

| # | Decision | Chosen approach | Alternatives rejected | Reason | Risk / maintenance cost |
|---|---|---|---|---|---|
| 1 | | configuration / custom app / hook / patch / fork | | | |
| 2 | | | | | |

Classification reminder:

- **Configuration-only** — settings, letterhead, templates. Upgrade-safe; must be reproduced per
  environment.
- **Custom app / supported hook** — versioned and reproducible. Preferred.
- **Patch / migration** — for existing sites; must be idempotent.
- **Framework fork / core edit** — not upgrade-safe; requires explicit approval and a maintenance plan.

## 4. Affected files

| File / artifact | App | Change | Version-sensitive? |
|---|---|---|---|
| | | new / modified | |

## 5. Version notes

| Area | v15 behavior | v16 behavior | What we implement |
|---|---|---|---|
| Print/PDF | | | |
| Translations | | | |
| Desk route / navigation | | | |
| App tile registration | | | |

## 6. Dependencies

| Dependency | Owner | Status | Needed by |
|---|---|---|---|
| Final assets (logo, favicon) | | | |
| Written licensing/trademark approval | | | |
| Sender domain access | | | |
| Staging environment | | | |
| Chromium installed for PDFs (v16) | | | |

## 7. Testing and verification

| Surface | How verified | Evidence | Result |
|---|---|---|---|
| Desk | | screenshot | |
| Login | | screenshot | |
| Portal/website | | URL + screenshot | |
| Email | | rendered HTML | |
| Print/PDF | | PDF | |
| Cache/build/migrate persistence | | commands + screenshots | |

Full checklist: `white-label-verification.md`.

## 8. Rollback

| Item | Value |
|---|---|
| Backout method (revert commit / restore settings / patch) | |
| Data affected (settings, records) | |
| Time to revert | |
| Who approves rollback | |

## 9. Acceptance criteria

- [ ] Every `IN` surface from discovery shows client branding with no upstream brand visible.
- [ ] Out-of-scope surfaces are documented and accepted.
- [ ] Branding persists after `clear-cache`, `bench build`, and `migrate`.
- [ ] A fresh site install reproduces branding without manual steps (or the manual steps are documented).
- [ ] Email and PDF outputs verified, not just the desk.
- [ ] Licensing/trademark questions resolved or explicitly deferred with a named owner.
- [ ] Upgrade checklist completed and attached.

## 10. Approvals

| Role | Name | Date | Notes |
|---|---|---|---|
| Client product owner | | | |
| Implementer | | | |
| Licensing reviewer (if required) | | | |
