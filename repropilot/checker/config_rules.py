"""Config rules: experiment configuration files."""

from .rules import CheckableRule, EvidenceLevel

CONFIG_RULES: list[CheckableRule] = [
    CheckableRule(
        id="R_CF_001",
        category="config",
        weight=2.0,
        evidence_level=EvidenceLevel.static,
        checklist_refs=["CF-1"],
        fix="Add a configs/ directory or at least one YAML/JSON configuration file.",
        description="Repository must expose experiment hyperparameters via config files.",
        check=lambda s: bool(s.get("configs")),
    ),
]
