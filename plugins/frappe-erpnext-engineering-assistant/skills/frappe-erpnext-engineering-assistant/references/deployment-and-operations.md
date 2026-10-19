# Deployment and Operations

Production reliability is a design property, not an afterthought. This reference covers what a
Frappe/ERPNext deployment needs, how to release and roll back, and what evidence makes a backup or
DR claim real.

**Commands vary by bench version and deployment.** Run `bench <command> --help` on the target bench
before relying on a flag. Anything below marked *(verify)* must be confirmed there.

## 1. Hosting patterns

| Pattern | Shape | Good for | Watch |
|---|---|---|---|
| **Bench on a VM/bare metal** | nginx → gunicorn → MariaDB/Postgres + Redis + workers + scheduler | Full control, custom apps, single-tenant | You own patching, backups, monitoring, TLS |
| **Containerized bench** | Separate web/worker/scheduler/redis/db containers | Reproducibility, horizontal scaling | Persistent volumes for sites/files/backups; Chromium in every printing container; shared queue/cache correctness |
| **Managed Frappe hosting** | Provider runs bench/sites | Small teams, less ops | App-install constraints, data residency, export/exit plan, cost |

Choose based on who will operate it, not on what is fashionable. The client must know who is
responsible for backups, restores, TLS, upgrades, and monitoring — put it in the runbook.

## 2. Environment requirements

- **OS and runtime:** match the supported versions for the target Frappe major. v16 requires
  **Python 3.14+ and Node 24+**; v15 has its own floor. Pin these in the image/runbook. (Verified:
  v16 migration guide.)
- **Database:** MariaDB or PostgreSQL as supported by the target version. Set character set,
  timezone, and connection limits deliberately. Back up the database *and* the site files.
- **Redis:** separate logical uses for cache, queue, and socketio where the deployment supports it.
  Memory pressure here causes slow desks and lost jobs.
- **PDF engine:** v15 uses wkhtmltopdf; v16 uses Chromium for editor formats (`bench setup-chrome`,
  or `chromium_path` in `common_site_config.json` on offline servers). Install fonts the client's
  documents use. (Verified: PDF generation docs.)
- **Timezone/locale:** set the OS, database, site, and user timezones consistently. Mismatched
  timezones silently shift posting dates and scheduler runs.
- **Disk:** assets, uploads, backups, and logs all grow. Monitor free space and set retention.

## 3. Configuration

Frappe reads configuration from `common_site_config.json` (bench-wide) and `site_config.json`
(per site). `.env`-style files are not the native mechanism; use the config files or environment
variables read explicitly by your app.

```bash
bench --site <site> show-config          # effective config, redact before sharing
bench --site <site> set-config <key> <value>
```

Rules:

- `developer_mode` must be off in production. It changes behavior and exposes development tools.
- Do not commit `site_config.json`, `common_site_config.json`, database credentials, or encryption
  keys to Git.
- The `encryption_key` in `site_config.json` protects encrypted field values. Back it up separately
  and securely; losing it makes those values unrecoverable. Never rotate it casually.
- Keep environment-specific values (hostnames, provider keys, mail domains) out of code.
- v16 caches site/common config for up to about a minute. Do not assume a config change applies
  instantly to running workers. (Verified: v16 migration guide.)

## 4. Services and health

A production bench normally runs:

| Service | Role | Health signal |
|---|---|---|
| nginx/reverse proxy | TLS, static assets, routing | 200 on `/api/method/ping`; valid cert |
| gunicorn/web | application requests | 5xx rate, latency, restarts |
| worker (short/long) | background jobs | queue depth, failed jobs, worker logs |
| scheduler | scheduled events | scheduler enabled per site; recent runs |
| Redis | cache/queue/socketio | memory, evictions, connectivity |
| database | persistence | connections, slow queries, replication if used |
| socketio | realtime | connection errors, memory |

Useful checks (confirm availability on your bench):

```bash
bench doctor
bench --site <site> show-pending-jobs
bench --site <site> ready-for-migration
bench --site <site> enable-scheduler      # or disable-scheduler
bench --site <site> purge-jobs            # destructive to queued jobs; understand before running
```

A site restored from backup often has the scheduler **disabled**. Re-enable it deliberately and
verify that scheduled jobs run.

## 5. Domains, proxy, and TLS

- One hostname per site (or a documented wildcard/multi-site setup). Keep staging and production on
  separate hostnames and separate credentials.
- Terminate TLS at the proxy; redirect HTTP to HTTPS; use HSTS only when every subdomain is ready.
- Automate certificate renewal and alert before expiry. A silent expiry is an outage.
- Set `client_max_body_size` (or equivalent) above the largest allowed upload; document the value.
- Preserve real client IPs (`X-Forwarded-For`) for logs, rate limiting, and audit.
- Test after proxy changes: login, file upload, websocket/realtime, PDF generation.

## 6. Secrets

- Store credentials in the platform's secret manager or root-owned config outside the repo, with
  least privilege and per-environment separation.
