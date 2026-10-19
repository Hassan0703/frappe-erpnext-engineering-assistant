#!/usr/bin/env python3
"""Structural validation for the frappe-erpnext-engineering-assistant repository.

The product is Markdown guidance for AI coding agents, so the failure modes that matter are
structural: invalid manifests, frontmatter the agent cannot parse, links to references that do not
exist, orphaned references, templates that never reach the installed plugin, unsupported version
claims, and secrets committed by accident.

This script uses only the standard library. It is run by CI and can be run locally:

    python3 scripts/validate_repo.py

Exit status is 0 when no errors were found, 1 otherwise. Warnings do not fail the build.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "plugins" / "frappe-erpnext-engineering-assistant" / "skills" / "frappe-erpnext-engineering-assistant"
REFERENCES = SKILL_DIR / "references"
TEMPLATES = ROOT / "docs" / "templates"
BUNDLED_TEMPLATES = SKILL_DIR / "assets" / "templates"
PLUGIN_MANIFEST = ROOT / "plugins" / "frappe-erpnext-engineering-assistant" / ".claude-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
SKILL_MD = SKILL_DIR / "SKILL.md"
TEMPLATE_INDEX = TEMPLATES / "README.md"
AUDIT_DIR = ROOT / "docs" / "audit"

# The audit documents deliberately quote the baseline defects (including the old "v15+" claim) as
# historical evidence, so they are exempt from the version-phrasing scan.
PHRASING_EXEMPT_DIRS = (AUDIT_DIR,)

# Intentional inventory. A new reference or template must be added here (and to the index), so the
# set of shipped artifacts stays a deliberate decision rather than an accident. These lists are
# checked for both missing and unexpected entries.
REQUIRED_REFERENCES = frozenset(
    {
        "ai-features.md",
        "client-patterns.md",
        "code-placement.md",
        "data-migration.md",
        "deployment-and-operations.md",
        "erp-implementation.md",
        "hooks-and-customization.md",
        "performance.md",
        "reports-and-printing.md",
        "review-checklist.md",
        "security.md",
        "server-patterns.md",
        "support-and-incidents.md",
        "testing-and-qa.md",
        "version-compatibility.md",
        "white-labeling.md",
    }
)

REQUIRED_TEMPLATES = frozenset(
    {
        "backup-restore-test.md",
        "configuration-inventory.md",
        "cutover-checklist.md",
        "data-mapping.md",
        "defect-report.md",
        "delivery-test-note.md",
        "deployment-runbook.md",
        "environment-inventory.md",
        "fit-gap-analysis.md",
        "handover-checklist.md",
        "incident-report.md",
        "migration-plan.md",
        "migration-reconciliation.md",
        "migration-run-log.md",
        "permissions-matrix.md",
        "project-discovery.md",
        "regression-checklist.md",
        "release-and-rollback.md",
        "requirements-and-acceptance.md",
        "technical-design.md",
        "test-plan.md",
        "uat-signoff.md",
        "white-label-discovery.md",
        "white-label-implementation-plan.md",
        "white-label-upgrade-checklist.md",
        "white-label-verification.md",
    }
)

# The white-labeling guide is only useful if every client-visible surface the engagement brief names
# is actually covered. These checks are presence-only and deliberately coarse: they fail when a
# surface disappears entirely, and cannot judge whether the guidance for it is correct. That part is
# a human-review responsibility and is recorded as such in the reference itself.
# Inherited branding from the project's origin. The MIT licence and the NOTICE must keep the
# original copyright/attribution, the changelog records the rename, and the audit documents are
# historical evidence, so those are exempt. Every other shipped file must carry the new identity.
# ``validate_repo.py`` holds the patterns themselves and is skipped, as in the secret scan.
BRANDING_EXEMPT_NAMES = frozenset({"LICENSE", "NOTICE", "CHANGELOG.md", "validate_repo.py"})
BRANDING_EXEMPT_DIRS = (AUDIT_DIR,)
INHERITED_BRANDING = [
    (re.compile(r"frappe-code-standards", re.I), "old product/plugin slug"),
    (re.compile(r"nextash", re.I), "old organisation/marketplace name"),
    (re.compile(r"faisal[- ]zahoor", re.I), "inherited author credit"),
]

# A line that removes, renames, or explains the previous product is not branding. Upgrade
# instructions must name the old plugin and marketplace exactly, so those lines are allowed.
BRANDING_CONTEXT_RE = re.compile(
    r"\b(?:uninstall|remove|renamed|rename|previous|formerly|previously|migrat(?:e|ion))\b",
    re.IGNORECASE,
)

# Every pattern for a surface must appear (case-insensitive) somewhere in the guide.
WHITE_LABEL_SURFACES: list[tuple[str, tuple[str, ...]]] = [
    ("desk", (r"\bdesk\b",)),
    ("login", (r"\blogin\b",)),
    ("navbar and workspace", (r"navbar", r"workspace")),
    ("website and portal", (r"website", r"portal")),
    ("application metadata", (r"app_title", r"app_logo_url")),
    ("logo, favicon and assets", (r"logo", r"favicon", r"assets")),
    ("email and notifications", (r"email", r"notification")),
    ("print and PDF", (r"print", r"pdf")),
    ("translations and terminology", (r"translation", r"terminology")),
    ("PWA / mobile", (r"pwa", r"mobile")),
    ("multi-tenant separation", (r"multi-tenant",)),
    ("upgrade and asset rebuild", (r"upgrade", r"bench build")),
    ("licensing and trademarks", (r"licens", r"trademark")),
    ("verification procedure", (r"verification",)),
    ("configuration-only class", (r"configuration-only",)),
    ("supported custom-app class", (r"custom-app",)),
    ("hook class", (r"hook",)),
    ("fixture class", (r"fixture",)),
    ("patch or migration class", (r"patch", r"migration")),
    ("framework-fork class", (r"framework fork", r"core modification")),
]

errors: list[str] = []
warnings: list[str] = []


def error(message: str) -> None:
    errors.append(message)


def warn(message: str) -> None:
    warnings.append(message)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def markdown_files() -> list[Path]:
    skip = {".git", "node_modules", "__pycache__"}
    return sorted(
        p
        for p in ROOT.rglob("*.md")
        if not any(part in skip for part in p.parts)
    )


def strip_code_fences(text: str) -> str:
    """Remove fenced code blocks so examples are not scanned for links or phrasing."""
    out: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return "\n".join(out)


# --------------------------------------------------------------------------------------- manifests


def load_json(path: Path) -> dict | None:
    """Parse a JSON file, reporting a clean error instead of raising."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        error(f"{rel(path)}: invalid JSON ({exc})")
        return None


