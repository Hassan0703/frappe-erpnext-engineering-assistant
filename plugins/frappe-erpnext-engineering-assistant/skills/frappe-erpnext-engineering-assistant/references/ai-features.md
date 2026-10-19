# AI Features and Agents in Frappe/ERPNext

AI can draft, classify, summarize, extract, and suggest. It must not become an unaudited path around
Frappe's permissions, validations, or approval workflows.

**Core rule:** model output is untrusted input. Valid JSON is not correct data, and a confident
sentence is not authorization.

## 1. Start with a written use case

Before building, write:

- The business decision or task the AI supports.
- Who uses it, and which role/permission they have.
- Inputs (DocTypes, fields, documents, emails) and their sensitivity.
- Expected output and **measurable acceptance criteria** (accuracy threshold, allowed error rate,
  latency, cost per operation).
- What happens when the model is wrong, unavailable, slow, or too expensive.
- Whether the action is advisory (human decides) or consequential (creates/changes/sends money or
  documents).
- The named operational owner and the kill switch.

If the use case is "add AI", stop. Pick a task with a measurable outcome.

## 2. Architecture boundaries

| Layer | Rule |
|---|---|
| Browser | Never holds provider API keys. May call a whitelisted server method. |
| Server | Owns credentials, prompt templates, tool registry, validation, logging, quotas. |
| Background job | Use `frappe.enqueue` for long calls; never hold a web request open for a slow model. |
| Provider | Receives the minimum data required; no secrets; documented retention/training terms. |
| Database | Stores approved outputs and audit metadata; never stores raw secrets in logs. |

Prefer a **single server-side gateway module** (e.g. `<app>/<module>/ai/client.py`) over scattered
provider calls. One place to enforce timeouts, retries, redaction, and logging.

## 3. Tool and API access

If the model can call tools:

- Define an explicit **registry** of allowed tools. Never let the model name an arbitrary method,
  DocType, or SQL query.
- Each tool maps to a narrow server function with a typed schema and a documented side effect.
- Pass the **calling user's** identity into every tool. The tool checks permission as that user;
  never execute tools as Administrator to "make it work".
- Read tools and write tools are separate. Write tools are opt-in per use case.
- No raw SQL tool. No shell tool. No file-system tool. No arbitrary HTTP fetch.
- Tool arguments are untrusted: validate types, ranges, doctype/field allowlists, and ownership.
- Rate-limit per user and per site; cap tool calls per request.

```python
TOOLS = {
    "get_customer_balance": get_customer_balance,   # read, permission-checked
    "draft_quotation": draft_quotation,             # write, creates a DRAFT only
}
```

## 4. Authorization and least privilege

- AI must not bypass `frappe.has_permission`, `doc.check_permission`, `permlevel`, or user
  permissions. If the user cannot read a document, the model cannot summarize it.
- Scope retrieval to the user's allowed companies/territories; do not retrieve globally then filter
  in the prompt.
- A model suggestion does not grant authority. Approval by a human with the right role is still
  required for submit/cancel/pay/send/delete.
- Secrets and provider keys live in encrypted settings, read server-side
  (`frappe.utils.password.get_decrypted_password` where appropriate — verify on your version), never
  in client code or boot data.
- Log the acting user, not a shared service account, for consequential actions.

## 5. Prompt injection and untrusted content

Every document, email, comment, attachment, web page, and OCR result is untrusted content.

- Separate **instructions** from **data**. Put retrieved content in a delimited data section and tell
  the model it is data, not instructions.
- Never let retrieved content choose tools, change system prompts, or set approval flags.
- Strip or neutralize obvious instruction patterns; cap length; prefer structured fields over raw
  HTML/email bodies.
- Treat URLs, file names, and metadata as attacker-controlled.
- Do not auto-follow links or execute code suggested by content.
- Test with adversarial documents: "ignore previous instructions", fake approvals, hidden text,
  prompt leakage requests.
- If the model can write to a DocType, validate the resulting document with normal server-side rules
  and require human review before submit.

## 6. Input and output validation

Inputs:

- Validate types, lengths, and allowed values before calling the model.
- Minimize: send only the fields needed for the task.
- Redact or tokenize identifiers when full values are not required.

Outputs:

