"""Reproducibility scoring engine.

Default mode accounts only for static + semantic evidence.
Report always marks runnable evidence as 'not assessed' unless
--run-smoke-test is explicitly enabled.
"""

from __future__ import annotations

from .config_rules import CONFIG_RULES
from .data_rules import DATA_RULES
from .onboarding_rules import ONBOARDING_RULES
from .results_rules import RESULTS_RULES
from .rules import CheckableRule
from .workflow_rules import WORKFLOW_RULES

_ALL_RULES: list[CheckableRule] = (
    ONBOARDING_RULES + DATA_RULES + CONFIG_RULES + WORKFLOW_RULES + RESULTS_RULES
)

_DEFAULT_LEVELS = {"static", "semantic"}
_FULL_LEVELS = {"static", "semantic", "runnable"}


def compute_score(
    scan_result: dict,
    run_smoke_test: bool = False,
) -> dict:
    """Score a repository against all registered rules.

    Parameters
    ----------
    scan_result:
        Dict produced by ``scan_repo()`` (keys → bool).
    run_smoke_test:
        When True, runnable-evidence rules are included in scoring.
        Defaults to False per project safety policy.

    Returns
    -------
    dict with keys:
        score        – int 0-100
        passed       – list of passing CheckableRule objects
        failed       – list of failing CheckableRule objects
        not_assessed – runnable rules skipped because smoke test is off
        mode         – "static" | "full"
    """
    active_levels = _FULL_LEVELS if run_smoke_test else _DEFAULT_LEVELS

    active: list[CheckableRule] = []
    not_assessed: list[CheckableRule] = []

    for rule in _ALL_RULES:
        level = rule.evidence_level.value
        if level in active_levels:
            active.append(rule)
        elif level == "runnable" and not run_smoke_test:
            not_assessed.append(rule)

    passed: list[CheckableRule] = []
    failed: list[CheckableRule] = []

    for rule in active:
        (passed if rule.check(scan_result) else failed).append(rule)

    total_weight = sum(r.weight for r in active)
    passed_weight = sum(r.weight for r in passed)
    score = round(passed_weight / total_weight * 100) if total_weight > 0 else 0

    return {
        "score": score,
        "passed": passed,
        "failed": failed,
        "not_assessed": not_assessed,
        "mode": "full" if run_smoke_test else "static",
    }
