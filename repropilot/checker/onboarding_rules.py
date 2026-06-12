"""Onboarding rules: README and dependency declaration."""

from .rules import CheckableRule, EvidenceLevel

ONBOARDING_RULES: list[CheckableRule] = [
    CheckableRule(
        id="R_ON_001",
        category="onboarding",
        weight=3.0,
        evidence_level=EvidenceLevel.static,
        checklist_refs=["ON-1"],
        fix="Add a README.md (or .rst / .txt) describing the project and how to reproduce results.",
        description="Repository must have a top-level README file.",
        check=lambda s: bool(s.get("readme")),
    ),
    CheckableRule(
        id="R_ON_002",
        category="onboarding",
        weight=3.0,
        evidence_level=EvidenceLevel.static,
        checklist_refs=["ON-2"],
        fix="Add requirements.txt or pyproject.toml listing all dependencies.",
        description="Repository must declare its Python dependencies.",
        check=lambda s: bool(s.get("dependency_file")),
    ),
]
