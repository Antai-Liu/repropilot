"""Workflow rules: testing infrastructure."""

from .rules import CheckableRule, EvidenceLevel

WORKFLOW_RULES: list[CheckableRule] = [
    CheckableRule(
        id="R_WF_001",
        category="workflow",
        weight=2.0,
        evidence_level=EvidenceLevel.static,
        checklist_refs=["WF-1"],
        fix="Add a tests/ directory with at least smoke tests for the training pipeline.",
        description="Repository must have a tests/ directory.",
        check=lambda s: bool(s.get("tests_dir")),
    ),
]