def check_manifests() -> None:
    json_files = [p for p in ROOT.rglob("*.json") if ".git" not in p.parts]
    if not json_files:
        error("no JSON manifests found")
        return

    for path in json_files:
        load_json(path)

    if not PLUGIN_MANIFEST.exists():
        error(f"missing plugin manifest: {rel(PLUGIN_MANIFEST)}")
        return

    plugin = load_json(PLUGIN_MANIFEST)
    if plugin is None:
        return
    for key in ("name", "version", "description"):
        if not plugin.get(key):
            error(f"{rel(PLUGIN_MANIFEST)}: missing required key '{key}'")
    version = str(plugin.get("version", ""))
    # Semantic versioning including an optional pre-release/build suffix (e.g. 2.0.0-beta.1).
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?", version):
        error(f"{rel(PLUGIN_MANIFEST)}: version '{version}' is not semver (MAJOR.MINOR.PATCH)")
    if plugin.get("name") != SKILL_DIR.name:
        warn(
            f"{rel(PLUGIN_MANIFEST)}: plugin name '{plugin.get('name')}' differs from skill "
            f"directory '{SKILL_DIR.name}'"
        )

    if not MARKETPLACE.exists():
        error(f"missing marketplace manifest: {rel(MARKETPLACE)}")
        return

    market = load_json(MARKETPLACE)
    if market is None:
        return
    if not market.get("name"):
        error(f"{rel(MARKETPLACE)}: missing 'name'")
    plugins = market.get("plugins") or []
    if not plugins:
        error(f"{rel(MARKETPLACE)}: no plugins declared")
    for entry in plugins:
        source = entry.get("source")
        if not source:
            error(f"{rel(MARKETPLACE)}: plugin '{entry.get('name')}' has no source")
            continue
        source_path = (MARKETPLACE.parent.parent / source).resolve()
        if not source_path.exists():
            error(f"{rel(MARKETPLACE)}: plugin source does not exist: {source}")
        elif not (source_path / ".claude-plugin" / "plugin.json").exists():
            error(f"{rel(MARKETPLACE)}: plugin source has no .claude-plugin/plugin.json: {source}")

    marketplace_names = {entry.get("name") for entry in plugins}
    if plugin.get("name") not in marketplace_names:
        error(
            f"{rel(MARKETPLACE)}: does not declare the plugin '{plugin.get('name')}' that "
            f"{rel(PLUGIN_MANIFEST)} defines"
        )
    if not isinstance(market.get("owner"), dict) or not market["owner"].get("name"):
        error(f"{rel(MARKETPLACE)}: missing owner.name")
    if not isinstance(plugin.get("author"), dict) or not plugin["author"].get("name"):
        error(f"{rel(PLUGIN_MANIFEST)}: missing author.name")
    keywords = plugin.get("keywords")
    if not isinstance(keywords, list) or not all(isinstance(k, str) and k for k in keywords):
        error(f"{rel(PLUGIN_MANIFEST)}: 'keywords' must be a list of non-empty strings")
    if not isinstance(plugin.get("license"), str) or not plugin["license"].strip():
        error(f"{rel(PLUGIN_MANIFEST)}: missing 'license'")

    changelog = ROOT / "CHANGELOG.md"
    if changelog.exists():
        match = re.search(
            r"^##\s*\[?(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)",
            changelog.read_text(encoding="utf-8"),
            re.M,
        )
        if not match:
            warn("CHANGELOG.md: no version heading found (expected '## x.y.z')")
        elif match.group(1) != version:
            error(
                f"version mismatch: plugin.json is {version} but CHANGELOG.md starts at "
                f"{match.group(1)}"
            )
    else:
        warn("CHANGELOG.md is missing")


