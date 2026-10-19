# White-label Discovery

**Purpose:** capture everything needed to scope a white-label/branding engagement before any file is
changed. Fill this in with the client, not for them.

**How to use:** copy into the client project (e.g. `docs/white-label/discovery.md`), fill every row,
mark anything unknown as `OPEN`, and get sign-off on the in-scope list.

---

## 1. Identity

| Item | Value |
|---|---|
| Client / legal entity | |
| Product name (user-facing) | |
| Tagline / short description | |
| Product owner (name, role) | |
| Brand guidelines document / link | |
| Approved logo files (light / dark / SVG / PNG / icon) | |
| Brand colours (hex), fonts | |
| Languages / locales in scope | |
| Timezone(s) / currency(ies) / date & number formats | |
| RTL required? | |

## 2. Tenancy and deployment

| Item | Value |
|---|---|
| Model | single-tenant per client / multi-tenant shared bench / shared site |
| Sites and environments | dev / staging / production (hostnames) |
| Frappe version | |
| ERPNext version | |
| Add-on apps and branches | |
| Who operates the system | |

## 3. Surface scope

Mark each surface `IN` or `OUT`. Anything marked `OUT` must still be verified as upstream-branded and
accepted by the client.

| Surface | Scope | Notes / owner |
|---|---|---|
| Desk navbar logo | | |
| App title / app icon / app metadata | | |
| Login page (logo, copy, footer) | | |
| Browser title / favicon | | |
| Website and portal (brand, nav, footer, copyright) | | |
| Home page and role-based landing | | |
| Apps/desktop screen app tile | | |
| Workspaces / sidebar labels | | |
| Emails (headers, footers, sender identity) | | |
| Notifications (in-app and email) | | |
| Print formats / letterhead / PDF | | |
| Exported documents (CSV/Excel) | | |
| Error / 404 pages | | |
| Terminology and translations | | |
| Client-specific CSS/JS | | |
| PWA / mobile manifest | | |
| Documentation / help links | | |
| Upstream attribution removal | | |

## 4. Terminology

| Upstream term | Client term | Where it appears | Method (label/translation/copy) |
|---|---|---|---|
| | | | |
| | | | |

> Do not rebrand by changing stored data values (statuses, DocType names). Change labels, copy, and
> translations.

## 5. Domains, email, and integrations

| Item | Value |
|---|---|
| Production hostname(s) | |
| Staging hostname(s) | |
| Sender name / address / domain | |
| SPF / DKIM / DMARC owner | |
| Client-specific integrations affected by branding | |

## 6. Constraints and licensing

| Question | Answer | Approved by |
|---|---|---|
| Is upstream attribution to be removed? | | |
| Is the product redistributed to third parties? | | |
| Who owns the custom code? | | |
| Licensing review required (ERPNext GPLv3, Framework MIT, trademark policy)? | | |
| Any legal/regulatory constraint on naming or claims? | | |

## 7. Verification and acceptance

| Item | Value |
|---|---|
| Who verifies each surface | |
| Verification environment | |
| Evidence required (screenshots, PDFs, email HTML, URLs) | |
| Sign-off date and approver | |

## 8. Open questions

| # | Question | Owner | Needed by | Status |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |

---

**Sign-off:** scope in §3 approved by ____________________ on __________
