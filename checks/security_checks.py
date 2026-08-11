"""
checks/security_checks.py
---------------------------
A deliberately simple, teaching-scale secret scanner. This is NOT a
replacement for a real tool like gitleaks or truffleHog — it exists to
catch the single most common student mistake: accidentally committing
an API key or password.

Only one pattern family is implemented in v1 (AWS-style keys + generic
"api_key = ..." assignments). Adding more patterns (private key
headers, Slack tokens, generic passwords, etc.) is intentionally left
as a good-first-issue — see ISSUES.md.
"""

import os
import re

from osready.models import CheckResult

# Folders we never want to scan into — they're huge, not written by
# the student, and would make the check painfully slow.
SKIP_DIRS = {".git", "node_modules", "venv", ".venv", "__pycache__"}

# Each tuple is (human-readable label, compiled regex).
# Keep these conservative: a false positive is annoying, but a false
# negative in a workshop context is worse, so we lean a little broad.
SECRET_PATTERNS = [
    ("AWS Access Key", re.compile(r"AKIA[0-9A-Z]{16}")),
    (
        "Hardcoded API/secret key",
        re.compile(r"(?i)(api|secret)_?key\s*=\s*['\"][A-Za-z0-9_\-]{16,}['\"]"),
    ),
]


def check_hardcoded_secrets(repo_path: str) -> CheckResult:
    """
    Walks every text file in the repo (skipping the folders in
    SKIP_DIRS) and checks each line against SECRET_PATTERNS.
    Returns fail on the *first* match, since one leaked secret is
    already reason enough to stop and fix it before opening a PR.
    """
    for root, dirs, files in os.walk(repo_path):
        # Removing names from `dirs` in-place tells os.walk not to
        # descend into them at all.
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for filename in files:
            filepath = os.path.join(root, filename)
            match = _scan_file(filepath)
            if match:
                label, line_number = match
                return CheckResult(
                    name="No hardcoded secrets",
                    passed=False,
                    message=(
                        f"Possible {label} found in "
                        f"{os.path.relpath(filepath, repo_path)}:{line_number}. "
                        "Remove it and rotate the credential before committing."
                    ),
                    severity="high",
                )

    return CheckResult(
        name="No hardcoded secrets",
        passed=True,
        message="No obvious hardcoded secrets found.",
        severity="high",
    )


def _scan_file(filepath: str):
    """
    Reads a file line-by-line and checks it against every pattern in
    SECRET_PATTERNS. Returns (label, line_number) on the first hit,
    or None if nothing matched.

    We open with errors="ignore" because binary files (images, etc.)
    would otherwise crash this with a decoding error — we just want
    to skip over the parts we can't read as text.
    """
    try:
        with open(filepath, "r", errors="ignore") as f:
            for line_number, line in enumerate(f, start=1):
                for label, pattern in SECRET_PATTERNS:
                    if pattern.search(line):
                        return (label, line_number)
    except (IsADirectoryError, PermissionError):
        pass
    return None


CHECKS = [
    check_hardcoded_secrets,
]
