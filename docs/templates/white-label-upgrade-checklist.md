# White-label Upgrade Checklist

**Purpose:** stop branding regressions after a Frappe/ERPNext upgrade, patch, or environment rebuild.

**How to use:** attach to the client project and run before and after every upgrade. Record results;
do not assume branding survived because it "should".

---

## 1. Upgrade context

| Item | Value |
|---|---|
| From version → to version | |
| Frappe / ERPNext | |
| Apps upgraded | |
| Staging rehearsal date | |
| Production window | |
| Owner | |

## 2. Before the upgrade

- [ ] Asset files, brand colours, and fonts archived outside the app (logo files are not lost in a revert).
- [ ] Current branding screenshots captured (desk, login, portal, email, PDF) as the baseline.
- [ ] Custom workspace/sidebar changes exported or copied — v16 overwrites modified standard workspaces on migrate.
- [ ] Configuration inventory current (settings, letterheads, print formats, email templates).
- [ ] Translations source of truth identified and exported (CSV for v15, PO for v16).
- [ ] Print formats reviewed: classic formats must be converted before they stop working (v17 per upstream).
- [ ] Backup taken and restore verified for the branding-relevant data.
- [ ] Rollback plan and data-loss window stated.

## 3. After the upgrade

Run `white-label-verification.md` in full, and additionally confirm:

- [ ] `bench build` completed successfully for the branding app.
- [ ] Caches cleared (`clear-cache`, `clear-website-cache`).
- [ ] Chromium available for PDFs if the system prints (`bench setup-chrome` or `chromium_path`).
- [ ] Desk route/bookmarks updated if the version changed routes (`/app` → `/desk` in v16).
- [ ] App tile still registers on the apps/desktop screen (`add_to_apps_screen`).
- [ ] Favicon and browser title correct on desk, website, and login.
- [ ] Email sender identity, footer, and legal text unchanged.
- [ ] Letterhead assigned to every company that prints.
- [ ] Print/PDF CSS still correct after any print-format conversion.
- [ ] Translations render in all supported languages (format may have changed between versions).
- [ ] Terminology overrides still applied after the framework's own translation updates.
- [ ] Rich-text brand copy renders correctly (sanitizer behavior changed between versions).
- [ ] No upstream brand visible on any in-scope surface.
- [ ] Out-of-scope surfaces unchanged or re-accepted by the client.

## 4. Known version-specific regression risks

| Risk | Version | Mitigation |
|---|---|---|
| Standard workspace edits overwritten on migrate | v16 | Re-apply as app-shipped/private workspaces |
| Classic print formats deprecated; PDF engine changed to Chromium | v16 | Convert formats, provision Chromium, re-test PDFs |
| Translation files moved from CSV to PO/MO | v16 | Convert and compile; verify languages |
| `/app` → `/desk`; `/apps` deprecated | v16 | Update docs, links, redirects, training |
| App tile/navigation changes (sidebar/desktop) | v16 | Verify `add_to_apps_screen` and sidebars |
| HTML sanitization changed (bleach → nh3) | v16 | Re-check rich-text brand copy |
| Site/common config cached ~1 minute | v16 | Re-check after waiting/restarting, not immediately |
| Python/Node floor raised | v16 | Re-provision images before upgrading |

## 5. Result

| Item | Value |
|---|---|
| Regressions found | |
| Fixes applied (ticket IDs) | |
| Re-verification date | |
| Sign-off (client) | |
| Outstanding items / owner | |
