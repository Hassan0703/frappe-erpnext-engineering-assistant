# White-Labeling and Product Identity

White-labeling is not "change the logo". It is a controlled product-identity change across every
surface a client's users, customers, and auditors see — while keeping upgrades safe. Treat it as a
small implementation project with a scope, an inventory, a verification pass, and a rollback plan.

**Scope reminder:** Frappe/ERPNext v15 and v16 only. Detect the version first
(`version-compatibility.md`). Branding mechanisms differ between versions.

## 1. Discovery before implementation

Answer these before touching a file. Use `assets/templates/white-label-discovery.md`.

1. **Who is the product for?** Client name, product name, tagline, legal entity, locales.
2. **Tenancy:** single-tenant per client, multi-tenant shared bench, or a shared site? This decides
   whether branding is per-site configuration or per-tenant data.
3. **Which surfaces are in scope?** Desk, login, website/portal, emails, notifications, print/PDF,
   app tiles, PWA, error pages, docs, API responses, exported files.
4. **Which surfaces are explicitly out of scope?** Write this down; it prevents UAT surprises.
5. **Assets:** logo (light/dark, SVG/PNG), favicon, app icon, splash image, brand colors, fonts.
   Get written usage rights and the required sizes.
6. **Terminology:** which upstream terms must change (product name, module names, email copy,
   "Powered by" text)? Which must remain for legal or support reasons?
7. **Localization:** languages, timezone, currency, date/number formats, right-to-left support.
8. **Domains and email:** production/staging hostnames, sender domains, SPF/DKIM ownership.
9. **Constraints:** is the client allowed to remove upstream attribution? Is the product
   redistributed to third parties? (See §9.)
10. **Verification owner:** who signs off each surface, and in which environment?

If any of 1–4 is unknown, stop. Branding without a surface inventory always misses email or print.

## 2. Safe-change classification

Classify every intended change before implementing it. Prefer the top of this list.

| Class | Examples | Upgrade safety | Use when |
|---|---|---|---|
| **1. Configuration-only (standard settings)** | Website Settings brand fields, Navbar Settings `app_logo`, Letter Head, Email Template, Print Format record, Translation record | Good, but stored in DB and must be reproduced per environment | The surface is designed to be configured |
| **2. Supported custom-app mechanism** | App metadata in `hooks.py`, assets under `public/`, app `templates/emails/`, website templates, app translation files, app CSS/JS bundles | Good; versioned in your app | You need reproducibility, multiple sites, or version control, and no framework hook is required |
| **3. Hook or fixture** | `app_logo_url`, `brand_html`, `add_to_apps_screen`, `website_context`, `default_mail_footer`, `app_include_css` / `web_include_css`; Custom Field and Property Setter fixtures | Good; versioned in the app. Fixtures are records, so review what they overwrite on migrate | The surface exposes a documented hook, or a record must exist on every site |
| **4. Patch / migration** | Set a Single DocType value, create a Letter Head, backfill a setting | Good if idempotent; runs on migrate | Existing sites need the change applied consistently and no hook or fixture can express it |
| **5. Framework fork / core modification** | Editing `apps/frappe/...` templates or assets | **Poor**; overwritten on upgrade | Almost never; requires explicit approval and a maintenance plan |

Classes 2 and 3 are both app-level, but they fail differently: hook values are code and fail at
import or boot; fixtures are records and fail at sync or merge. Test both on a fresh site **and**
after `bench --site <site> migrate`.

Rules:

- Do not edit files inside `apps/frappe`, `apps/erpnext`, or another vendor app. Use hooks,
  templates in your own app, and configuration.
- Do not claim a core edit is "upgrade-safe" because it worked locally. Upgrades overwrite it.
- Do not rely on a database-only change that no one can reproduce. Record it in a patch, fixture, or
  the environment runbook.
- Do not assume a Single DocType exports cleanly as a fixture. `Website Settings` and `Navbar
  Settings` are Singles; verify `export-fixtures` behavior on your version. If it does not round-trip,
  apply values in `after_install`/a patch with `frappe.db.set_single_value(...)` and document it.
  *(Unverified: fixture support for Single DocTypes.)*

### 2.1 Decision tree

Pick the least invasive mechanism that works, in this order, and stop at the first that applies:

1. **Supported setting or record** — Website Settings, Navbar Settings, Letter Head, Email Template,
   Translation record, Print Format record. Configuration is intended to be configured; reproduce it
   per environment.
2. **Documented hook** — `app_logo_url`, `brand_html`, `add_to_apps_screen`, `website_context`,
   `default_mail_footer`, `app_include_css` / `web_include_css`, or another verified hook. Versioned in
   the custom app.
