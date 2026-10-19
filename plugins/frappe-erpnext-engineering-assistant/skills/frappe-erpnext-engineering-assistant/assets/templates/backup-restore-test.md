# Backup and Restore Test

**Purpose:** prove a backup can actually be restored. A scheduled backup job is not evidence.

**How to use:** execute this drill on a scratch site or isolated host — never over production. Record
observed results, durations, and failures. Re-run at the agreed interval and after any change to
backup configuration.

---

## 1. Drill context

| Item | Value |
|---|---|
| Date / time (timezone) | |
| Performed by | |
| Environment used for restore | scratch site / isolated host (name) |
| Source environment of backup | production / staging |
| Backup timestamp used | |
| Backup location | |
| Frappe / ERPNext versions (source → restore) | |
| Reason (scheduled drill / pre-upgrade / incident) | |

## 2. Backup inventory

| Artifact | Present? | Size | Checksum/verified | Notes |
|---|---|---|---|---|
| Database dump | | | | |
| Public files | | | | |
| Private files | | | | |
| Site config (incl. `encryption_key`) | | | | |
| Custom code revision recorded | | | | |

> Without the matching `encryption_key`, encrypted field values are unrecoverable. Confirm it is
> stored separately and accessibly.

## 3. Restore procedure executed

```text
[ ] Provisioned an empty site/host at the same versions
[ ] Restored database
[ ] Restored public files
[ ] Restored private files
[ ] Applied configuration (site_config / common_site_config)
[ ] Confirmed site starts
[ ] Confirmed scheduler state is intentional (restored sites often have it disabled)
```

Commands used (record exactly):

```text

```

## 4. Verification

| # | Check | Method | Result | Pass/Fail |
|---|---|---|---|---|
| 1 | Row count: key transactional DocType | `SELECT COUNT(*)` vs source snapshot | | |
| 2 | Row count: key master DocType | | | |
| 3 | Latest transaction present | Search by name | | |
| 4 | Attachment opens (private file) | Open the file | | |
| 5 | Attachment sample checksum matches | Compare hashes | | |
| 6 | Login works for a normal user | Log in | | |
| 7 | Permissions correct | Restricted user sees only allowed rows | | |
| 8 | A report runs with correct totals | Run and compare | | |
| 9 | PDF generates | Render one | | |
| 10 | Email sends (staging only) | Send test | | |
| 11 | Encrypted values readable | Open a doc with an encrypted field | | |
| 12 | Branding/letterhead present | Visual check | | |

## 5. Measured outcomes

| Metric | Value |
|---|---|
| Total restore duration | |
| Time to a usable site | |
| Backup size (DB / files) | |
| Compared against RTO/RPO | pass / fail |
| Data loss window in a real restore | |

## 6. Problems found

| # | Problem | Impact | Fix required | Owner | Status |
|---|---|---|---|---|---|
| 1 | | | | | |

## 7. Sign-off

| Item | Value |
|---|---|
| Restore verified by | |
| Reviewed by | |
| Scratch environment destroyed | yes/no |
| Next drill due | |
| Backup procedure/config changes required | |
