# Deployment Runbook

**Purpose:** the single operational document for installing, deploying, and recovering a
Frappe/ERPNext site. It must be executable by someone who did not build the system.

**How to use:** copy into the client's repository or ops wiki. Replace every `<placeholder>`, delete
nothing without recording why, and verify each command on the target bench (`--help`) before relying
on it. Record who owns each section.

---

## 1. System summary

| Item | Value |
|---|---|
| Client / product | |
| Environments | dev / staging / production (hostnames) |
| Frappe version | |
| ERPNext version | |
| Add-on apps (branch) | |
| Hosting model | VM / containers / managed |
| Database engine / version | |
| Redis | |
| PDF engine | wkhtmltopdf (v15) / Chromium (v16) |
| Object storage / CDN | |
| Repo / branch for deployment | |
| Owner(s) | |

## 2. Access and secrets

| Item | Where stored | Who has access | Rotation |
|---|---|---|---|
| SSH / host access | | | |
| Database credentials | | | |
| `site_config.json` / `common_site_config.json` | | | |
| `encryption_key` | | | |
| Provider API keys | | | |
| TLS certificates | | | |
| Backup storage credentials | | | |

> Never store production secrets in this document. Reference the secret store.

## 3. Provisioning (new environment)

```text
[ ] OS, Python, Node, database, Redis installed at supported versions (v16: Python 3.14+, Node 24+)
[ ] Bench created / containers configured
[ ] Apps fetched at pinned branches
[ ] Site created
[ ] Apps installed on the site
[ ] site_config / common_site_config applied (developer_mode off)
[ ] Scheduler enabled
[ ] Reverse proxy + TLS configured
[ ] Upload size configured at the proxy
[ ] PDF engine provisioned (bench setup-chrome for v16) and tested
[ ] Email account + sender domain configured and tested
[ ] Object storage/CDN configured (if used)
[ ] Monitoring and alerting attached
[ ] Backups scheduled + off-site storage confirmed
[ ] Smoke test passed
```

## 4. Routine deployment

```text
[ ] Change reviewed/approved; CI green; version/tag recorded
[ ] Backup: database + files + config; verify size and completion
[ ] Maintenance mode on (if users would see a partial state)
[ ] Deploy code at the recorded revision
[ ] Install/update dependencies
[ ] bench --site <site> migrate
[ ] bench build
[ ] Restart web, worker, scheduler, socketio
[ ] Smoke test (section 5)
[ ] Branding spot check (if identity changed)
[ ] Maintenance mode off
[ ] Monitor errors/latency/queue for <window>
```

Record each run in `release-and-rollback.md`.

## 5. Smoke test (post-deploy)

```text
[ ] /api/method/ping responds
[ ] Login as a normal user (not only Administrator)
[ ] Open a list view; open a document; save
[ ] Submit or cancel the critical business transaction
[ ] Run the most important report
[ ] Generate a PDF
[ ] Send a test email to an external address
[ ] Trigger or wait for one scheduled job
[ ] Check Error Log for new errors
[ ] Verify branding surfaces changed by the release
```

## 6. Service management

| Task | Command (verify with --help) |
|---|---|
| Start/stop services | |
| Restart web/workers | |
| Enable/disable scheduler | `bench --site <site> enable-scheduler` / `disable-scheduler` |
| Check scheduler + workers | `bench doctor` |
| Check pending jobs | `bench --site <site> show-pending-jobs` |
| Maintenance mode | `bench --site <site> set-maintenance-mode on\|off` |
| Show effective config | `bench --site <site> show-config` |

## 7. Backup and restore

| Item | Value |
|---|---|
| Schedule | |
| Scope | database + public files + private files + config |
| Location | off-host, encrypted |
| Retention | |
| Restore procedure reference | `backup-restore-test.md` |
| Last successful restore drill | |

```bash
bench --site <site> backup --with-files          # confirm flags
bench --site <site> restore <path>               # restore procedure; never over production without approval
```

## 8. Monitoring

| Signal | Tool | Threshold | Owner | First response |
|---|---|---|---|---|
| HTTP 5xx | | | | |
| Latency p95 | | | | |
| Scheduler last run | | | | |
| Queue depth/age | | | | |
| Disk usage | | | | |
| DB connections/slow queries | | | | |
| Redis memory | | | | |
| TLS expiry | | | | |
| Backup age | | | | |
| PDF failures | | | | |
| Email queue | | | | |

## 9. Rollback

| Item | Value |
|---|---|
| Code-only rollback steps | |
| Full rollback steps (restore DB + files) | |
| Data-loss window if restored | |
| Decision maker | |
| Reference | `release-and-rollback.md` |

## 10. Contacts and escalation

| Role | Name | Contact | Hours |
|---|---|---|---|
| Service owner | | | |
| DBA | | | |
| Client product owner | | | |
| Security escalation | | | |

## 11. Change log of this runbook

| Date | Change | Author |
|---|---|---|
| | | |
