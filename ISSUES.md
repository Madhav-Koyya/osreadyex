# Issue backlog

This is the master list to copy from when creating GitHub issues.
Each one below is written the way you'd paste it into an issue body.

---

## good-first-issue

### 1. Add a "not on main branch" check
**File:** `osready/checks/git_checks.py`
Add `check_not_on_main_branch`. Use `git rev-parse --abbrev-ref HEAD`
to get the current branch name; fail if it's `main` or `master`.
Severity: `medium`.

### 2. Add a "remote origin configured" check
**File:** `osready/checks/git_checks.py`
Add `check_remote_origin_exists`. Use `git remote -v`; fail if it
prints nothing. Severity: `medium`.

### 3. Add a "no uncommitted changes" check
**File:** `osready/checks/git_checks.py`
Add `check_no_uncommitted_changes`. Use `git status --porcelain`; if
it prints anything, the working tree is dirty. Severity: `low`.

### 4. Add a LICENSE file check
**File:** `osready/checks/doc_checks.py`
Copy `check_readme_exists` and adapt it to look for `LICENSE`,
`LICENSE.md`, or `LICENSE.txt`. Severity: `medium`.

### 5. Add a CONTRIBUTING.md file check
**File:** `osready/checks/doc_checks.py`
Same pattern as #4, but for `CONTRIBUTING.md`. Severity: `low`.

### 6. Add a pytest.ini / pyproject.toml `[tool.pytest]` check
**File:** `osready/checks/test_checks.py`
Extend `TEST_SIGNALS` handling to also recognize a `[tool.pytest.ini_options]`
section inside `pyproject.toml`, not just a standalone `pytest.ini`.

### 7. Write a test for `check_readme_exists`
**File:** `tests/test_doc_checks.py` (new file)
Follow the pattern in `tests/test_git_checks.py`: use `tmp_path`,
create a repo folder with and without a README, assert on the result.

---

## intermediate

### 8. Add a private-key-header secret pattern
**File:** `osready/checks/security_checks.py`
Add a regex to `SECRET_PATTERNS` that matches
`-----BEGIN PRIVATE KEY-----` (and RSA/OpenSSH variants). Think about
why this pattern shouldn't have false positives the way the generic
`api_key = ...` pattern might, and add a short comment explaining it.

### 9. Add a `--json` output mode
**Files:** `osready/cli.py`, `osready/reports/`
Add a `--json` flag to the `check` command. When set, print the
results as JSON instead of the human-readable report (add a new
function in `reports/`, e.g. `json_report.py`, following the same
"only this file calls print()" pattern as `terminal_report.py`).

### 10. Make severity weights configurable
**File:** `osready/reports/scorer.py`
Currently `SEVERITY_WEIGHTS` is hardcoded. Let a project optionally
provide an `.osready.toml` config file that overrides these weights.
Needs a small design write-up in the issue discussion before starting.

### 11. Add a LICENSE auto-fix
**File:** `osready/fixes/` (new file, follow `fix_contributing.py`)
Add `fix_missing_license` that writes an MIT license template if
`LICENSE` doesn't exist. Wire it into `cli.py`'s `fix` command.

### 12. Add a "TODO/FIXME density" check
**File:** `osready/checks/` (new category file: `code_quality_checks.py`)
This is your first chance to add a whole new *category*, not just a
new check inside one. You'll need to register it in
`osready/checks/__init__.py`'s `ALL_CHECKS` dict — that's the only
place you need to touch outside your new file.

---

## complex

### 13. GitHub API integration: check PR template exists on GitHub, not just locally
**Files:** new `osready/checks/github_checks.py`, plus a new dependency
Use the GitHub REST API (via `requests`) to check things a local file
scan can't, e.g. whether branch protection is enabled on the repo.
Needs a GitHub token input design (env var, most likely) — discuss the
approach in the issue before writing code.

### 14. Wire `osready check` into a pre-push Git hook
**Files:** new `osready/hooks/` folder, or a `osready install-hook` CLI command
Generate a `.git/hooks/pre-push` script that runs `osready check .`
and blocks the push on a non-zero exit code. Needs to handle: what if
`osready` isn't on PATH inside the hook's environment?

### 15. Auto-discovery of checks (registry via `import.meta.glob`-style scanning)
**File:** `osready/checks/__init__.py`
Right now, adding a new *category* means adding one line to
`ALL_CHECKS` by hand. Replace this with automatic discovery: scan the
`checks/` folder for any file exposing a `CHECKS` list and register it
without anyone editing `__init__.py`. This is the same idea DoxDock
uses for auto-discovering its tools — worth reading how it does it for
inspiration, but the Python approach will look different (probably
`importlib` + `pkgutil`, not a bundler-time glob).

### 16. CI pipeline that runs `osready check` on every PR to this repo
**Files:** `.github/workflows/ci.yml`
Set up GitHub Actions to install the package and run `osready check .`
plus `pytest` on every pull request, so the club's own repo eats its
own dog food.
