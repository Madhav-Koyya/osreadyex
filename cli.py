"""
cli.py
-------
The command-line interface. This file's ONLY job is to:
  1. parse what the student typed (`osready check .` or `osready fix .`)
  2. call the right function from checks/, reports/, or fixes/
  3. exit with the right status code

It does NOT contain any check logic, scoring logic, or printing logic
itself — it just wires those three pieces together. This keeps it
short enough to read in one sitting even if you've never touched this
project before.
"""

import argparse
import sys

from osready.checks import run_all_checks
from osready.fixes.fix_contributing import fix_missing_contributing
from osready.reports.scorer import has_blocking_failure
from osready.reports.terminal_report import print_report


def main():
    parser = argparse.ArgumentParser(
        prog="osready",
        description="Check whether a repository is ready for a pull request.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser(
        "check", help="Run all readiness checks against a repository."
    )
    check_parser.add_argument(
        "path", nargs="?", default=".", help="Path to the repo (default: current folder)"
    )

    fix_parser = subparsers.add_parser(
        "fix", help="Auto-generate simple missing files (currently: CONTRIBUTING.md)."
    )
    fix_parser.add_argument(
        "path", nargs="?", default=".", help="Path to the repo (default: current folder)"
    )

    args = parser.parse_args()

    if args.command == "check":
        results = run_all_checks(args.path)
        print_report(results)
        # Non-zero exit code if a high-severity check failed. This is
        # what lets osready eventually be wired into a pre-push hook
        # or CI job — see ISSUES.md.
        sys.exit(1 if has_blocking_failure(results) else 0)

    elif args.command == "fix":
        message = fix_missing_contributing(args.path)
        print(message)
        sys.exit(0)


if __name__ == "__main__":
    main()
