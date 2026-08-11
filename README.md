# OpenSourceReady (`osready`)

A command-line tool that checks whether your repository is ready for
your first open-source pull request — and tells you exactly what to
fix if it isn't.

```
$ osready check .

OpenSourceReady report
========================================
[FAIL] Git identity configured (high)
       -> Missing Git config: user.name, user.email. Fix with: ...
[PASS] README present (medium)
[PASS] No hardcoded secrets (high)
[FAIL] Tests present (low)
       -> No tests folder or test files found. ...
========================================
Readiness score: 7/10
```

## Install

```
git clone <this-repo-url>
cd osready
pip install -e .
```

## Usage

```
osready check .      # run all checks against the current folder
osready fix .         # auto-generate simple missing files (CONTRIBUTING.md)
```

## How it's organized

```
osready/
  models.py            # the CheckResult shape every check returns
  checks/
    git_checks.py       # Git config/state checks
    doc_checks.py        # README/LICENSE/CONTRIBUTING checks
    security_checks.py   # hardcoded-secret scanning
    test_checks.py       # "do tests exist" checks
    __init__.py           # the registry — collects all categories
  reports/
    scorer.py             # turns results into a score out of 10
    terminal_report.py    # prints the report
  fixes/
    fix_contributing.py   # auto-generates missing files
  cli.py                   # wires it all together
```

Every check is a small, independent function with the same contract:
it takes a repo path and returns one `CheckResult`. That's what makes
this a good project to practice contributing to — see
[CONTRIBUTING.md](CONTRIBUTING.md) and [ISSUES.md](ISSUES.md) for how
to add your own.

## Why only one check per category?

This is v1, and it's meant to be a starting skeleton, not a finished
tool. Every category has exactly one check implemented so there's
real, obvious room for the next contributor — that's the whole point
of this being a club project. See `ISSUES.md` for the backlog.
