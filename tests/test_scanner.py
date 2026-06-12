"""Tests for scan_repo — bad / medium / good fixture repos."""

import pytest

from repropilot.checker import scan_repo


@pytest.fixture()
def bad_repo(tmp_path):
    """Minimal repo: no standard artifacts."""
    (tmp_path / "train.py").write_text("pass")
    return tmp_path


@pytest.fixture()
def medium_repo(tmp_path):
    """Partial repo: has README and dependency file, no tests/outputs."""
    (tmp_path / "README.md").write_text("# Medium")
    (tmp_path / "requirements.txt").write_text("numpy")
    return tmp_path


@pytest.fixture()
def good_repo(tmp_path):
    """Complete repo: all expected artifacts present."""
    (tmp_path / "README.md").write_text("# Good")
    (tmp_path / "pyproject.toml").write_text("[project]\nname='good'")
    (tmp_path / "configs").mkdir()
    (tmp_path / "src").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "outputs").mkdir()
    return tmp_path


class TestBadRepo:
    def test_all_absent(self, bad_repo):
        result = scan_repo(bad_repo)
        assert result == {
            "readme": False,
            "dependency_file": False,
            "configs": False,
            "src_dir": False,
            "tests_dir": False,
            "outputs_dir": False,
        }


class TestMediumRepo:
    def test_readme_present(self, medium_repo):
        assert scan_repo(medium_repo)["readme"] is True

    def test_dependency_file_present(self, medium_repo):
        assert scan_repo(medium_repo)["dependency_file"] is True

    def test_tests_absent(self, medium_repo):
        assert scan_repo(medium_repo)["tests_dir"] is False

    def test_outputs_absent(self, medium_repo):
        assert scan_repo(medium_repo)["outputs_dir"] is False


class TestGoodRepo:
    def test_all_present(self, good_repo):
        result = scan_repo(good_repo)
        assert all(result.values()), f"Missing artifacts: {result}"


class TestScannerEdgeCases:
    def test_yaml_config_detected(self, tmp_path):
        (tmp_path / "config.yaml").write_text("key: value")
        assert scan_repo(tmp_path)["configs"] is True

    def test_json_config_detected(self, tmp_path):
        (tmp_path / "params.json").write_text("{}")
        assert scan_repo(tmp_path)["configs"] is True

    def test_pyproject_as_dependency_file(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[project]")
        assert scan_repo(tmp_path)["dependency_file"] is True
