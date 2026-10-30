#!/usr/bin/env python3
"""Output validator for agent-01 (deploy-incident triage).

Checks report.md for: required sections, required facts (the port pair),
verbatim evidence, and absence of fabricated specifics.

Usage: python verify_output.py
Exit codes: 0 = ACCEPT, 1 = REJECT.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.join(HERE, "workspace")
REPORT = os.path.join(HERE, "report.md")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def main():
    if not os.path.exists(REPORT):
        print("REJECT: report.md not found next to verify_output.py")
        return 1
    report = read(REPORT)

    # 1. required sections
    for section in ("## Root cause", "## Evidence", "## Recommended fix", "## Rollback condition"):
        if section not in report:
            print(f"REJECT: missing section '{section}'")
            return 1

    # 2. root cause states the port pair
    root = report.split("## Root cause", 1)[1].split("## Evidence", 1)[0]
    if "5433" not in root or "5432" not in root:
        print("REJECT: Root cause must state both ports (5433 configured vs 5432 actual)")
        return 1

    # 3. evidence block: every line must be a verbatim substring of a workspace file
    evidence = report.split("## Evidence", 1)[1].split("## Recommended fix", 1)[0]
    fence = re.search(r"```[^\n]*\n(.*?)```", evidence, re.S)
    if not fence:
        print("REJECT: Evidence section must contain a fenced code block")
        return 1
    sources = {name: read(os.path.join(WORKSPACE, name))
               for name in os.listdir(WORKSPACE)}
    lines = [ln.strip() for ln in fence.group(1).splitlines() if ln.strip()]
    if len(lines) < 2:
        print("REJECT: evidence block must quote at least 2 lines")
        return 1
    for ln in lines:
        if not any(ln in src for src in sources.values()):
            print(f"REJECT: evidence line not found verbatim in workspace: {ln[:70]}")
            return 1

    # 4. anti-fabrication: root cause must not borrow the unrelated warning
    if re.search(r"disk.{0,20}71%", root) or "worker-2" in root:
        print("REJECT: root cause incorrectly blames the unrelated disk warning")
        return 1

    # 5. rollback condition must be concrete (mention the working port)
    rollback = report.split("## Rollback condition", 1)[1]
    if "5432" not in rollback:
        print("REJECT: rollback/verification condition must reference the working port 5432")
        return 1

    print("ACCEPT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