- Never paste production secrets into prompts, tickets, chat, screenshots, or logs.
- Rotate after exposure. Removing a secret from the latest commit does not remove it from history.
- Grant backup access only to operators who need it, and log access.
- The app's own secrets (payment keys, API tokens) belong in site config or the environment, read at
  runtime — not in JS bundles.

## 7. Email, storage, and integrations

- Configure an authenticated outgoing Email Account and sender domain (SPF/DKIM/DMARC owned by the
  client). Test delivery to an external mailbox, not just internal.
- Monitor the email queue; a stuck queue looks like "the system doesn't send email".
- For object storage/CDN, the `write_file`/`before_write_file` hooks can redirect file I/O. Verify
  privacy semantics: private files must not become public through the CDN.
- For every integration, define timeout, retry policy, idempotency key, failure notification, and an
  owner. See `ai-features.md` for LLM-specific controls.
- Webhooks must verify signatures and tolerate duplicates.

## 8. Sizing and capacity

Do not size from a blog formula. Measure:

- Requests per second and p95 latency at peak.
- Background queue depth and job duration.
- Database size, slow-query log, connection count.
- Redis memory and evictions.
- Disk growth for uploads/backups/logs.
- PDF/print volume (v16 Chromium is heavier than wkhtmltopdf for some formats).

Start with a known-good reference architecture for the expected user count, then load-test the
actual critical flows (login, list view, a heavy report, document submit, PDF). Record results.

## 9. Staging and production parity

Staging must be close enough to catch upgrade and migration failures:

- Same Frappe/ERPNext majors and add-on apps.
- Same database engine and character set/timezone.
- Same custom apps and patch level.
- Representative (anonymized) data volume, including attachments.
- Same PDF engine and fonts.
- Separate credentials, domains, mail settings, and storage.

Never copy production customer data to staging without anonymization and authorization.

## 10. Release procedure

```text
[ ] Change reviewed and CI green
[ ] Release notes / changelog written
[ ] Version/tag recorded
[ ] Backup taken: database + files + config; verify size and completion
[ ] Restore drill current (for major releases)
[ ] Staging deployment of the same artifact succeeded
[ ] Maintenance mode on (if users would see partial state)
[ ] Deploy code at the recorded revision
[ ] Install/update dependencies for the target version
[ ] bench --site <site> migrate
[ ] bench build
[ ] Restart web, worker, scheduler, socketio
[ ] Smoke test: login, list view, one transaction, one report, one PDF, email
[ ] Branding spot-check (see white-labeling.md)
[ ] Maintenance mode off
[ ] Monitor errors, latency, queue for the agreed window
```

Keep releases small. A release that changes schema, code, and assets at once is hard to roll back.

### Risk classification (decide before you schedule it)

Classify every production change; the class sets the required evidence, approver, and rollback
posture. When in doubt, classify higher. Record the class in the release/rollback template.

| Class | Examples | Required before deploy | Approval | Rollback expectation |
|---|---|---|---|---|
| **1 — No runtime effect** | documentation, comments, template text not loaded at runtime | review | normal reviewer | none |
| **2 — Code/config, no schema or data** | controller/JS/CSS change, hook change, translation text, asset update | backup taken (even if not strictly needed); staging smoke | tech lead | redeploy previous revision, rebuild, restart |
| **3 — Schema or data change** | DocType/field change, fixture, patch, `migrate`, report/print format conversion | verified backup **and** current restore drill; staging migration rehearsal | tech lead + client owner | restore pre-release DB and files, or forward-fix; state the data-loss window |
| **4 — Destructive / irreversible / financial** | bulk data repair, ledger or stock correction, production restore, site reinstall, forced migration, permission widening | written plan, verified backup, dry run on a copy, maintenance window, named decision-maker | client owner + tech lead, in writing | often forward-fix only; get explicit approval and record it |

Rules:

- A class 3 or 4 change never ships without a backup you can restore and a stated rollback path.
- Permissions and authentication changes are class 4: they can expose data even when no schema changes.
- If the classification is disputed, treat it as the higher class until evidence settles it.

## 11. Rollback

**Patches and migrations are generally forward-only.** There is often no "undo migrate". Plan
rollback as one of:

1. **Code-only rollback** (no schema/data change): redeploy the previous revision, rebuild, restart.
2. **Full rollback** (schema/data changed): restore the pre-release database and files, then deploy
   the previous code revision. This loses data written after the backup — state that explicitly and
   get approval.
3. **Forward fix** (preferred when data must be preserved): write a corrective patch and deploy it.

Rollback is a decision, not a reflex. Record the chosen path, the data-loss window, and the approver
in `assets/templates/release-and-rollback.md`.

## 12. Backups

A backup exists only if it can be restored. Define:

| Question | Required answer |
|---|---|
| What is backed up? | Database, public files, private files, config (including `encryption_key`), custom code revision |
| How often? | Schedule tied to RPO; before every release and migration |
| Where? | Encrypted off-site storage, separate from the host/provider account |
| Retention? | Per data class and contract; bench prunes old backups by default — confirm the configured retention |
| Who can access? | Named operators, least privilege, access logged |
| How is integrity checked? | Size, checksum, and a periodic restore test |
| How is it encrypted? | At rest and in transit; key stored separately from the backup |

