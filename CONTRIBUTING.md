# Contributing to OpenSourceReady

This guide assumes you've never opened a pull request before. If you
have, skip to "Adding a new check."

## 1. Set up the project locally

```
git clone <your-fork-url>
cd osready
python -m venv venv
source venv/bin/activate          # on Windows: venv\Scripts\activate
pip install -e .
pip install pytest
```

Check it worked:

```
osready check .
```

You should see a report printed to your terminal.

## 2. Find an issue to work on

Look at the repo's Issues tab. Every issue is labeled:

- `good-first-issue` — small, self-contained, a great place to start
- `intermediate` — touches more than one file, or needs a small design decision
- `complex` — needs a new dependency, external API, or bigger design

Comment on the issue to say you're picking it up before you start.

## 3. Adding a new check (the most common contribution)

Every check follows the exact same shape. Open
`osready/checks/git_checks.py` and read `check_git_identity` — that's
your template.

1. Pick the right file for your check's category (`git_checks.py`,
   `doc_checks.py`, `security_checks.py`, or `test_checks.py`).
2. Write a function: `def check_something(repo_path: str) -> CheckResult:`
3. Return a `CheckResult` on both the pass and fail path.
4. Add your function to the `CHECKS` list at the bottom of the file.
5. Write a test in `tests/` — copy `tests/test_git_checks.py` as a
   starting point.

You do not need to touch `cli.py`, `scorer.py`, or the registry in
`checks/__init__.py` — they automatically pick up anything in a
`CHECKS` list.

## 4. Run the tests before opening a PR

```
python -m pytest tests/
osready check .
```

## 5. Open the pull request

- Keep it focused on one check or one fix — small PRs get reviewed faster.
- Describe what you added and why, in plain language.
- Link the issue you're closing (e.g. "Closes #12").

## Code style

- Every function needs a short docstring explaining *why*, not just *what*.
- No new dependencies without discussing it in the issue first.
