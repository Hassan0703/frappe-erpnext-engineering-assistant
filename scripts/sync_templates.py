#!/usr/bin/env python3
"""Mirror the canonical templates into the skill bundle.

The repository's canonical templates live in ``docs/templates/``. A Claude Code plugin is installed
from ``plugins/frappe-erpnext-engineering-assistant/``, so anything outside that directory is unavailable at
runtime. This script copies the canonical templates into
``plugins/frappe-erpnext-engineering-assistant/skills/frappe-erpnext-engineering-assistant/assets/templates/`` so the skill can
reference them when installed.

Usage:
    python3 scripts/sync_templates.py           # write the bundled copies
    python3 scripts/sync_templates.py --check   # verify they match (exit 1 if not)
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "docs" / "templates"
TARGET = (
    ROOT
    / "plugins"
    / "frappe-erpnext-engineering-assistant"
    / "skills"
    / "frappe-erpnext-engineering-assistant"
    / "assets"
    / "templates"
)
INDEX = "README.md"


def template_files() -> list[Path]:
    if not SOURCE.is_dir():
        raise SystemExit(f"error: template source directory not found: {SOURCE}")
    return sorted(p for p in SOURCE.glob("*.md") if p.name != INDEX)


def main(argv: list[str]) -> int:
    check = "--check" in argv
    files = template_files()
    if not files:
        raise SystemExit(f"error: no templates found in {SOURCE}")

    if check:
        missing = []
        stale = []
        for src in files:
            dst = TARGET / src.name
            if not dst.exists():
                missing.append(src.name)
            elif dst.read_bytes() != src.read_bytes():
                stale.append(src.name)
        extras = sorted(
            p.name for p in TARGET.glob("*.md") if p.name not in {f.name for f in files}
        ) if TARGET.is_dir() else []
        if missing or stale or extras:
            for name in missing:
                print(f"missing in bundle: {name}")
            for name in stale:
                print(f"out of date in bundle: {name}")
            for name in extras:
                print(f"stale file in bundle (no source): {name}")
            print("run: python3 scripts/sync_templates.py")
            return 1
        print(f"bundled templates up to date ({len(files)} files)")
        return 0

    TARGET.mkdir(parents=True, exist_ok=True)
    for src in files:
        shutil.copyfile(src, TARGET / src.name)
    # Remove bundle files whose source was deleted.
    valid = {p.name for p in files}
    for existing in TARGET.glob("*.md"):
        if existing.name not in valid:
            existing.unlink()
            print(f"removed {existing.name}")
    print(f"synced {len(files)} templates -> {TARGET.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