3. **Custom-app asset, template, or metadata** — `public/` assets, `templates/emails/`, website
   templates, app translation files, app `hooks.py` metadata. Also versioned.
4. **Fixture or patch** — a record must exist on every site and no hook sets it. Fixtures for DocType
   records (with a module filter); an idempotent patch/`after_install` for Single DocType values that
   do not round-trip. Always verify on a fresh site **and** after `migrate`.
5. **Framework fork / core modification** — only framework source can express it. Stop: this needs
   explicit written approval and a maintenance plan, and it is overwritten on upgrade. Prefer
   re-scoping the requirement or raising it with the client.

If two mechanisms work, choose the one earlier in this list. If the client's deployment model forces
site-level scripts, that is a documented exception, not an equivalent.

## 3. Surface inventory

For each row: inspect the installed version, implement with the listed mechanism, then verify.
Field names below are described by purpose because they can differ between releases — confirm the
exact `fieldname` in the installed DocType JSON before writing code.

How to read this inventory against the seven things each surface must document:

| Required detail | Where it is recorded |
|---|---|
| Supported implementation method | The `Mechanism` column of each table below |
| Application / configuration locations | The `Mechanism` and `Notes` columns (DocType settings, hooks, app paths) |
| v15 vs v16 difference | §4 *Version differences that change the plan* (per-area rows) |
| Required hooks, fixtures, configuration | The `Mechanism` column (hook name, setting, DocType, or app asset); §2 for fixtures vs patches on Single DocTypes |
| Dependencies and limitations | §2 classification table, §3 notes, §9 legal boundary |
| Verification steps | The `Verification` column where the table has one; otherwise the surface checklist in §6 |
| Upgrade and maintenance implications | §7 *Upgrade and maintenance implications*, and the upgrade checklist template |

### 3.1 Application identity and metadata

| Item | Mechanism | Notes |
|---|---|---|
| App title / publisher / description | Custom app's `hooks.py` (`app_title`, `app_publisher`, `app_description`, `app_version`) | Versioned; shown in About and app listings |
| App icon / color | `add_to_apps_screen` (logo, title, route) for the visible app tile; `app_logo_url` for the desk logo. `app_icon` and `app_color` are legacy ERPNext hooks: ERPNext declares both, but Frappe core 15.94 and 16.16 do not read them for the app tile — the tile uses the `add_to_apps_screen` entry (`logo`) | Verified in source (15.94.1, 16.16.0). Do not rely on `app_icon` / `app_color` for a visible logo; check the installed version if a theme or add-on reads them |
| Desk app logo | `app_logo_url` hook, or Navbar Settings `app_logo` | Hook is version-controlled; setting is per-site |
| App tile on the apps screen | `add_to_apps_screen` hook (v15 and later) with `name`, `logo`, `title`, `route`, optional `has_permission` | v16 shows these on the desktop screen; v15 on `/apps` |
| Product naming in docs/help links | Custom app templates/links | Do not break support links the client needs |

### 3.2 Desk, navbar, and login

| Item | Mechanism | Verification |
|---|---|---|
| Desk navbar logo | Navbar Settings `app_logo`; or `app_logo_url` hook | Log in, hard-refresh, check navbar |
| Login page logo/brand | Login template + brand context. Inspect the installed login template (commonly `apps/frappe/frappe/www/login.html`) and the settings it reads; confirm which of Website Settings / Navbar Settings supplies the logo on your version | Open `/login` in a private window; check logo, title, footer |
| Login page copy/legal links | Custom app template override or supported context | Same |
| Favicon | Website Settings favicon and/or `website_context = {"favicon": ...}` | Check tab icon on desk, website, login |
| Brand colors/theme | Website Theme / custom CSS bundle via `app_include_css` (desk) and `web_include_css` (website/portal) | Check desk + portal, light/dark if supported |
| Browser/product title | Inspect `base.html`/desk boot payload; `app_title` and site name contribute | Check tab title on login, desk, portal |

Do not hardcode a logo URL in JavaScript. Use settings or a hook so staging and production can differ.

### 3.3 Website and portal

| Item | Mechanism | Verification |
|---|---|---|
| Brand name / brand HTML | Website Settings brand fields (`brand_html` hook if you need version control) | Public homepage, portal, login |
| Logo / splash / favicon | Website Settings brand section | Public and authenticated pages |
| Navbar/footer links and copyright | Website Settings top bar/footer items | All public pages |
| Home page and role-based landing | Website Settings `home_page`; `role_home_page` and `get_website_user_home_page` hooks | Log in as each role |
| Custom base template | `base_template` / `base_template_map` hooks | Every route that uses it |
| Portal sidebar | `portal_menu_items` / `standard_portal_menu_items` | Customer/supplier portal |
| Error pages | App `www/404.html` override (Frappe resolves `www/<path>.html` across installed apps) or a custom error template; `website_route_rules` / `website_redirects` for routing | Visit a missing route |

