# Regression Checklist

**Purpose:** the recurring set of checks that catch breakage introduced by a change, an upgrade, or a
configuration edit.

**How to use:** run before releases and after upgrades. Extend it every time a defect escapes — add the
check that would have caught it.

---

## Context

| Item | Value |
|---|---|
| Release / change | |
| Environment | |
| Frappe / ERPNext versions | |
| Executed by / date | |

## 1. Core flows

```text
[ ] Login as administrator and as a normal user
[ ] Create, save, submit, and cancel one document per critical DocType
[ ] Amend a submitted document
[ ] Attach a file and open it again
[ ] Create a child-table row and verify totals
[ ] Duplicate detection / naming series still correct
[ ] Print a document to PDF
[ ] Send/queue one email
```

## 2. Permissions

```text
[ ] Restricted user cannot see other company/territory records (list + direct access)
[ ] Restricted user cannot write/submit/cancel outside their role
[ ] Sensitive field hidden at the correct permlevel
[ ] Whitelisted method denies an unauthorized user
[ ] Guest endpoint behaves as intended (or is absent)
```

## 3. Data and reports

```text
[ ] Key reports return the same figures as before (compare saved output)
[ ] Date-boundary filters still correct
[ ] Dashboard counts load
[ ] Exports produce expected columns/rows
```

## 4. Background work

```text
[ ] Scheduler enabled and a scheduled job ran recently
[ ] Queue depth normal; no stuck jobs
[ ] Long job completes and logs errors correctly
[ ] Notification/email queue draining
```

## 5. Integrations

```text
[ ] Outbound call succeeds
[ ] Downstream failure is handled and logged (test with a fake/disabled endpoint)
[ ] Duplicate webhook delivery does not double-apply
[ ] Credentials still valid
```

## 6. Version-specific

```text
[ ] v16: app routes/links use /desk; /apps not referenced
[ ] v16: print formats converted; PDF renders via Chromium
[ ] v16: translations compile (PO/MO) and render in each language
[ ] v16: no reliance on removed modules or deprecated APIs
[ ] v15: no v16-only hook/class imports introduced
[ ] Query field expressions valid for the version (v16 strict parsing)
[ ] Explicit ordering where reports/jobs depend on order
```

## 7. Branding (if applicable)

```text
[ ] Desk, login, portal, favicon correct
[ ] Email sender/footer correct
[ ] Print/PDF letterhead correct
[ ] Survives clear-cache, bench build, migrate
```

## 8. Deployment and recovery

```text
[ ] Smoke test passed after deploy
[ ] Backup ran and is off-site
[ ] Restore drill current
[ ] Monitoring/alerts firing correctly (test one)
```

## 9. Result

| Section | Result | Issues raised |
|---|---|---|
| Core flows | | |
| Permissions | | |
| Data/reports | | |
| Background work | | |
| Integrations | | |
| Version-specific | | |
| Branding | | |
| Deployment/recovery | | |

Checks added to this list after this run:

| # | New check | Triggering defect |
|---|---|---|
| 1 | | |
