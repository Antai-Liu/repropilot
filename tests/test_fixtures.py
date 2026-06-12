"""Verify score distribution against real fixture repositories."""

from pathlib import Path

from repropilot.checker import scan_repo
from repropilot.checker.scoring import compute_score

_FIXTURES = Path(__file__).parent / "fixtures"


def _score(repo_name: str) -> int:
    return compute_score(scan_repo(_FIXTURES / repo_name))["score"]


def test_bad_repo_score_below_40():
    assert _score("bad_repo") < 40


def test_medium_repo_score_between_40_and_75():
    score = _score("medium_repo")
    assert 40 <= score <= 75, f"Expected medium score in [40, 75], got {score}"


def test_good_repo_score_above_75():
    assert _score("good_repo") > 75
