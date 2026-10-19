#!/usr/bin/env python3
"""Tests for ``scripts/validate_repo.py``.

The validator is the only automated gate on this repository, so it needs its own tests: a clean
baseline that passes, one failing case per check, and confirmation that the historical phrasing kept
in the audit documents stays exempt. Every case runs against a throwaway copy of the repository, so
the working copy is never modified.

Run with the standard library only::

    python3 -m unittest discover -s scripts/tests -p "test_*.py" -v
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
IGNORE = shutil.ignore_patterns(".git", "__pycache__", ".freebuff", "node_modules")

SKILL = "plugins/frappe-erpnext-engineering-assistant/skills/frappe-erpnext-engineering-assistant/SKILL.md"
REFERENCES = "plugins/frappe-erpnext-engineering-assistant/skills/frappe-erpnext-engineering-assistant/references"
GUIDE = f"{REFERENCES}/white-labeling.md"
BUNDLED = "plugins/frappe-erpnext-engineering-assistant/skills/frappe-erpnext-engineering-assistant/assets/templates"
MANIFEST = "plugins/frappe-erpnext-engineering-assistant/.claude-plugin/plugin.json"

# Built at runtime so this test file does not itself trip the secret or version-phrasing scans.
UNSUPPORTED_RANGE = "Assume Frappe " + "v15" + "+ unless the project says otherwise."
FAKE_TOKEN = "sk-" + "a" * 24

# Every white-labeling surface except PWA/mobile, so the coverage check can be shown to fire.
MINIMAL_GUIDE = (
    "# White-labeling\n\n"
    "desk login navbar workspace website portal app_title app_logo_url logo favicon assets "
    "email notification print pdf translation terminology multi-tenant upgrade `bench build` "
    "licensing trademark verification configuration-only custom-app hook fixture patch migration "
    "framework fork core modification\n"
)


class ValidatorTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="fcs-validate-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.root = self.tmp / "repo"
        shutil.copytree(REPO, self.root, ignore=IGNORE)

    def path(self, relative: str) -> Path:
        return self.root / relative

    def run_validator(self) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, "scripts/validate_repo.py"],
            cwd=self.root,
            capture_output=True,
            text=True,
        )

    def assert_passes(self) -> None:
        result = self.run_validator()
        self.assertEqual(
            result.returncode, 0, f"expected pass:\n{result.stdout}\n{result.stderr}"
        )

    def assert_fails(self, needle: str) -> None:
        result = self.run_validator()
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, 1, f"expected failure, got pass:\n{output}")
        self.assertIn(needle, output)

    def append(self, relative: str, text: str) -> None:
        target = self.path(relative)
        target.write_text(target.read_text(encoding="utf-8") + text, encoding="utf-8")

    def rewrite(self, relative: str, old: str, new: str) -> None:
        target = self.path(relative)
        target.write_text(target.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")


class BaselineTests(ValidatorTestCase):
    def test_clean_repository_passes(self) -> None:
        self.assert_passes()

    def test_audit_documents_may_quote_historical_phrasing(self) -> None:
        # The audit directory quotes the pre-fix claim as evidence and is exempt by design.
        self.append("docs/audit/repository-audit.md", "\nLegacy note: " + UNSUPPORTED_RANGE + "\n")
        self.assert_passes()

    def test_links_inside_code_fences_are_not_checked(self) -> None:
        self.append("README.md", "\n```\n[not a link](docs/also-missing.md)\n```\n")
        self.assert_passes()


class StructureTests(ValidatorTestCase):
    def test_unsupported_version_range_fails(self) -> None:
        self.append(f"{REFERENCES}/security.md", "\n" + UNSUPPORTED_RANGE + "\n")
        self.assert_fails("version range like")

    def test_broken_relative_link_fails(self) -> None:
        self.append("README.md", "\n[missing](docs/does-not-exist.md)\n")
        self.assert_fails("broken link")

    def test_orphaned_reference_fails(self) -> None:
        self.rewrite(SKILL, "`references/code-placement.md`", "`code-placement.md`")
        self.assert_fails("not linked from SKILL.md")

    def test_reference_missing_from_numbered_index_fails(self) -> None:
        target = self.path(SKILL)
        text = re.sub(r"^4\. `references/hooks-and-customization\.md`.*\n", "", target.read_text(), flags=re.M)
        target.write_text(text, encoding="utf-8")
        self.assert_fails("reference index does not list references/hooks-and-customization.md")

    def test_missing_required_reference_fails(self) -> None:
        self.path(f"{REFERENCES}/performance.md").unlink()
        self.assert_fails("required reference missing")

    def test_missing_template_fails(self) -> None:
        self.path("docs/templates/uat-signoff.md").unlink()
        self.assert_fails("required template missing")

    def test_bundled_template_drift_fails(self) -> None:
        self.append(f"{BUNDLED}/test-plan.md", "\nDrifted copy.\n")
        self.assert_fails("bundled template out of date")

    def test_template_missing_from_index_fails(self) -> None:
        self.rewrite("docs/templates/README.md", "[`test-plan.md`](test-plan.md)", "test-plan.md")
        self.assert_fails("is not listed in the index")

    def test_duplicate_template_index_entry_fails(self) -> None:
        self.append("docs/templates/README.md", "\n[`test-plan.md`](test-plan.md)\n")
        self.assert_fails("more than once")


class MetadataTests(ValidatorTestCase):
    def test_version_mismatch_between_manifest_and_changelog_fails(self) -> None:
        self.rewrite(MANIFEST, '"version": "2.0.0-beta.1"', '"version": "9.9.9"')
        self.assert_fails("version mismatch")

    def test_invalid_json_manifest_fails(self) -> None:
        self.path(".claude-plugin/marketplace.json").write_text('{"name": ', encoding="utf-8")
        self.assert_fails("invalid JSON")

    def test_plugin_missing_from_marketplace_fails(self) -> None:
        self.rewrite(".claude-plugin/marketplace.json", '"frappe-erpnext-engineering-assistant"', '"other-plugin"')
        self.assert_fails("does not declare the plugin")

    def test_manifest_missing_author_fails(self) -> None:
        self.rewrite(
            MANIFEST,
            '"author": {\n    "name": "Hassan0703",\n    "url": "https://github.com/Hassan0703"\n  },',
            '"author": {},',
        )
        self.assert_fails("missing author.name")


class SecurityTests(ValidatorTestCase):
    def test_secret_in_documentation_fails(self) -> None:
        self.append("CONTRIBUTING.md", "\napi_key = " + repr(FAKE_TOKEN) + "\n")
        self.assert_fails("possible secret")

    def test_private_key_block_fails(self) -> None:
        self.append("SECURITY.md", "\n-----BEGIN " + "RSA PRIVATE KEY-----\n")
        self.assert_fails("possible secret")


class WhiteLabelTests(ValidatorTestCase):
    def test_missing_white_label_surface_fails(self) -> None:
        self.path(GUIDE).write_text(MINIMAL_GUIDE, encoding="utf-8")
        self.assert_fails("required white-labeling coverage missing for 'PWA / mobile'")

    def test_present_white_label_surfaces_pass(self) -> None:
        self.path(GUIDE).write_text(
            MINIMAL_GUIDE + "pwa mobile\n", encoding="utf-8"
        )
        self.assert_passes()


class BrandingTests(ValidatorTestCase):
    """Inherited branding must not survive outside the licence, NOTICE, changelog and audit history."""

    def test_old_organisation_name_fails(self) -> None:
        self.append(f"{REFERENCES}/security.md", "\nContact " + "Next" + "ash for details.\n")
        self.assert_fails("inherited branding")

    def test_old_product_slug_fails(self) -> None:
        old_slug = "frappe-" + "code-standards"
        self.append("CONTRIBUTING.md", f"\nOld repository: Hassan0703/{old_slug}\n")
        self.assert_fails("inherited branding")

    def test_removal_instructions_may_name_the_old_plugin(self) -> None:
        old_slug = "frappe-" + "code-standards"
        old_marketplace = "next" + "ash"
        self.append(
            "CONTRIBUTING.md",
            f"\nUninstall {old_slug}@{old_marketplace} before installing this version.\n",
        )
        self.assert_passes()

    def test_licence_and_notice_may_keep_original_attribution(self) -> None:
        # The baseline already contains the original copyright line in LICENSE; it must stay exempt.
        self.assert_passes()


class RepositoryConsistencyTests(ValidatorTestCase):
    def test_ci_runs_validator_sync_and_validator_tests(self) -> None:
        workflow = self.path(".github/workflows/validate.yml").read_text(encoding="utf-8")
        self.assertIn("validate_repo.py", workflow)
        self.assertIn("sync_templates.py --check", workflow)
        self.assertIn("unittest discover", workflow)

    def test_skill_description_declares_scope_and_capabilities(self) -> None:
        text = self.path(SKILL).read_text(encoding="utf-8")
        frontmatter = text.split("---", 2)[1]
        description = next(
            line.split(":", 1)[1].strip()
            for line in frontmatter.splitlines()
            if line.startswith("description:")
        )
        for topic in ("v15", "v16", "white-label", "deploy", "migration", "test"):
            self.assertIn(topic, description)

    def test_changelog_documents_the_current_version(self) -> None:
        changelog = self.path("CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("## 2.0.0-beta.1", changelog)

    def test_skill_name_matches_new_product(self) -> None:
        text = self.path(SKILL).read_text(encoding="utf-8")
        self.assertIn("name: frappe-erpnext-engineering-assistant", text)


if __name__ == "__main__":
    unittest.main()
