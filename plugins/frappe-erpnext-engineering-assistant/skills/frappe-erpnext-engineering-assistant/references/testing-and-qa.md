# Testing, QA, and Delivery Evidence

Tests are how a change becomes a fact. "It works on my site" is an observation, not evidence.

## 1. Test layers

Use the lightest layer that can prove the behavior, and add higher layers for risk.

| Layer | Proves | Typical tool |
|---|---|---|
| Unit | Pure transformation, validation helpers, calculations | `UnitTestCase` / plain pytest-style functions |
| Integration | Documents save, submit, cancel; hooks fire; DB state is correct | `IntegrationTestCase` |
| Permission | A non-privileged user cannot read/write/act | Integration + `frappe.set_user` |
| Workflow/business rule | State transitions, approvals, totals, blocking conditions | Integration |
| Regression | Previously broken behavior stays fixed | Integration, named after the defect |
| Migration | Load is idempotent and reconciles | Migration script + reconciliation report |
| API/integration failure | Timeouts, retries, bad payloads, duplicate webhooks | Unit/integration with fakes |
| Background job | Job logic and failure handling | Direct call or enqueue-now |
| UI/branding | Form behavior, visible identity | Manual checklist, Cypress where available |
| Deployment smoke | The release actually runs | Runbook smoke list |
| Backup/restore | A backup can be restored | Restore drill |
| Performance/security | The change meets its budget and controls | Load test, permission review |

Not every change needs every layer. Every change needs at least one executed check that would fail
if the change were wrong.

## 2. Version-specific conventions

**v16 (verified):** import from `frappe.tests`, and choose the class by whether the test touches the
database:

```python
from frappe.tests import IntegrationTestCase, UnitTestCase


class TestLoanApplication(IntegrationTestCase):
    def test_rejects_inverted_dates(self):
        doc = frappe.get_doc({...})
        with self.assertRaises(frappe.ValidationError):
            doc.insert()

    def test_non_privileged_user_cannot_read(self):
        frappe.set_user("limited@example.com")
        self.addCleanup(frappe.set_user, "Administrator")
        self.assertFalse(frappe.has_permission("Loan Application", "read"))
```

- `IntegrationTestCase` for anything that creates, queries, or saves documents.
- `UnitTestCase` only for in-memory logic that does not touch the database.
- If you override `setUpClass`, call `super().setUpClass()`.
- v16 renames test dependency attributes to `EXTRA_TEST_RECORD_DEPENDENCIES` and
  `IGNORE_TEST_RECORD_DEPENDENCIES`; `frappe.flags.in_test` is deprecated in favor of `frappe.in_test`.
- `frappe.tests.utils.FrappeTestCase` is deprecated in v16 (upstream states removal in v17). Do not
  introduce it in new code; migrate it when touching an existing test file.

**v15:** `FrappeTestCase` is the established base class. Keep existing v15 tests working; do not
backport v16-only imports into a v15 app.

Confirm the available classes on the installed version before rewriting a suite.

## 3. Where tests live

```
apps/<app>/<app>/<module>/doctype/<doctype_snake>/test_<doctype_snake>.py
apps/<app>/<app>/<module>/test_<feature>.py
```

- Name tests after behavior, not implementation: `test_blocks_submit_when_credit_limit_exceeded`.
- One reason to fail per test. Avoid asserting five unrelated things.
- Build the minimum fixture the test needs; do not depend on demo data or a developer's local site.
- Use the `before_tests` hook for seed data that must exist for the suite.
- Clean up users/roles/settings you change, or the next test inherits your state.

## 4. Running tests

```bash
bench --site <test_site> run-tests --app <app>
bench --site <test_site> run-tests --app <app> --module <app>.path.to.test_module
bench --site <test_site> run-tests --app <app> --doctype "<DocType>"
bench --site <test_site> run-parallel-tests --app <app>   # CI; confirm flags with --help
```

- Prefer a dedicated test site, never production.
- Run the narrowest useful scope first (one doctype/module), then the app suite for regressions.
- Preserve the exit status when piping output; read the failure, do not grep for "OK".
- A skipped test is not a passing test. Report skips explicitly.
- If the suite cannot run (no site, missing dependency, broken environment), say exactly what failed
  to run and what remains unverified.

## 5. What to test for common changes