- Require a schema (JSON schema/pydantic or explicit parser). Reject anything that does not conform.
- Validate domain rules: doctype exists, link targets exist, amounts non-negative, dates in range,
  enum values allowed, currency matches.
- Never insert model output directly with `ignore_permissions=True`.
- Create drafts, not submitted documents, unless a human approved the exact content.
- Preserve provenance: which model, prompt version, input references, and confidence.

## 7. Human approval for consequential actions

Require explicit human approval for anything that:

- Submits, cancels, or deletes a document.
- Moves money, changes prices, taxes, credit limits, or payroll.
- Sends email/SMS to customers or suppliers.
- Changes permissions, users, or configuration.
- Writes to production data in bulk.

The approval UI must show the **diff or exact payload**, not just "Approve?". Record who approved,
when, and what they saw. Approval must be enforced server-side; a UI checkbox is not a control.

## 8. Audit and traceability

Store, per AI operation:

- Timestamp, site, user, feature/use case.
- Model/provider and prompt/template version.
- Input references (document names, not full sensitive text).
- Tool calls and arguments (redacted where needed).
- Output/decision and confidence, if provided.
- Human approval/rejection and the approver.
- Latency, token usage, cost estimate, and error/fallback path.

Keep audit records immutable enough for review; define retention. Do not log secrets, full prompts
containing PII, or raw attachments.

## 9. Rate limits, cost, retries, and failure handling

- Per-user and per-site quotas; maximum input/output tokens; maximum tool calls.
- Timeouts on every provider call. Never allow an unbounded request.
- Retries only for transient failures, with backoff and an idempotency key for writes.
- Circuit breaker: after repeated failures, stop calling and fall back.
- Cost budget and alerting; track spend per feature and per tenant.
- Fail closed for consequential actions; fail open only for explicitly safe advisory features.
- If the model is unavailable, the manual workflow must still work. Design it first.

## 10. Evaluation and regression

- Build a dataset of representative, anonymized cases with expected outcomes or a rubric.
- Include edge cases, adversarial inputs, and past failures.
- Run the evaluation before changing a prompt, model, or tool schema; compare against the last run.
- Track accuracy, false positives/negatives, refusal rate, latency, and cost.
- A prompt change is a code change: review it, version it, and record the eval result.
- Do not ship a model change based on one happy-path demo.

## 11. Monitoring, fallback, and ownership

Monitor:

- Error/timeout rate and provider status.
- Latency and token/cost per operation.
- Human override/rejection rate (a rising rate means the model is wrong).
- Refusal and empty-output rates.
- Prompt-injection or policy violations detected.
- Data-retention/compliance events.

Provide a documented kill switch that disables the feature without a deployment. Name an owner for
prompts, model versions, costs, incidents, and data-processing terms.

## 12. Privacy and compliance

- Send the minimum personal data required; prefer IDs over names where the task allows.
- Confirm the provider's retention, training, and region terms; record them.
- Do not send credentials, encryption keys, full payment data, or health data without explicit
  approval and a lawful basis.
- Honor deletion/retention obligations for AI logs as for other personal data.
- Add AI-related DocTypes to `user_data_fields` if they store personal data.

## 13. Anti-patterns

- API key in JavaScript or a public DocType.
- Model output inserted with `ignore_permissions=True`.
- A "tool" that runs arbitrary SQL, shell, or HTTP.
- Letting document text alter the system prompt or tool list.
- Auto-submitting invoices because the JSON parsed.
- Logging full prompts containing customer data.
- No timeout, no quota, no cost visibility.
- No evaluation set; quality judged by demos.
- No human owner or kill switch.

## 14. Checklist

- [ ] Use case, users, data, acceptance criteria, and owner written down.
- [ ] Server-side gateway; no keys in the browser.
- [ ] Tool registry with allowlists; tools run as the calling user with permission checks.
- [ ] Inputs minimized and validated; outputs schema-validated and domain-validated.
- [ ] Untrusted content isolated; injection tests pass.
- [ ] Human approval enforced server-side for consequential actions.
- [ ] Audit trail records model/prompt version, tools, decision, approver, cost.
- [ ] Timeouts, quotas, retries with idempotency, circuit breaker, fallback workflow.
- [ ] Evaluation dataset and regression run recorded.
- [ ] Monitoring, kill switch, and named ownership in place.
- [ ] Privacy/retention terms reviewed; AI data included in deletion scope.