# ------------------------------------------------------------------------------------ skill frontmatter


def check_skill() -> None:
    if not SKILL_MD.exists():
        error(f"missing skill entry point: {rel(SKILL_MD)}")
        return

    text = SKILL_MD.read_text(encoding="utf-8")
    if not text.startswith("---"):
        error(f"{rel(SKILL_MD)}: missing YAML frontmatter")
        return

    end = text.find("\n---", 3)
    if end == -1:
        error(f"{rel(SKILL_MD)}: frontmatter is not closed with '---'")
        return

    frontmatter = text[3:end]
    fields: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            warn(f"{rel(SKILL_MD)}: frontmatter line is not 'key: value': {line.strip()}")
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()

    name = fields.get("name", "")
    description = fields.get("description", "")

    if not name:
        error(f"{rel(SKILL_MD)}: frontmatter missing 'name'")
    else:
        if name != SKILL_DIR.name:
            error(f"{rel(SKILL_MD)}: name '{name}' must match directory '{SKILL_DIR.name}'")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
            error(f"{rel(SKILL_MD)}: name '{name}' must be lowercase alphanumeric with hyphens")
        if len(name) > 64:
            error(f"{rel(SKILL_MD)}: name exceeds 64 characters")

    if not description:
        error(f"{rel(SKILL_MD)}: frontmatter missing 'description'")
    elif not 1 <= len(description) <= 1024:
        error(
            f"{rel(SKILL_MD)}: description must be 1-1024 characters (found {len(description)})"
        )

    if not fields.get("license"):
        warn(f"{rel(SKILL_MD)}: frontmatter has no 'license' field (portable across agents)")

    # The description is the only routing signal the agent sees before loading the skill.
    for topic in ("v15", "v16", "white-label", "deploy", "migration", "test"):
        if topic.lower() not in description.lower():
            warn(f"{rel(SKILL_MD)}: description does not mention '{topic}' (discoverability)")


# ------------------------------------------------------------------------------- reference inventory


