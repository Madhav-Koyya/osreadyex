"""
checks/__init__.py
--------------------
This is the "registry" — the one place that knows all four check
categories exist. It's the same idea DoxDock uses for its PDF/image
tools: each category is its own self-contained module with a fixed
shape (a CHECKS list), and this file just collects them into one
dictionary. Nothing outside this file needs to know how many
categories exist or what's inside them.

If you add a brand-new CATEGORY (not just a new check inside an
existing one — that's simpler, see the other files) — say, a
"dependency_checks.py" — this is the only extra line you add to wire
it in. That's an "intermediate" issue, see ISSUES.md.
"""

from osready.checks import doc_checks
from osready.checks import git_checks
from osready.checks import security_checks
from osready.checks import test_checks

# Category name -> list of check functions in that category.
# The CLI and the scorer both loop over this dictionary; neither of
# them imports git_checks or doc_checks directly.
ALL_CHECKS = {
    "git": git_checks.CHECKS,
    "documentation": doc_checks.CHECKS,
    "security": security_checks.CHECKS,
    "testing": test_checks.CHECKS,
}


def run_all_checks(repo_path: str):
    """
    Runs every registered check against repo_path and returns a flat
    list of CheckResult objects. This is the single function the CLI
    calls — it doesn't need to know anything about categories.
    """
    results = []
    for category, check_functions in ALL_CHECKS.items():
        for check_function in check_functions:
            results.append(check_function(repo_path))
    return results
