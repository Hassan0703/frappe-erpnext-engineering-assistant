# White-label Verification

**Purpose:** prove the client's branding renders correctly on every surface, in the real environment,
and survives cache clears, builds, and migrations.

**How to use:** run after implementing branding and again after every upgrade. Record evidence, not
opinions. Attach screenshots/PDFs/HTML to the delivery record.

---

## 1. Context

| Item | Value |
|---|---|
| Environment / URL | |
| Frappe version | |
| ERPNext version | |
| Apps and branches | |
| Browser(s) / viewport | |
| Logged-in roles tested | |
| Verified by / date | |

## 2. Functional verification

Test in a private window. Use a non-Administrator user for at least one pass.

| # | Surface | Expected | Actual | Evidence | Pass/Fail |
|---|---|---|---|---|---|
| 1 | Login page | Client logo, title, no upstream brand | | | |
| 2 | Desk navbar | Client logo/app title | | | |
| 3 | Apps / desktop screen | Correct tile, icon, title, route | | | |
| 4 | Workspaces / sidebar | Client terminology | | | |
| 5 | Website home | Brand, nav, footer, copyright | | | |
| 6 | Portal | Brand and nav for customer/supplier | | | |
| 7 | Email | Sender identity, header, footer, legal text | | | |
| 8 | Notification | Correct copy and links | | | |
| 9 | Print/PDF | Letterhead, logo, totals, footer | | | |
| 10 | Error/404 page | Branded, no stack trace | | | |
| 11 | Favicon / browser title | Client identity | | | |
| 12 | Mobile/narrow viewport | No clipped logo or broken nav | | | |
| 13 | Target language | New terminology shown | | | |

## 3. Asset checks

```bash
# Expected: HTTP 200 for every brand asset
curl -sI https://<host>/assets/<app>/images/logo.png | head -1
curl -sI https://<host>/assets/<app>/images/favicon.ico | head -1

# Expected: no upstream brand strings in rendered HTML
curl -s https://<host>/login | grep -i "<upstream-brand>" && echo "FOUND - investigate"
```

| Asset URL | Status | Notes |
|---|---|---|
| | | |

Browser console: [ ] no 404s [ ] no errors

## 4. Persistence checks

| Check | Command | Result | Pass/Fail |
|---|---|---|---|
| Cache clear | `bench --site <site> clear-cache` then reload | | |
| Website cache clear | `bench --site <site> clear-website-cache` | | |
| Asset build | `bench build --app <app>` | | |
| Migration | `bench --site <site> migrate` | | |
| Process restart | restart web/workers; reload | | |
| Fresh install (if applicable) | new site + install app | | |

## 5. Environment parity

| Surface | Staging | Production | Difference intentional? |
|---|---|---|---|
| Desk | | | |
| Login | | | |
| Portal | | | |
| Email sender | | | |
| PDF/letterhead | | | |

Record any intentional difference (e.g. staging uses a test sender) and who approved it.

## 6. Defects found

| # | Defect | Severity | Owner | Status | Evidence |
|---|---|---|---|---|---|
| 1 | | | | | |

## 7. Sign-off

| Item | Value |
|---|---|
| Verified by | |
| Client approver | |
| Date | |
| Outstanding items | |
| Upgrade checklist updated? | yes/no |