The hooks documentation notes that `brand_html` should be used when you want the brand
version-controlled; otherwise Website Settings is the intended mechanism.

### 3.4 Email and notifications

| Item | Mechanism | Verification |
|---|---|---|
| Global email footer | `default_mail_footer` hook | Send a test email; inspect HTML source |
| Sender identity | `get_sender_details` hook; Email Account configuration | Check From name/address |
| Transactional templates | Email Template records; app `templates/emails/` | Trigger each notification, inspect rendered email |
| Notification copy | Notification DocType / notification templates | Trigger and inspect |
| Provider integration | `override_email_send` (only if using a provider) | Send through the provider; check status handling |
| Unsubscribe/legal footer | Template + settings | Confirm legally required text is present |

Email is the most commonly forgotten surface. Include it in the surface inventory and in UAT.

### 3.5 Print, PDF, and exported documents

| Item | Mechanism | Verification |
|---|---|---|
| Letterhead (logo, address, footer) | Letter Head DocType; assign per company | Render a document with each company |
| Print format layout/branding | Print Format (HTML/Jinja) or v16 Print Format Editor | Render PDF, inspect header/footer/logo |
| PDF engine | v15: wkhtmltopdf; v16: Chromium (editor formats), `bench setup-chrome` / `chromium_path` | First PDF generation on a cold server |
| Document CSS | v16 converted formats use `.print-format-doc`, `.section`, `.field .label`, `.field .value`; classic `.print-format`, `.section-break`, `.data-field` styles need rewriting | Compare before/after conversion |
| Exports | CSV/Excel exports are data, not branded documents | Confirm scope with the client |

v16 deprecates classic print formats; new ones cannot be created there and upstream states they stop
working in v17. Convert standard formats in developer mode, save, and re-test. Do not promise
classic-format longevity.

### 3.6 Terminology and translations

| Version | Mechanism |
|---|---|
| v15 | CSV translation files; `bench new-language`, `bench update-translations`, `bench build-message-files` |
| v16 | Gettext PO/MO; `bench generate-pot-file`, `bench update-po-files`, `bench compile-po-to-mo`, `bench migrate-csv-to-po` |

- Override terminology in the app's translation files, not by editing framework source.
- v16 deprecates the view-specific `get_translated_dict` helper: v16.16 keeps it only as a shim in
  `frappe/deprecation_dumpster.py` (removal slated for v17), so new code must not use it. Put strings
  in app translation files.
- Do not translate data values (status names stored in the DB) to rebrand them. Rename the label or
  provide a mapping; changing stored values breaks reports and integrations.
- After changing translations, rebuild and clear caches, then verify in the target language.

### 3.7 Static assets and custom CSS/JS

- Brand assets live in the custom app's `public/` tree and are served under `/assets/<app>/...` after
  `bench build`.
- Desk-wide CSS/JS: `app_include_css` / `app_include_js`. Website-wide: `web_include_css` /
  `web_include_js`. Web forms: `webform_include_css` / `webform_include_js`.
- Keep overrides small and namespaced (e.g. `.client-brand ...`) to survive upgrades.
- Do not replace framework asset files in place.
- Verify assets return 200 and the browser console has no 404s after build and cache clear.

### 3.8 PWA / mobile

If the client requires an installable app or offline behavior, confirm what the target version
supports before promising it. Manifest/service-worker support is not uniform across versions and
deployment models; treat it as custom-app work with its own verification. *(Unverified for specific
v15/v16 patch levels.)*

## 4. Version differences that change the plan

| Area | v15 | v16 | Branding consequence |
|---|---|---|---|
| Desk route | `/app` | `/desk` | Update links, redirects, screenshots, training |
| Apps screen | `/apps` | Deprecated; desktop screen + sidebar | App tile must be registered via `add_to_apps_screen`; test the v16 desktop |
| Navigation | Workspaces | Persistent sidebar (`Workspace Sidebar`) + desktop | Curate sidebars; don't rely on modified standard workspaces (they are overwritten on migrate) |
| Print/PDF | wkhtmltopdf, classic formats | Chromium, Print Format Editor, classic deprecated | Branding via letterhead/print format needs conversion and Chromium provisioning |
| Translations | CSV | PO/MO | Terminology workflow and bench commands differ |
| Sanitization | bleach | nh3 | Rich-text brand copy may render differently |
| Email commit behavior | `sendmail(now=True)` commits | Does not commit | Test notification flows after upgrade |

