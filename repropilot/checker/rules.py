"""Pydantic models for reproducibility scoring rules."""

from __future__ import annotations

from enum import Enum
from typing import Callable, List

from pydantic import BaseModel, ConfigDict, Field


class EvidenceLevel(str, Enum):
    static = "static"
    semantic = "semantic"
    runnable = "runnable"
    declared = "declared"


class Rule(BaseModel):
    id: str = Field(..., description="Unique rule identifier, e.g. 'R001'")
    category: str = Field(..., description="Rule category, e.g. 'documentation'")
    weight: float = Field(..., ge=0.0, description="Relative scoring weight (≥ 0)")
    evidence_level: EvidenceLevel = Field(
        ..., description="Type of evidence: static | semantic | runnable | declared"
    )
    checklist_refs: List[str] = Field(
        ..., description="References to checklist items this rule covers"
    )
    fix: str = Field(..., description="Suggested remediation for a failing rule")
    description: str = Field(..., description="Human-readable description of the rule")


class CheckableRule(Rule):
    """Rule subclass that carries a check callable for scoring."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    check: Callable[[dict], bool] = Field(
        ..., exclude=True, description="Predicate applied to scan_result dict"
    )
