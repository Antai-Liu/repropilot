# ReproPilot Scoring

ReproPilot scores a repository on a **0 – 100** scale by evaluating
static and semantic evidence of reproducibility.

## Scoring formula

```
score = round(passed_weight / total_active_weight * 100)
```

Only rules whose `evidence_level` is **static** or **semantic** contribute
to the denominator in the default mode (no `--run-smoke-test`).

> **Report note:** `runnable evidence: not assessed` is always printed
> when the smoke-test flag is off, per project policy.

## Evidence levels

| Level    | Meaning                                          | Counted by default |
|----------|--------------------------------------------------|--------------------|
| static   | File / directory presence detectable by scanner  | ✓                  |
| semantic | Structural inference (e.g. src/ implies code)    | ✓                  |
| runnable | Requires actually executing code                 | only with `--run-smoke-test` |
| declared | Explicitly declared in a manifest                | ✓                  |

## Rules

| ID       | Category   | Weight | Evidence | What is checked                              |
|----------|------------|--------|----------|----------------------------------------------|
| R_ON_001 | onboarding | 3.0    | static   | README file present                          |
| R_ON_002 | onboarding | 3.0    | static   | requirements.txt or pyproject.toml present   |
| R_DA_001 | data       | 2.0    | semantic | src/ directory present                       |
| R_CF_001 | config     | 2.0    | static   | configs/ directory or YAML/JSON config file  |
| R_WF_001 | workflow   | 2.0    | static   | tests/ directory present                     |
| R_RS_001 | results    | 2.0    | static   | outputs/ directory present                   |

**Total active weight (default mode): 14.0**

### Score benchmarks

| Score | Interpretation          |
|-------|-------------------------|
| ≥ 90  | Highly reproducible     |
| 70–89 | Mostly reproducible     |
| 50–69 | Partially reproducible  |
| < 50  | Needs significant work  |

## Running

```bash
# Default (static + semantic only)
repropilot check /path/to/repo

# Include runnable evidence
repropilot check /path/to/repo --run-smoke-test
```

## Updating this file

Per project convention, update `docs/scoring.md` whenever any public
scoring behaviour changes (new rules, weight changes, new evidence
levels, changes to the scoring formula).
