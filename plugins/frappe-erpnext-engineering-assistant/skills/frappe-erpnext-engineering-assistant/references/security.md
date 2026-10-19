# Security, Privacy, and Licensing

Security is part of correctness. A feature that works but exposes another customer's data is a
defect, not a trade-off. This reference covers the controls a Frappe/ERPNext implementation must
get right, plus the licensing boundary that white-labeling runs into.

## 1. Authorization is not authentication

A logged-in user is not an authorized user. Frappe's permission model has several layers; use the
layer that matches the question.

| Question | Mechanism |
|---|---|
| Can this role use this DocType at all? | Role + DocPerm (Role Permission Manager) |
| Can this role read/write/submit/cancel? | DocPerm `read`/`write`/`create`/`submit`/`cancel`/`delete` |
| Can this role see this *field*? | `permlevel` on the field + DocPerm at that level |
| Can this user see this *row*? | User Permissions, `permission_query_conditions`, `has_permission` |
| Can this user act on this *document*? | `doc.check_permission("write")` / `frappe.has_permission(..., doc=doc)` |
| Can this website user see this page? | `has_website_permission` |

Rules:

- `@frappe.whitelist()` means "reachable over HTTP by an authenticated session", **not** "allowed".
  Check the permission explicitly.
- For row scoping, `permission_query_conditions` must return a valid SQL `WHERE` fragment with
  escaped values (`frappe.db.escape(user)`), or use Query Builder criteria where possible.
- In v16, `has_permission` hooks must return an explicit `True` to allow. Do not return `None` and
  assume a fallback; the v16 migration guide tightened this.
- Never use `ignore_permissions=True` to make a failing flow work. It is acceptable only for
  system-created records (setup, migration, integrations acting as the system), with a comment
  naming the reason.
- Do not implement security in JavaScript. Hiding a button or field is UX, not access control.
- `frappe.only_for(("System Manager",))` is a role gate, not a substitute for document permission.

```python
@frappe.whitelist(methods=["POST"])
def cancel_application(name: str):
    doc = frappe.get_doc("Loan Application", name)
    doc.check_permission("cancel")          # document-level
    frappe.has_permission("Loan Application", "cancel", doc=doc, throw=True)
    ...
```

## 2. Whitelisted methods and APIs

Every whitelisted function is a public endpoint of the site.

- Use type hints on arguments; Frappe validates them on recent versions, and they document intent.
- Use `methods=["POST"]` for anything that changes state. v16 additionally requires POST for several
  core state-changing endpoints (`logout`, `upload_file`, `send_login_link`, …).
- `allow_guest=True` only with an explicit reason, strict input validation, rate limiting, and no
  data exposure. Guest endpoints are unauthenticated by definition.
- Return only what the caller needs. Do not return a full document when three fields are used.
- Do not trust client-supplied doctype/field names in dynamic queries; whitelist them.
- API keys/secrets belong in the client's secret store, never in front-end code.
- Rate limiting: implement at the reverse proxy and/or in the endpoint. Do not assume the framework
  provides per-endpoint limits; verify what the deployment actually enforces.
- For inbound webhooks, verify a signature or shared secret before processing, and make the handler
  idempotent.

## 3. SQL injection

- Prefer Query Builder (`frappe.qb`) or `frappe.get_all`/`get_list` with structured filters.
- Raw SQL only when necessary, always with named parameters:

```python
frappe.db.sql(
    "select name from `tabSales Invoice` where customer = %(customer)s and docstatus = 1",
    {"customer": customer},
)
```

- Never build SQL with f-strings, `%` formatting, `.format()`, or string concatenation — including
  `order_by`, `group_by`, table names, and field names.
- If a field or direction must be dynamic, map it through an allowlist:

```python
SORTABLE = {"posting_date": "posting_date", "grand_total": "grand_total"}
order_by = SORTABLE.get(requested, "posting_date")
```

- `frappe.db.escape` is for values in permission query fragments, not a license to concatenate
  arbitrary SQL.

## 4. Output encoding and XSS

- Jinja templates escape output by default. `|safe`, `{{ ... }}` inside string-built HTML, and
  direct DOM insertion bypass that protection.
- Rich-text/HTML fields must be sanitized **on the server** before storage or rendering.
  `frappe.utils.sanitize_html` is the framework helper: v15 uses bleach, v16 uses nh3 and strips
  forbidden tags instead of escaping them. Behavior differs; test the actual output.
- Print formats and portal pages are rendered HTML. Treat every user-supplied value as untrusted,
  including names, addresses, remarks, and uploaded file names.
- Do not interpolate user input into inline `<script>` or event-handler attributes.
- When rendering a Jinja variable inside an attribute, quote it and keep autoescaping enabled.

## 5. File uploads and file access

- Set `is_private=1` for anything not intentionally public. A public file URL is accessible without
  a session.
- Validate extension, declared MIME type, and actual content. Do not trust the filename; normalize it
  and reject path separators and traversal sequences.
- Enforce a size limit at the proxy and in the application. Verify the effective limit.
- Restrict executable/script extensions. Store uploads outside executable paths; never serve user
  uploads from a directory that can execute code.
