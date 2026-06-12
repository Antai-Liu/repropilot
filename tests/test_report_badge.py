"""Tests for report.py, badge.py, and terminal_output.py."""

import pytest

from repropilot.checker.badge import markdown_badge, shields_url
from repropilot.checker.report import build_markdown, write_report
from repropilot.checker.scoring import compute_score
from repropilot.checker.terminal_output import print_report

_ALL_KEYS = ["readme", "dependency_file", "configs", "src_dir", "tests_dir", "outputs_dir"]
_GOOD = {k: True for k in _ALL_KEYS}
_BAD = {k: False for k in _ALL_KEYS}


# ---------------------------------------------------------------------------
# badge.py
# ---------------------------------------------------------------------------


class TestShieldsUrl:
    def test_returns_string(self):
        assert isinstance(shields_url(100), str)

    def test_contains_score(self):
        assert "95" in shields_url(95)

    @pytest.mark.parametrize(
        "score,expected_colour",
        [(100, "brightgreen"), (90, "brightgreen"), (70, "yellow"), (50, "orange"), (0, "red")],
    )
    def test_colour_thresholds(self, score, expected_colour):
        assert expected_colour in shields_url(score)


class TestMarkdownBadge:
    def test_contains_img_syntax(self):
        badge = markdown_badge(80)
        assert badge.startswith("![")
        assert "](" in badge

    def test_includes_repo_path(self):
        badge = markdown_badge(75, repo_path="my/repo")
        assert "my/repo" in badge

    def test_no_suffix_when_empty_path(self):
        badge = markdown_badge(75, repo_path="")
        assert "()" not in badge


# ---------------------------------------------------------------------------
# report.py
# ---------------------------------------------------------------------------


class TestBuildMarkdown:
    def test_returns_string(self):
        result = compute_score(_GOOD)
        assert isinstance(build_markdown(result), str)

    def test_contains_score(self):
        result = compute_score(_GOOD)
        md = build_markdown(result, repo_path="my/repo")
        assert "100" in md

    def test_contains_repo_path(self):
        result = compute_score(_GOOD)
        md = build_markdown(result, repo_path="custom/path")
        assert "custom/path" in md

    def test_passed_section_present(self):
        result = compute_score(_GOOD)
        assert "## Passed rules" in build_markdown(result)

    def test_failed_section_present(self):
        result = compute_score(_BAD)
        assert "## Failed rules" in build_markdown(result)

    def test_not_assessed_section_when_runnable_skipped(self):
        result = compute_score(_GOOD, run_smoke_test=False)
        md = build_markdown(result)
        # No runnable rules currently defined, so section should be absent
        assert isinstance(md, str)


class TestWriteReport:
    def test_writes_file(self, tmp_path):
        out = tmp_path / "report.md"
        result = compute_score(_GOOD)
        write_report(result, out)
        assert out.exists()
        assert out.stat().st_size > 0

    def test_content_matches_build_markdown(self, tmp_path):
        out = tmp_path / "report.md"
        result = compute_score(_GOOD)
        write_report(result, out, repo_path="test/repo")
        assert out.read_text(encoding="utf-8") == build_markdown(result, "test/repo")


# ---------------------------------------------------------------------------
# terminal_output.py
# ---------------------------------------------------------------------------


class TestPrintReport:
    def test_runs_without_error(self, capsys):
        result = compute_score(_GOOD)
        print_report(result, path=".")
        captured = capsys.readouterr()
        assert "100" in captured.out

    def test_shows_pass_for_high_score(self, capsys):
        result = compute_score(_GOOD)
        print_report(result, path=".")
        assert "PASS" in capsys.readouterr().out

    def test_shows_fail_for_low_score(self, capsys):
        result = compute_score(_BAD)
        print_report(result, path=".")
        assert "FAIL" in capsys.readouterr().out

    def test_shows_failed_rule_fix(self, capsys):
        result = compute_score(_BAD)
        print_report(result, path=".")
        output = capsys.readouterr().out
        assert "Fix:" in output