```bash
bench --site <site> backup --with-files          # confirm flags with --help
ls -lh sites/<site>/private/backups/
```

Do not leave the only copy on the same disk, host, or cloud account as production. Do not assume the
provider backs up for you unless it is in the contract.

## 13. Restore drill

Run on a **scratch site or isolated host**, never over production.

```text
[ ] Select a real backup from the agreed retention window
[ ] Provision an empty site/host with the same versions
[ ] Restore database + public files + private files
[ ] Confirm the site starts and the scheduler state is intentional
[ ] Verify row counts for key DocTypes against the source snapshot
[ ] Verify a sample of attachments (open a private file, check checksum)
[ ] Verify login for a normal user and an administrator
[ ] Verify permissions with a non-privileged user
[ ] Render a report and a PDF
[ ] Send a test email from staging only
[ ] Record duration (RTO evidence) and any gaps
[ ] Destroy the scratch environment securely
```

Record the result in `assets/templates/backup-restore-test.md`. A scheduled backup job with no
restore evidence is **not** a verified backup.

## 14. Disaster recovery and incidents

- Define **RPO** (acceptable data loss) and **RTO** (acceptable downtime) with the client, in writing.
- Identify failure scenarios: host loss, database corruption, accidental deletion, ransomware,
  provider outage, certificate expiry.
- Keep an out-of-band contact list and access path (not dependent on the failed system).
- For a production incident: stabilize first (stop the bleeding, preserve evidence), communicate,
  then fix. Use `assets/templates/incident-report.md`.
- After recovery, verify data integrity and re-enable the scheduler; a common post-restore failure is
  "everything works but no jobs run".

## 15. Upgrade planning (v15 → v16)

1. Confirm every installed app has a v16-compatible branch; do not mix majors.
2. Provision the new runtime: Python 3.14+, Node 24+, Chromium for PDFs.
3. Rehearse on a production-like staging clone with a real backup.
4. Back up workspaces; standard workspace edits are overwritten on v16 migrate.
5. Convert classic print formats; rewrite CSS selectors; re-test PDFs.
6. Convert translations to PO/MO; rebuild.
7. Check for removed modules and imports (Blog, Newsletter, Energy Points, Backup Integrations).
8. Audit `get_all`/`get_list` field expressions, implicit ordering, `has_permission` returns,
   `override_doctype_class` inheritance, and `db.get_value` comparisons on Singles.
9. Migrate staging, run smoke + branding verification, then repeat in production in a window.
10. Keep the pre-upgrade backup until the client signs off.

Details and sources: `version-compatibility.md`.

## 16. Monitoring and alerting

Alert on symptoms users feel, not only on process liveness:

- HTTP 5xx rate and p95 latency.
- Scheduler disabled or no recent scheduled runs.
- Background queue depth/age; failed job count.
- Error Log growth (new error types, not just volume).
- Database connections/slow queries/disk.
- Redis memory/evictions.
- Disk space and backup age.
- TLS certificate expiry.
- Email queue backlog and bounce rate.
- PDF generation failures (Chromium missing/timeouts).
- Login failures and permission-denied spikes.

Every alert needs an owner, a threshold, and a documented first response.

## 17. Common failure modes

| Symptom | Likely cause | Check |
|---|---|---|
| Desk blank / assets 404 | `bench build` not run or cache stale | Build, clear cache, hard refresh |
| Code change not active | Workers/web not restarted | Restart processes; confirm revision |
| Scheduled jobs stopped | Scheduler disabled (often after restore) | `bench doctor`, enable scheduler |
| Slow site, growing queue | Workers down or undersized | Pending jobs, worker logs |
| PDF hangs/fails | Chromium missing or no internet | `bench setup-chrome`, `chromium_path`, logs |
| Emails not sent | Queue stuck, bad credentials, DNS | Email queue, provider logs, DNS |
| Config change ignored | v16 config cache (~1 min) or wrong site | `show-config`, wait, restart |
| Disk full | Backups/logs/uploads | Retention, off-host storage |
| Restore "worked" but data missing | Files not restored / wrong backup | Counts, attachments, private files |
| Wrong tenant data | Missing site context or row scoping | Site routing, permissions, job context |

## 18. Operations checklist

- [ ] Versions detected and recorded; apps compatible with the Frappe major.
- [ ] Runtime, database, Redis, PDF engine, and fonts provisioned and pinned.
- [ ] `developer_mode` off; config and secrets outside the repo.
- [ ] TLS automated; renewal alert configured; upload size set.
- [ ] Scheduler enabled; workers and queue monitored.
- [ ] Backups include DB, public/private files, config/encryption key; stored encrypted off-site.
- [ ] Restore drill executed and recorded within the agreed window.
- [ ] Release and rollback procedures written, with data-loss window stated.
- [ ] Monitoring covers 5xx, queue, scheduler, disk, cert, backup age, PDF, email.
- [ ] Staging matches production majors/apps/PDF engine; data anonymized.
- [ ] Post-upgrade verification includes branding, permissions, reports, PDF, email.
- [ ] DR contacts and out-of-band access documented.
