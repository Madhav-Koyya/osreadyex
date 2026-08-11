"""
checks/test_checks.py
------------------------
Checks that look for *evidence* that the project has tests at all.
This does not run the tests or check coverage percentage — that's a
much bigger job, and a great "complex" backlog issue (it would need a
new dependency to parse coverage output). v1 just asks "does anything
that looks like a test exist?"
"""

import os

from osready.models import CheckResult

# Any of these being present is enough to pass the check.
TEST_SIGNALS = [
    "tests",  # a tests/ folder
    "test",  # a test/ folder (some projects use singular)
    "pytest.ini",
    "conftest.py",
]


def check_tests_exist(repo_path: str) -> CheckResult:
    """
    Looks in the top level of the repo for any of the folder/file
    names in TEST_SIGNALS, or any *_test.py / test_*.py file.
    """
    top_level_entries = os.listdir(repo_path)

    for signal in TEST_SIGNALS:
        if signal in top_level_entries:
            return CheckResult(
                name="Tests present",
                passed=True,
                message=f"Found {signal}.",
                severity="low",
            )

    for entry in top_level_entries:
        if entry.startswith("test_") or entry.endswith("_test.py"):
            return CheckResult(
                name="Tests present",
                passed=True,
                message=f"Found test file: {entry}.",
                severity="low",
            )

    return CheckResult(
        name="Tests present",
        passed=False,
        message=(
            "No tests folder or test files found. Even one small test "
            "shows a maintainer you're testing your changes."
        ),
        severity="low",
    )


CHECKS = [
    check_tests_exist,
]
