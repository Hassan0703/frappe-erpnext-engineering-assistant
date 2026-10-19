# Cutover Checklist

**Purpose:** sequence the final move to the new system so nothing is forgotten under time pressure.

**How to use:** print or duplicate per cutover. Each item has an owner and a time. The go/no-go
decision is explicit and recorded.

---

## Cutover context

| Item | Value |
|---|---|
| Migration / project | |
| Cutover date / window (timezone) | |
| Source freeze start | |
| Target go-live | |
| Cutover lead | |
| Decision maker (go/no-go) | |
| Rollback trigger + owner | |

## T-1 (day before)

```text
[ ] Final migration rehearsal passed on production-like data
[ ] Reconciliation report reviewed; differences approved or zero
[ ] Target backup taken and restore verified
[ ] Rollback procedure rehearsed and documented (data-loss window stated)
[ ] Users notified of downtime and changes
[ ] Freeze instructions issued to source-system users
[ ] Access ready for all operators (no single point of failure)
[ ] Monitoring attached to the target
[ ] Hypercare plan and owner confirmed
```

## T-0 (cutover)

```text
[ ] Source writes frozen at <time>
[ ] Final extract taken (timestamp + checksum recorded)
[ ] Final delta load executed (run log updated)
[ ] Idempotency re-run confirms no duplicates
[ ] Reconciliation re-run on final data
[ ] Opening balances and stock signed off by business owner
[ ] Users, roles, and permissions created and verified
[ ] Permissions tested with restricted users
[ ] Integrations repointed and tested end-to-end
[ ] Notifications/email re-enabled (were disabled during load)
[ ] Scheduler enabled; one scheduled job verified
[ ] Reports and dashboards checked with real data
[ ] Print formats/PDF verified
[ ] Branding verified (if applicable)
[ ] Target backup taken post-load, pre-go-live
[ ] Go/no-go decision recorded
[ ] Go-live announced
```

## T+0 to T+1 (hypercare)

```text
[ ] Smoke test executed by the business
[ ] Error Log and failed jobs reviewed
[ ] Duplicate-creation check (masters created twice by users/integrations)
[ ] First transactions entered and validated
[ ] Bank/GL reconciliation started
[ ] Source system kept read-only for the agreed period
[ ] Issues logged with severity and owner
[ ] Daily check-in scheduled
```

## T+7 / T+30

```text
[ ] First period close completed and reconciled
[ ] Post-go-live reconciliation compared to cutover figures
[ ] Source system decommission/archive decision recorded
[ ] Documentation updated with actual outcomes
[ ] Migration artifacts archived (mapping, run logs, reconciliation, approvals)
[ ] Lessons learned recorded
```

## Rollback decision

| Item | Value |
|---|---|
| Trigger conditions | |
| Who decides | |
| Method (restore pre-cutover target / re-enable source) | |
| Data-loss window | |
| Time required | |
| Communication plan | |

## Sign-off

| Role | Name | Date | Notes |
|---|---|---|---|
| Cutover lead | | | |
| Business owner | | | |
| Finance (if money/stock) | | | |
| Operations | | | |