- Check permission on the attached document before returning or deleting a file.
- Migrations that copy attachments must preserve privacy flags and verify checksums/counts; a public
  copy of a private document is a data leak.

## 6. Secrets and configuration

- Never commit `site_config.json`, `common_site_config.json`, `.env` files, private keys, API tokens,
  database dumps, or customer exports. Keep them out of the repository and out of chat/prompts.
- External service credentials belong in the environment or the site's secret store, read through
  configuration — not hardcoded in Python or JS.
- Do not log secrets, session IDs, authorization headers, or full request bodies containing PII.
- Rotate credentials after any suspected exposure; removing a secret from the latest commit does not
  remove it from history or from anyone who already read it.
- Use separate credentials per environment. A staging key must not be able to touch production.
- Encryption keys and backup passphrases need an owner, a storage location, and a recovery procedure.

## 7. Logging and observability

- `frappe.log_error(title=..., message=frappe.get_traceback())` for unexpected failures; include the
  document and operation, not the payload.
- Log identifiers, not personal data. If an identifier is sensitive, hash or truncate it.
- Do not use `print()` or `console.log` as production telemetry.
- Error Log entries are visible to System Managers; treat them as semi-public within the site.
- For AI features, log the decision, tool calls, and approvals — not the raw sensitive prompt.

## 8. Dependencies and supply chain

- Pin versions in the app's dependency manifest; do not depend on an unpinned branch in production.
- Before adding a dependency, check maintenance status, license, and known vulnerabilities.
- Prefer framework utilities over adding a package for a small task.
- Review patches and migrations from third-party apps before running them on production.
- Do not vendor unknown binaries or run install scripts from untrusted sources.

## 9. Multi-tenancy and isolation

- The standard isolation boundary is **one site per tenant**, with separate databases and site
  directories. A shared site with row-level filters is a weaker boundary and must be designed,
  tested, and reviewed as such.
- Never query another site's database from application code.
- Scheduler jobs and background workers must set/respect the site context; a job that runs without a
  site or with the wrong site can write to the wrong tenant.
- User Permissions and `permission_query_conditions` must be tested with a tenant-A user against
  tenant-B records.
- Shared Redis/cache and shared file storage need namespacing; verify keys and paths do not collide.
- White-label deployments must confirm that branding, email, domains, and backups are tenant-scoped.

## 10. Privacy and data lifecycle

- Declare personal-data DocTypes in the `user_data_fields` hook so framework download/deletion tools
  can find them.
- Know where PII lives: DocTypes, comments, communications, attachments, error logs, backups, and
  analytics exports.
- Define retention per data class; do not keep backups forever by default.
- Deletion must cover child tables, attachments, linked communications, and search indexes — not just
  the parent row.
- Test the deletion path on a copy, not on production.
- Data migration must not widen access: preserve privacy flags, permissions, and ownership.

## 11. AI-specific security

See `ai-features.md`. In short: AI output is untrusted input; tool access must be least-privilege;
document content is a prompt-injection vector; consequential actions need human approval; and AI
must not bypass Frappe permissions or validations.

## 12. Licensing, attribution, and trademarks

This is an engineering boundary, not legal advice. Verify with the client's counsel before
committing to a white-label distribution model.

| Component | License (verified 2026-10-19) | Practical implication |
|---|---|---|
| Frappe Framework | MIT | Permissive; preserve copyright and license notices in copies/substantial portions |
| ERPNext | GPLv3 | Distributing modified ERPNext triggers GPL source-availability obligations; internal use is different from distribution |
| ERPNext documentation | CC-BY-SA-3.0 | Attribution and share-alike apply to adapted docs |
| Frappe/ERPNext names and logos | Trademark policy published by Frappe | Technical removal of a logo is not the same as a right to use or imply endorsement |

Rules:

1. Do not delete copyright headers or license files from framework or ERPNext source as a "branding"
   step. That is a licensing change, not a theme change.
2. Distinguish **internal deployment** (client uses the system) from **distribution** (client sells or
   gives the modified product to third parties). GPL obligations differ materially.
3. A white-label contract should state which components are modified, how source is made available,
   and who owns custom code.
4. Do not state a legal conclusion. Identify the question, cite the license, and recommend qualified
   review.
5. Do not use upstream trademarks in a way that suggests endorsement or origin.

## 13. Pre-finish security checklist

- [ ] Every whitelisted method checks permission, not just login.
- [ ] State-changing endpoints use POST; guest endpoints are justified and rate-limited.
- [ ] Row-level scoping tested with a non-privileged user.
- [ ] `permlevel` used for sensitive fields; JS hiding is not the control.
- [ ] No SQL string interpolation; dynamic sort/field names are allowlisted.
- [ ] User HTML/rich text sanitized server-side; no unescaped `|safe` on user data.
- [ ] Uploads are private by default, type/size validated, and access-checked.
- [ ] No secrets, PII, or customer data in code, config committed to Git, logs, or fixtures.
- [ ] Error messages do not leak internal paths, SQL, or stack traces to end users.
- [ ] Backup/export access is restricted and encrypted; retention is defined.
- [ ] Personal-data hooks (`user_data_fields`) updated for new DocTypes.
- [ ] Licensing/trademark implications reviewed if branding or distribution is involved.