## 5. Implementation sequence (recommended)

1. Freeze scope using the discovery checklist. Record out-of-scope surfaces.
2. Capture a **before** baseline: screenshots of desk, login, portal, an email, and a PDF, plus a
   list of asset URLs and their HTTP status.
3. Implement configuration-level changes first (settings, letterhead, templates).
4. Implement app-level changes (hooks, assets, translations) in the custom app.
5. Add a patch/`after_install` for anything existing sites need but cannot get from a fixture.
6. Build assets, migrate, clear caches, restart workers.
7. Run the verification procedure (§6). Record evidence per surface.
8. Repeat in staging with production-like data; compare.
9. Write the upgrade checklist entry (§7) and hand over ownership of assets/credentials.

## 6. Verification procedure

Run in a **private window** and, where possible, as a non-Administrator user.

```text
[ ] Login page: logo, title, favicon, footer, no upstream brand
[ ] Desk: navbar logo, app title, favicon, theme colors, sidebar/workspace labels
[ ] Apps/desktop screen: correct app tile, icon, title, route
[ ] Portal/website: brand, nav, footer, copyright, home page
[ ] Email: From name/address, header, footer, legal text, links
[ ] Notification: rendered copy and links
[ ] Print/PDF: letterhead, logo, header/footer, page break, fonts
[ ] Assets: every brand URL returns 200; console has no 404s
[ ] Translations: target language shows the new terminology
[ ] Mobile/narrow viewport: no clipped logo or broken nav
[ ] Error page: branded, no stack trace
[ ] Cache: hard refresh after clear-cache; result persists
[ ] Rebuild: `bench build`; result persists
[ ] Migrate: `bench --site <site> migrate`; result persists
[ ] Fresh site install (if the app ships branding): result appears without manual steps
```

Useful checks:

```bash
bench --site <site> clear-cache
bench --site <site> clear-website-cache
bench build --app <app>
curl -sI https://<host>/assets/<app>/images/logo.png | head -1
```

Compare rendered HTML for leftover upstream names:

```bash
curl -s https://<host>/login | grep -i "<upstream-brand>" && echo "FOUND"
```

Do not declare branding complete from the desk alone. Email and PDF are separate render paths.

## 7. Upgrade and maintenance implications

- **Standard workspaces are overwritten on v16 migrate.** Back up customizations and re-apply them as
  private/standard workspaces in your app.
- **Assets must be rebuilt** (`bench build`) after changing `public/` or include hooks; clear caches
  afterwards.
- **Classic print formats** are deprecated in v16; conversion changes CSS selectors and the PDF
  engine.
- **Translation format** changed in v16; keep the source of truth in the format the target version
  uses.
- **Singles are not guaranteed to travel via fixtures.** If branding is applied by patch, keep the
  patch idempotent and record it in the deployment runbook.
- **Branding is environment-specific.** Staging and production may intentionally differ; never copy
  production credentials or customer assets into staging.
- Add every branded surface to `assets/templates/white-label-upgrade-checklist.md` and run it after
  every upgrade.

## 8. Multi-tenant and multi-site

- Prefer **one site per tenant**. Branding then lives in that site's settings, assets, and email
  configuration.
- If tenants share a site, branding must be data-driven (per-company/tenant fields and templates) and
  tested for cross-tenant leakage in emails, PDFs, and portal pages.
- Never let one tenant's logo, sender address, or domain appear in another tenant's documents.
- Backups, file storage, and cache keys must be tenant-scoped.

## 9. Legal and trademark boundary

Verified licenses: Frappe Framework is **MIT**, ERPNext is **GPLv3**, ERPNext documentation is
**CC-BY-SA-3.0**, and Frappe publishes a **Logo and Trademark Policy**. See `security.md` §12.

- Removing a visible logo is a technical change; it is not a license to remove copyright notices or
  relicense the software.
- Distributing modified ERPNext can trigger GPL source-availability obligations. Internal use and
  distribution are different scenarios.
- Do not imply upstream endorsement.
- Do not give legal advice. Identify the question, cite the license, and recommend review by
  qualified counsel.
- Record the client's written approval for the branding scope, including any retention of upstream
  attribution.

## 10. Anti-patterns

- Editing `apps/frappe` or `apps/erpnext` templates/assets directly.
- Replacing a framework asset file instead of adding an override.
- Hardcoding a logo URL or brand name in JS or a print format.
- Branding only the desk and calling it done.
- Changing stored status values to change labels.
- Applying settings manually on production with no patch/fixture/runbook entry.
- Claiming the brand survives an upgrade without re-running verification.
- Promising "fully white-labeled" before email, PDF, portal, and login have been checked.
