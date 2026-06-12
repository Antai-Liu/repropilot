"""Data rules: source code structure as proxy for reproducible data handling."""

from .rules import CheckableRule, EvidenceLevel

DATA_RULES: list[CheckableRule] = [
    CheckableRule(
        id="R_DA_001",
        category="data",
        weight=2.0,
        evidence_level=EvidenceLevel.semantic,
        checklist_refs=["DA-1"],
        fix="Create a src/ directory containing data-loading and preprocessing modules.",
        description="A src/ directory suggests structured, importable data-processing code.",
        check=lambda s: bool(s.get("src_dir")),
    ),
]
