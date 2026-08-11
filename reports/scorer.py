"""
reports/scorer.py
-------------------
Turns a list of CheckResult objects into a single readiness score out
of 10.

The idea: every check "costs" points if it fails, and how many points
it costs depends on its severity. A failing high-severity check (like
a hardcoded secret) should hurt the score a lot more than a failing
low-severity one (like missing tests).
"""

# How many points a single failing check removes, by severity.
# These numbers are a starting point, not a law of physics — tuning
# them based on real workshop feedback is a good intermediate issue.
SEVERITY_WEIGHTS = {
    "high": 3,
    "medium": 2,
    "low": 1,
}

MAX_SCORE = 10


def calculate_score(results) -> float:
    """
    Starts at MAX_SCORE and subtracts weighted points for every
    failing check. Never goes below 0.
    """
    score = MAX_SCORE

    for result in results:
        if not result.passed:
            score -= SEVERITY_WEIGHTS.get(result.severity, 1)

    return max(score, 0)


def has_blocking_failure(results) -> bool:
    """
    Returns True if any high-severity check failed. The CLI uses this
    to decide its exit code, which is what makes it possible for
    someone to wire osready into a pre-push hook or CI pipeline later
    (a "complex" backlog issue) — a non-zero exit code is the standard
    way tools signal "something is wrong" to other tools.
    """
    return any(not r.passed and r.severity == "high" for r in results)
