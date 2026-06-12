"""Results rules: persisted outputs and artifacts."""

from .rules import CheckableRule, EvidenceLevel

RESULTS_RULES: list[CheckableRule] = [
    CheckableRule(
        id="R_RS_001",
        category="results",
        weight=2.0,
        evidence_level=EvidenceLevel.static,
        checklist_refs=["RS-1"],
        fix="Add an outputs/ directory to store model checkpoints, metrics, and figures.",
        description="Repository must have an outputs/ directory for reproducible artifacts.",
        check=lambda s: bool(s.get("outputs_dir")),
    ),
]
