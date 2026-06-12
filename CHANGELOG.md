# Changelog

All notable changes to ReproPilot are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [0.1.0] — 2024-01-01

### Added

#### `repropilot check`
- Static reproducibility scorer: scans a repository and returns a
  **0 – 100** score based on six weighted rules (README, dependency file,
  configs, source directory, tests directory, outputs directory).
- Default mode uses only `static` and `semantic` evidence; `runnable`
  evidence is explicitly marked **not assessed** in the report.
- `--run-smoke-test` flag opts in to runnable-evidence rules.
- Exits with code 1 when score < 90 (CI-friendly).

#### `repropilot init`
- `--task fake-image-detection`: scaffolds a complete, CPU-runnable
  PyTorch project (15 files) that scores 100/100 out of the box.
- Generated project includes README, DATA.md, requirements.txt,
  configs/default.yaml, src/ package, tests/, outputs/, LICENSE, and
  a `.github/workflows/repropilot.yml` self-check workflow.

#### Scoring engine
- Six rule categories: `onboarding`, `data`, `config`, `workflow`,
  `results` — each with `id`, `category`, `weight`, `evidence_level`,
  `checklist_refs`, `fix`, and `description`.
- `EvidenceLevel` enum: `static | semantic | runnable | declared`.
- `compute_score(scan_result, run_smoke_test=False)` returns
  `score`, `passed`, `failed`, `not_assessed`, `mode`.

#### Outputs
- `terminal_output.print_report` — formatted terminal report.
- `report.build_markdown` / `write_report` — Markdown report file.
- `badge.shields_url` / `markdown_badge` — shields.io badge URLs.

#### CI / tooling integration
- `action.yml` — GitHub Actions composite action.
- `.pre-commit-hooks.yaml` — pre-commit hook (`repropilot-check`).
- `.github/workflows/ci.yml` — lint + test on every push/PR.

#### Documentation
- `docs/scoring.md` — full rule table, weight table, evidence levels,
  scoring formula, and benchmark thresholds.
- `README.md` — project overview, quickstart, score breakdown example,
  CI snippet, badge instructions, pre-commit setup, roadmap.
