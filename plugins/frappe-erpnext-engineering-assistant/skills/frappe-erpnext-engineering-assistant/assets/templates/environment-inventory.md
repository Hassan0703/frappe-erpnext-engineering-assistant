# Environment Inventory

**Purpose:** one authoritative record of every environment, version, and configuration difference.
Prevents "works in staging, fails in production" surprises and speeds up incident response.

**How to use:** update on every environment or version change. Keep it factual; verify values by
running the commands rather than copying from memory.

---

## 1. Environments

| | Dev | Staging | Production |
|---|---|---|---|
| Purpose | | | |
| Hostname / URL | | | |
| Hosting model | | | |
| Region | | | |
| Owner | | | |
| Data sensitivity | | | |
| Refresh policy (from prod?) | | | |
| Anonymization required | | | |

## 2. Versions (fill from `bench version`)

| Component | Dev | Staging | Production |
|---|---|---|---|
| Frappe | | | |
| ERPNext | | | |
| Add-on apps (+branches) | | | |
| Python | | | |
| Node | | | |
| Database engine/version | | | |
| Redis | | | |
| PDF engine (wkhtmltopdf/Chromium) | | | |

> Record the exact command output date. `bench version` output format differs between v15 and v16.

## 3. Configuration differences

| Setting | Dev | Staging | Production | Intentional? |
|---|---|---|---|---|
| `developer_mode` | | | | |
| Scheduler enabled | | | | |
| Email sender | | | | |
| File storage (local/S3) | | | | |
| Backup destination/retention | | | | |
| Log level / retention | | | | |
| Maintenance mode | | | | |

## 4. Integrations per environment

| Integration | Dev | Staging | Production | Credentials owner |
|---|---|---|---|---|
| Email provider | | | | |
| Payment gateway | | | | |
| SMS | | | | |
| Storage/CDN | | | | |
| AI/LLM provider | | | | |
| Other | | | | |

## 5. Access

| Access type | Dev | Staging | Production | Notes |
|---|---|---|---|---|
| SSH / container exec | | | | |
| Database console | | | | |
| Secret store | | | | |
| Backup storage | | | | |
| Monitoring | | | | |

## 6. Known differences and risks

| # | Difference | Risk | Mitigation | Owner |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |

## 7. Verification record

| Date | Verified by | Method | Findings |
|---|---|---|---|
| | | | |
