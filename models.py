"""
models.py
---------
This file defines ONE thing: what a "check result" looks like.

Every single check in this project — whether it's checking Git config,
looking for a README, or scanning for secrets — returns the exact same
shape of object. That's the whole trick that makes this codebase easy
to contribute to: once you understand CheckResult, you understand the
output of every check that exists now, and every check a future
student will ever add.

We use a @dataclass here instead of a plain class because a dataclass
auto-generates the boring stuff (the __init__ method, a nice __repr__
for printing) so we only have to list the fields we care about.
"""

from dataclasses import dataclass


@dataclass
class CheckResult:
    # A short, human-readable name for the check, e.g. "Git identity configured"
    name: str

    # Did the check pass? True or False. Nothing fancier than that.
    passed: bool

    # A one-line explanation shown to the student, e.g.
    # "No user.email set. Run: git config user.email you@example.com"
    message: str

    # How bad is it if this fails? One of: "high", "medium", "low"
    # This is used later by the scorer to decide how many points to
    # take off the readiness score.
    severity: str