| Change | Must test |
|---|---|
| New validation | Valid case saves; invalid case raises `frappe.ValidationError` with the expected message |
| Controller lifecycle | `on_submit`, `on_cancel`, and reversal side effects; no duplicate records on retry |
| Permission/role change | Allowed user succeeds; denied user gets `PermissionError`; list query hides rows |
| Custom field/fixture | Field exists after migrate; default and mandatory behavior correct |
| Patch | Runs on a pre-patch fixture; idempotent on re-run |
| Report | Filters, totals, permissions, empty result, date boundaries |
| Print format | Renders with a real document; totals and currency correct; PDF generated |
| Client script | Form loads, query filters apply, button calls the server method, error path shown |
| Integration | Success, timeout, non-2xx, malformed payload, duplicate delivery |
| Background job | Success path, failure logging, retry/idempotency |
| Branding | See `white-labeling.md` verification table |
| Migration | Idempotent re-run + reconciliation counts/totals |

## 6. Permission tests

Permissions are the most common silent regression.

```python
def test_company_scope_is_enforced(self):
    frappe.set_user("sales.user@example.com")
    self.addCleanup(frappe.set_user, "Administrator")

    visible = frappe.get_list("Sales Invoice", fields=["name"])
    self.assertTrue(all(row.company == "Company A" for row in visible))

    with self.assertRaises(frappe.PermissionError):
        frappe.get_doc("Sales Invoice", "SINV-COMPANY-B-0001").check_permission("read")
```

Test as a real role-limited user, not Administrator. Cover:

- List visibility (row-level scoping), not just direct document access.
- Field-level restrictions (`permlevel`).
- Write/submit/cancel/delete separately.
- Whitelisted methods reachable by an unauthorized user.
- Guest endpoints with no session.

## 7. Background jobs and scheduler

- Test the job function directly first; then test enqueue behavior.
- `frappe.enqueue(..., now=True)` executes inline where supported — useful for tests; confirm on your
  version.
- Assert that failures are logged (`frappe.log_error`) and do not silently disappear.
- For scheduler changes, run `bench --site <site> migrate` (scheduler events are registered on
  migrate) and confirm the job is registered and runs.
- After a restore, verify the scheduler is enabled; tests on a restored site can pass while scheduled
  work is dead.

## 8. API and integration failure tests

- Success response schema and status.
- Authentication failure, missing permission, invalid payload, wrong content type.
- Downstream timeout, 5xx, rate limit, and malformed response.
- Duplicate webhook/idempotency key: the second delivery must not double-apply.
- Partial failure in a batch: what is retried, what is rejected, what is logged.
- Never call a real third-party endpoint from an automated test; use a fake or a sandbox with
  explicit credentials.

## 9. Migration and deployment tests

- Migration: dry run on a production-like copy, idempotent re-run, reconciliation report. See
  `data-migration.md`.
- Deployment: run the smoke list in `assets/templates/deployment-runbook.md` after every release.
- Backup: execute the restore drill in `assets/templates/backup-restore-test.md`; a scheduled backup
  without a restore result is unverified.

## 10. UAT and client sign-off

UAT is a business acceptance activity, not a developer smoke test.

- Use `assets/templates/uat-signoff.md`.
- Scripts are written in business language with real data and expected outcomes.
- The client's named user executes them; the implementer observes and records.
- Distinguish "passed", "passed with observation", "failed", and "not tested".
- Sign-off includes date, name, role, environment, and version.
- Do not record client sign-off that did not happen.

## 11. Delivery test note

Every delivery includes `assets/templates/delivery-test-note.md` with:

- Change/delivery identifier and environment/version.
- Requirements tested and acceptance criteria.
- Test cases, expected vs actual.
- Commands/evidence (test output, screenshot, report, reconciliation).
- Failures, limitations, skipped checks, and outstanding risks.
- Automated vs manual vs client sign-off, tester, date.

If the note cannot be completed because something was not run, write "not run" and why. An honest
gap is manageable; a fabricated pass is not.

## 12. Test quality rules

- A test that cannot fail is not a test. Assert the behavior, not that no exception occurred.
- Do not weaken or delete an assertion to make a suite green. Fix the cause, or document why the
  behavior changed and get approval.
- Do not add `skip` to avoid an environment problem; fix the environment or report the limitation.
- Avoid time-dependent tests; pass explicit dates where the API allows it.
- Avoid order-dependent tests; each test sets up its own state.
- Keep tests fast enough to run on every change.
- When fixing a production defect, add a regression test that fails before the fix and passes after.

## 13. Pre-delivery QA checklist

- [ ] Version detected; tests use the conventions of that version.
- [ ] Targeted tests added/updated for the change.
- [ ] App test suite run; failures read, not filtered away.
- [ ] Permission behavior tested as a non-privileged user.
- [ ] Failure path tested (invalid input, downstream error, duplicate delivery).
- [ ] Migration/reconciliation evidence attached if data moved.
- [ ] Backup restore evidence current if the release affects recovery.
- [ ] Smoke test executed in the target environment.
- [ ] Branding verified if identity changed.
- [ ] Delivery test note completed with real results and limitations.
- [ ] UAT/sign-off recorded separately, with names and dates.
