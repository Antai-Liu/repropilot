# Contributing to ReproPilot

Thank you for considering a contribution!

## Development setup

```bash
git clone https://github.com/Antai-Liu/repropilot.git
cd repropilot
pip install -e ".[dev]"
```

## Running tests

```bash
pytest -q          # full test suite
ruff check .       # linter
```

All tests must pass and ruff must report zero errors before a PR is merged.

## Adding a scoring rule

1. Add a `CheckableRule` entry to the relevant category file in
   `repropilot/checker/` (e.g. `onboarding_rules.py`).
2. Every rule **must** include: `id`, `category`, `weight`,
   `evidence_level`, `checklist_refs`, `fix`, `description`, and a
   `check` callable.
3. Add fixture tests covering **bad / medium / good** repositories in
   `tests/` — see `tests/test_scoring.py` for the pattern.
4. Update `docs/scoring.md` to reflect the new rule and any weight changes.

## Submitting a pull request

1. Fork the repo and create a feature branch.
2. Make your changes; keep commits focused and atomic.
3. Run `pytest -q` and `ruff check .` locally — both must be clean.
4. **Every PR is self-checked with `repropilot check .`** as part of CI.
   The workflow in `.github/workflows/ci.yml` runs the check automatically.
5. Open a PR against `main` with a clear description of what changed and why.
6. A maintainer will review within a few days.

## Code style

- Python 3.10+, formatted and linted with `ruff` (`line-length = 100`).
- No comments explaining *what* the code does — only non-obvious *why*.
- No docstrings longer than one line.
- No features added beyond what the task requires.
