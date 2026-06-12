"""Tests for compute_score — bad / medium / good scan results."""

from repropilot.checker.scoring import compute_score

_ALL_KEYS = ["readme", "dependency_file", "configs", "src_dir", "tests_dir", "outputs_dir"]

BAD = {k: False for k in _ALL_KEYS}
MEDIUM = {**BAD, "readme": True, "dependency_file": True}
GOOD = {k: True for k in _ALL_KEYS}


class TestScoreDistribution:
    def test_bad_below_40(self):
        assert compute_score(BAD)["score"] < 40

    def test_medium_between_40_and_75(self):
        score = compute_score(MEDIUM)["score"]
        assert 40 <= score <= 75, f"Expected medium score in [40,75], got {score}"

    def test_good_above_75(self):
        assert compute_score(GOOD)["score"] > 75


class TestReturnShape:
    def test_keys_present(self):
        result = compute_score(BAD)
        assert set(result) == {"score", "passed", "failed", "not_assessed", "mode"}

    def test_score_is_int(self):
        assert isinstance(compute_score(GOOD)["score"], int)

    def test_mode_static_by_default(self):
        assert compute_score(BAD)["mode"] == "static"

    def test_mode_full_when_smoke(self):
        assert compute_score(BAD, run_smoke_test=True)["mode"] == "full"


class TestPassedFailed:
    def test_good_has_no_failed(self):
        result = compute_score(GOOD)
        assert result["failed"] == []

    def test_bad_has_no_passed(self):
        result = compute_score(BAD)
        assert result["passed"] == []

    def test_medium_has_both(self):
        result = compute_score(MEDIUM)
        assert len(result["passed"]) > 0
        assert len(result["failed"]) > 0


class TestNotAssessed:
    def test_not_assessed_is_list(self):
        result = compute_score(BAD)
        assert isinstance(result["not_assessed"], list)

    def test_not_assessed_empty_in_smoke_mode(self):
        result = compute_score(GOOD, run_smoke_test=True)
        assert result["not_assessed"] == []


class TestEdgeCases:
    def test_score_bounded_0_to_100(self):
        for sr in (BAD, MEDIUM, GOOD):
            s = compute_score(sr)["score"]
            assert 0 <= s <= 100

    def test_partial_scan_result(self):
        """Missing keys in scan_result should default to False without raising."""
        result = compute_score({})
        assert result["score"] == 0
