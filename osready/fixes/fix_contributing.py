"""
fixes/fix_contributing.py
----------------------------
The `osready fix` command's first (and only, in v1) auto-fix: it
generates a starter CONTRIBUTING.md if one doesn't already exist.

This is the pattern to copy for future fixes (a LICENSE generator, a
README generator, etc. — all good-first-issues in ISSUES.md): write a
function that takes repo_path, checks whether it needs to do
anything, writes a file if so, and returns a short message describing
what it did.
"""

import os

TEMPLATE = """# Contributing

Thanks for considering a contribution to this project!

## Getting started
1. Fork this repository and clone your fork.
2. Create a branch for your change: `git checkout -b my-change`.
3. Make your change and commit it with a clear message.
4. Push your branch and open a pull request.

## Before you open a pull request
- Run `osready check .` and make sure your readiness score looks good.
- Keep pull requests small and focused on one thing.

## Questions
Open an issue if anything here is unclear — that's a contribution too.
"""


def fix_missing_contributing(repo_path: str) -> str:
    """
    If CONTRIBUTING.md doesn't exist at the top level of repo_path,
    write the template above into it. Returns a message describing
    what happened, which the CLI just prints.
    """
    target_path = os.path.join(repo_path, "CONTRIBUTING.md")

    if os.path.isfile(target_path):
        return "CONTRIBUTING.md already exists — nothing to fix."

    with open(target_path, "w") as f:
        f.write(TEMPLATE)

    return f"Created {target_path}."