def check_references() -> None:
    if not REFERENCES.is_dir():
        error(f"missing references directory: {rel(REFERENCES)}")
        return

    skill_text = SKILL_MD.read_text(encoding="utf-8") if SKILL_MD.exists() else ""
    on_disk = {p.name for p in REFERENCES.glob("*.md")}
    linked = set(re.findall(r"references/([A-Za-z0-9._-]+\.md)", skill_text))

    for name in sorted(on_disk - linked):
        error(f"{rel(REFERENCES / name)}: not linked from SKILL.md (orphaned reference)")
    for name in sorted(linked - on_disk):
        error(f"{rel(SKILL_MD)}: links to missing reference 'references/{name}'")
    if not on_disk:
        error(f"{rel(REFERENCES)}: no reference documents found")

    for name in sorted(REQUIRED_REFERENCES - on_disk):
        error(f"required reference missing: references/{name}")
    for name in sorted(on_disk - REQUIRED_REFERENCES):
        error(
            f"unexpected reference references/{name} "
            "(add it to REQUIRED_REFERENCES and the SKILL.md index)"
        )

    # The numbered index at the end of SKILL.md is the human-facing catalogue; a reference linked
    # only from the routing table is easy to miss when the list is edited.
    index_entries = re.findall(
        r"^\d+\.\s+`references/([A-Za-z0-9._-]+\.md)`", skill_text, re.M
    )
    for name in sorted(on_disk - set(index_entries)):
        error(f"{rel(SKILL_MD)}: reference index does not list references/{name}")
    for name in sorted(set(index_entries) - on_disk):
        error(f"{rel(SKILL_MD)}: reference index lists missing references/{name}")
    for name in sorted({n for n in index_entries if index_entries.count(n) > 1}):
        error(f"{rel(SKILL_MD)}: reference index lists references/{name} more than once")


# -------------------------------------------------------------------------------- template inventory


def check_templates() -> None:
    if not TEMPLATES.is_dir():
        error(f"missing templates directory: {rel(TEMPLATES)}")
        return

    templates = sorted(p for p in TEMPLATES.glob("*.md") if p.name != "README.md")
    if not templates:
        error(f"{rel(TEMPLATES)}: no templates found")
        return

    template_names = {p.name for p in templates}
    for name in sorted(REQUIRED_TEMPLATES - template_names):
        error(f"required template missing: {rel(TEMPLATES / name)}")
    for name in sorted(template_names - REQUIRED_TEMPLATES):
        error(
            f"unexpected template {rel(TEMPLATES / name)} "
            "(add it to REQUIRED_TEMPLATES and the template index)"
        )

    if not TEMPLATE_INDEX.exists():
        error(f"missing template index: {rel(TEMPLATE_INDEX)}")
    else:
        index_text = TEMPLATE_INDEX.read_text(encoding="utf-8")
        listed_all = re.findall(r"\]\(([A-Za-z0-9._-]+\.md)\)", index_text)
        listed = set(listed_all)
        names = {p.name for p in templates}
        for name in sorted(names - listed):
            error(f"{rel(TEMPLATE_INDEX)}: template '{name}' is not listed in the index")
        for name in sorted(listed - names):
            error(f"{rel(TEMPLATE_INDEX)}: lists '{name}' which does not exist")
        for name in sorted({n for n in listed_all if listed_all.count(n) > 1}):
            error(f"{rel(TEMPLATE_INDEX)}: lists '{name}' more than once")
        if "docs/templates" not in index_text:
            warn(f"{rel(TEMPLATE_INDEX)}: should state the canonical template location")

    # Bundled copies must exist and match (the plugin cannot reach outside its own directory).
    if not BUNDLED_TEMPLATES.is_dir():
        error(
            "missing bundled templates "
            f"({rel(BUNDLED_TEMPLATES)}); run: python3 scripts/sync_templates.py"
        )
        return

    for src in templates:
        dst = BUNDLED_TEMPLATES / src.name
        if not dst.exists():
            error(f"bundled template missing: {rel(dst)} (run scripts/sync_templates.py)")
        elif dst.read_bytes() != src.read_bytes():
            error(f"bundled template out of date: {rel(dst)} (run scripts/sync_templates.py)")
    for extra in sorted(p.name for p in BUNDLED_TEMPLATES.glob("*.md")):
        if extra not in {p.name for p in templates}:
            error(f"bundled template has no source: {extra} (run scripts/sync_templates.py)")

    skill_text = SKILL_MD.read_text(encoding="utf-8") if SKILL_MD.exists() else ""
    if "assets/templates/" not in skill_text:
        error(f"{rel(SKILL_MD)}: does not reference the bundled templates path")


