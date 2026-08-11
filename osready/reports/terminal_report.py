"""
reports/terminal_report.py
-----------------------------
Turns a list of CheckResult objects (plus the score) into the printed
report a student sees in their terminal. This is the ONLY file that
should ever call print() — keeping all display logic in one place
means a future contributor can redesign the whole report (colors,
JSON output, whatever) without touching any check or the scorer.
"""

from osready.reports.scorer import calculate_score

PASS_ICON = "[PASS]"
FAIL_ICON = "[FAIL]"


def print_report(results):
    """
    Prints a simple, readable report:
      1. one line per check, grouped in the order checks ran
      2. the overall score out of 10
    """
    print("\nOpenSourceReady report")
    print("=" * 40)

    for result in results:
        icon = PASS_ICON if result.passed else FAIL_ICON
        print(f"{icon} {result.name} ({result.severity})")
        if not result.passed:
            print(f"       -> {result.message}")

    score = calculate_score(results)
    print("=" * 40)
    print(f"Readiness score: {score}/10\n")
