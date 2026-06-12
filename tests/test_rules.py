"""Tests for Rule model — bad / medium / good fixture rules."""

import pytest
from pydantic import ValidationError

from repropilot.checker import Rule, EvidenceLevel


GOOD_RULE_DATA = {
    "id": "R001",
    "category": "documentation",
    "weight": 1.0,
    "evidence_level": "static",
    "checklist_refs": ["ML-Repro-Checklist:1.1"],
    "fix": "Add a README.md describing how to reproduce results.",
    "description": "Repository must have a top-level README.",
}


class TestRuleValid:
    def test_all_evidence_levels_accepted(self):
        for level in ("static", "semantic", "runnable", "declared"):
            r = Rule(**{**GOOD_RULE_DATA, "evidence_level": level})
            assert r.evidence_level == EvidenceLevel(level)

    def test_field_values_stored(self):
        r = Rule(**GOOD_RULE_DATA)
        assert r.id == "R001"
        assert r.category == "documentation"
        assert r.weight == 1.0
        assert r.checklist_refs == ["ML-Repro-Checklist:1.1"]
        assert r.fix != ""
        assert r.description != ""


class TestRuleInvalid:
    def test_missing_id_raises(self):
        data = {k: v for k, v in GOOD_RULE_DATA.items() if k != "id"}
        with pytest.raises(ValidationError):
            Rule(**data)

    def test_negative_weight_raises(self):
        with pytest.raises(ValidationError):
            Rule(**{**GOOD_RULE_DATA, "weight": -1.0})

    def test_invalid_evidence_level_raises(self):
        with pytest.raises(ValidationError):
            Rule(**{**GOOD_RULE_DATA, "evidence_level": "hypothetical"})

    def test_missing_fix_raises(self):
        data = {k: v for k, v in GOOD_RULE_DATA.items() if k != "fix"}
        with pytest.raises(ValidationError):
            Rule(**data)

    def test_missing_checklist_refs_raises(self):
        data = {k: v for k, v in GOOD_RULE_DATA.items() if k != "checklist_refs"}
        with pytest.raises(ValidationError):
            Rule(**data)
