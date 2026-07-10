#!/usr/bin/env python3
"""Stamp a clean copy of the Data Science Toolbox into a new analysis folder.

Keeps the toolbox repo pristine (a template) while each real analysis lives in
its own self-contained workspace: edit notebooks there freely, point them at
real data, and nothing ever leaks back into the template or onto GitHub.

Usage:
    python new_project.py ~/work/q3-collections-model
    python new_project.py ../fraud-deep-dive --name "IEEE-CIS Fraud Deep Dive"
"""
import argparse
import shutil
import sys
from datetime import date
from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent

# What a fresh analysis workspace gets from the template:
COPY_GLOBS = ["*.ipynb", "utils.py", "score_batch.py", "requirements.txt",
              "PLAYBOOK.md", ".gitignore"]
SKIP_NAMES = {"new_project.py"}          # the stamper itself stays in the template


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("destination", help="folder to create for the new analysis")
    ap.add_argument("--name", help="human-readable project name (defaults to folder name)")
    ap.add_argument("--force", action="store_true",
                    help="copy into a non-empty destination (existing files are kept, "
                         "same-named files are overwritten)")
    args = ap.parse_args()

    dest = Path(args.destination).expanduser().resolve()
    name = args.name or dest.name

    if dest == TEMPLATE_DIR or TEMPLATE_DIR in dest.parents:
        print("ERROR: destination is inside the toolbox template folder — "
              "pick a path outside it so the template stays clean.")
        return 1
    if dest.exists() and any(dest.iterdir()) and not args.force:
        print(f"ERROR: {dest} already exists and is not empty (use --force to override).")
        return 1

    dest.mkdir(parents=True, exist_ok=True)
    (dest / "data").mkdir(exist_ok=True)
    (dest / "outputs").mkdir(exist_ok=True)

    copied = 0
    for pattern in COPY_GLOBS:
        for src in sorted(TEMPLATE_DIR.glob(pattern)):
            if src.name in SKIP_NAMES:
                continue
            shutil.copy2(src, dest / src.name)
            copied += 1

    (dest / "PROJECT_NOTES.md").write_text(f"""# {name}

- **Created:** {date.today().isoformat()} (from the Data Science Toolbox template)
- **Data source:** <where the data came from, extract date, row counts>
- **Question:** <what this analysis is trying to answer>
- **Target definition:** <exactly how the outcome column is defined>

## Decisions log
<!-- date: what you decided and why — future-you will thank present-you -->

## Findings
""")

    print(f"Created analysis workspace: {dest}")
    print(f"  {copied} template files copied | data/ and outputs/ ready | PROJECT_NOTES.md stub added")
    print()
    print("Next steps:")
    print(f"  1. cd {dest}")
    print("  2. Drop your data file into data/")
    print("  3. jupyter lab  ->  edit each notebook's INPUT cell freely — this copy is yours")
    print("  4. (optional) git init, if you want history for this analysis;")
    print("     the copied .gitignore already protects data/ and outputs/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