# ------------------------------------------------------------------------------------------- links


LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
HTML_RE = re.compile(r'(?:href|src)="([^"]+)"')


def check_links() -> None:
    checked = 0
    for path in markdown_files():
        text = strip_code_fences(path.read_text(encoding="utf-8"))
        targets = LINK_RE.findall(text) + HTML_RE.findall(text)
        for target in targets:
            if target.startswith(("http://", "https://", "mailto:", "#", "tel:")):
                continue
            clean = target.split("#", 1)[0].split("?", 1)[0].strip()
            if not clean:
                continue
            resolved = (path.parent / clean).resolve()
            if ROOT not in resolved.parents and resolved != ROOT:
                # Links like ../../issues/new/choose are resolved by the Git host, not on disk.
                continue
            checked += 1
            if not resolved.exists():
                error(f"{rel(path)}: broken link '{target}'")
    if checked == 0:
        warn("no relative links were found to check")


# ------------------------------------------------------------------------------- version phrasing


# Patterns that are wrong when stated as guidance. They are legitimate when the line is clearly
# negating them or documenting the rule itself (see CONTEXT_TOKEN_RE), e.g. "no v17+ support is
# claimed" or the changelog entry describing this fix.
SUSPECT_PATTERNS = [
    (
        re.compile(r"\bv1[0-9]+\+"),
        "version range like 'v15+' implies unsupported future versions",
    ),
    (
        re.compile(r"(?i)\bassume\s+frappe\s+v\d"),
        "instructs assuming a version instead of detecting it",
    ),
    (re.compile(r"\bv1[47-9]\b"), "version outside the supported range"),
    (re.compile(r"(?i)\bsupports?\s+v1[0-9]\b"), "support claim for a specific major version"),
]

# A line containing one of these is negating or explaining the claim, not making it.
CONTEXT_TOKEN_RE = re.compile(
    r"\b(?:not|no|never|earlier|unsupported|forbid|forbidden|banned|ban|beyond|upstream|"
    r"previously)\b"
    r"|out of scope|phras|range|deprecat|remov|convert",
    re.IGNORECASE,
)


def check_version_phrasing() -> None:
    for path in markdown_files():
        if any(exempt in path.parents for exempt in PHRASING_EXEMPT_DIRS):
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if CONTEXT_TOKEN_RE.search(line):
                continue
            for pattern, reason in SUSPECT_PATTERNS:
                match = pattern.search(line)
                if match:
                    error(
                        f"{rel(path)}:{lineno}: {reason} ('{match.group(0)}') -> "
                        f"{line.strip()[:110]}"
                    )


# ------------------------------------------------------------------------------------------ secrets


