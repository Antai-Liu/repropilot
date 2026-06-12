"""Tests for repropilot init --task fake-image-detection."""

import pytest
from typer.testing import CliRunner

from repropilot.checker import scan_repo
from repropilot.checker.scoring import compute_score
from repropilot.cli import app

runner = CliRunner()

REQUIRED_FILES = [
    "README.md",
    "DATA.md",
    "requirements.txt",
    "LICENSE",
    "configs/default.yaml",
    "src/train.py",
    "src/eval.py",
    "src/utils.py",
    "src/model.py",
    "src/dataset.py",
    "tests/test_smoke.py",
    "outputs/.gitkeep",
]


@pytest.fixture(scope="module")
def generated_project(tmp_path_factory):
    """Generate one project for the whole module; pytest cleans up tmp dirs."""
    dest = tmp_path_factory.mktemp("fake_image") / "myproject"
    result = runner.invoke(
        app,
        ["init", str(dest), "--task", "fake-image-detection"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output
    return dest


class TestInitSuccess:
    def test_creates_directory(self, generated_project):
        assert generated_project.is_dir()

    def test_check_score_at_least_90(self, generated_project):
        score = compute_score(scan_repo(generated_project))["score"]
        assert score >= 90, f"Score {score} < 90"


class TestRequiredFiles:
    @pytest.mark.parametrize("rel_path", REQUIRED_FILES)
    def test_file_exists(self, generated_project, rel_path):
        assert (generated_project / rel_path).exists(), f"Missing: {rel_path}"


class TestErrorHandling:
    def test_fails_when_directory_already_exists(self, tmp_path):
        existing = tmp_path / "occupied"
        existing.mkdir()
        result = runner.invoke(
            app, ["init", str(existing), "--task", "fake-image-detection"]
        )
        assert result.exit_code != 0

    def test_fails_on_unknown_task(self, tmp_path):
        dest = tmp_path / "notcreated"
        result = runner.invoke(
            app, ["init", str(dest), "--task", "unknown-task"]
        )
        assert result.exit_code != 0
        assert not dest.exists()
