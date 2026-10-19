# Security Policy

This repository is instruction content for AI coding agents. It ships no server, no runtime code, and
no data processing. The security risks here are different from a typical library:

- guidance that would lead an agent to weaken authorization, leak credentials, or damage production data;
- guidance that is wrong in a way that silently removes a protection (for example a permission check);
- repository content that contains a secret, credential, or customer datum;
- a validation script that can be bypassed or that gives false confidence.

## Supported versions

| Version | Supported |
|---|---|
| 2.x | Yes |
| 1.x | No (superseded; upgrade to 2.x) |

Guidance targets Frappe Framework/ERPNext **v15 and v16**. Reports about v14-or-earlier or v17-or-later
behavior are out of scope for support claims, though factual corrections with sources are welcome.

## Reporting a vulnerability

Please report privately. Do not open a public issue for a security problem.

1. Use GitHub's private vulnerability reporting (Security → Advisories → "Report a vulnerability") on
   this repository. If that is unavailable, contact the maintainers through the repository's published
   contact channel.
2. Do not include real credentials, customer data, or production dumps in the report. Redact and
   describe instead.

Please include:

- The file and section (or the prompt and the behavior you observed).
- What the guidance says and why it is unsafe.
- The failure mode: what an agent would do wrong, and the impact (data exposure, data loss, privilege
  escalation, outage).
- A suggested correction, if you have one, with a source where possible.
- Whether you want credit in the changelog.

## What to expect

- Acknowledgment on a best-effort basis; this project has no paid support and no response SLA.
- We will confirm the issue, decide whether guidance needs correcting, and ship a fix in a release.
- Credit on request, in the changelog entry for the fix.

## Out of scope

- The behavior of third-party AI models or agents themselves.
- A client's own Frappe/ERPNext deployment, configuration, or data.
- Legal conclusions about licensing or trademarks (see the licensing section of the security reference
  for where to look, and consult qualified counsel).
- Reports that require access to a system you do not own.

## Handling secrets in this repository

If you find a credential, key, or personal datum committed here, report it privately and do not
reproduce it publicly. Removing a value from the latest commit does not remove it from history;
maintainers should treat any confirmed exposure as a rotation event.

Repository contributors: never commit secrets, tokens, customer data, or production exports. The
validator scans for common credential patterns in CI, but it is a safety net, not a guarantee.