SECRET_PATTERNS = [
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key block"),
    (re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"), "GitHub personal access token"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key id"),
    (re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"), "API secret key"),
    (
        re.compile(
            r"(?i)\b(api[_-]?key|api[_-]?secret|secret[_-]?key|access[_-]?token|auth[_-]?token|"
            r"password|passwd)\b\s*[:=]\s*[\"'][^\"'\s]{6,}[\"']"
        ),
        "hardcoded credential-like value",
    ),
    (re.compile(r"(?i)\b(?:DB|DATABASE)_PASSWORD\s*[:=]\s*\S+"), "hardcoded database password"),
]


def check_secrets() -> None:
    skip_suffixes = {".png", ".ico", ".jpg", ".jpeg", ".gif", ".pdf", ".zip"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() in skip_suffixes:
            continue
        if path.name in {"validate_repo.py"}:
            continue  # this file contains the patterns themselves
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            for pattern, reason in SECRET_PATTERNS:
                if pattern.search(line):
                    error(f"{rel(path)}:{lineno}: possible secret ({reason})")


# ---------------------------------------------------------------------------------- local paths


LOCAL_PATH_PATTERNS = [
    (re.compile(r"/home/[a-z0-9._-]+/"), "absolute Linux home path"),
    (re.compile(r"/Users/[A-Za-z0-9._-]+/"), "absolute macOS home path"),
    (re.compile(r"[A-Za-z]:\\\\?Users\\\\"), "absolute Windows path"),
]


def check_local_paths() -> None:
    for path in markdown_files():
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            for pattern, reason in LOCAL_PATH_PATTERNS:
                if pattern.search(line):
                    warn(f"{rel(path)}:{lineno}: {reason} leaked into documentation")


# --------------------------------------------------------------------------------- inherited branding


def check_branding() -> None:
    """Fail when inherited branding survives in a shipped file.

    This is intentionally limited to the historical organisation slug, the old product slug, and the
    inherited author credit. It cannot judge whether prose still "sounds" like another product.
    """
    suffixes = {".md", ".json", ".py", ".yml", ".yaml", ".toml", ".txt"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if path.name in BRANDING_EXEMPT_NAMES:
            continue
        if any(exempt in path.parents for exempt in BRANDING_EXEMPT_DIRS):
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(lines, start=1):
            if BRANDING_CONTEXT_RE.search(line):
                continue
            for pattern, reason in INHERITED_BRANDING:
                match = pattern.search(line)
                if match:
                    error(
                        f"{rel(path)}:{lineno}: inherited branding ({reason}): "
                        f"'{match.group(0)}'"
                    )


# ------------------------------------------------------------------------------ white-label coverage


def check_white_labeling() -> None:
    """Presence check for the surfaces the engagement brief requires the guide to cover.

    This cannot judge correctness of the guidance, only that a surface has not silently disappeared.
    Section rewording that drops a keyword will fail the build; that is intentional, so the change is
    visible in review rather than shipped unnoticed.
    """
    guide = REFERENCES / "white-labeling.md"
    if not guide.exists():
        return  # check_references already reports the missing file

    text = guide.read_text(encoding="utf-8")
    for label, patterns in WHITE_LABEL_SURFACES:
        missing = [p for p in patterns if not re.search(p, text, re.IGNORECASE)]
        if missing:
            error(
                f"{rel(guide)}: required white-labeling coverage missing for '{label}' "
                f"(no match for {', '.join(missing)})"
            )


# ------------------------------------------------------------------------------- required artifacts


REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "SECURITY.md",
    ".github/workflows/validate.yml",
    ".github/pull_request_template.md",
    "docs/audit/repository-audit.md",
    "docs/audit/requirements-traceability.md",
    "docs/audit/implementation-roadmap.md",
    "docs/audit/phase-2-baseline.md",
    "docs/audit/phase-2-technical-findings.md",
    "docs/audit/phase-2-compatibility-matrix.md",
    "docs/audit/phase-2-agent-evaluation.md",
    "docs/audit/phase-2-final-report.md",
    "docs/templates/README.md",
    "templates/CLAUDE.md",
    "templates/AGENTS.md",
    "scripts/sync_templates.py",
    "scripts/tests/test_validate_repo.py",
]


def check_required_files() -> None:
    for name in REQUIRED_FILES:
        if not (ROOT / name).exists():
            error(f"missing required file: {name}")


def main() -> int:
    check_manifests()
    check_skill()
    check_references()
    check_templates()
    check_white_labeling()
    check_branding()
    check_links()
    check_version_phrasing()
    check_secrets()
    check_local_paths()
    check_required_files()

    print(f"markdown files scanned: {len(markdown_files())}")
    print(f"references: {len(list(REFERENCES.glob('*.md'))) if REFERENCES.is_dir() else 0}")
    print(f"templates: {len([p for p in TEMPLATES.glob('*.md') if p.name != 'README.md']) if TEMPLATES.is_dir() else 0}")

    for message in warnings:
        print(f"WARN  {message}")
    for message in errors:
        print(f"ERROR {message}")

    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
