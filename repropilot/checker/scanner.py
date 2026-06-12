"""Scan a target directory for reproducibility-relevant artifacts."""

from __future__ import annotations

import glob
from pathlib import Path


def scan_repo(root: str | Path) -> dict[str, bool]:
    """Return a presence map for key reproducibility artifacts under *root*."""
    root = Path(root)

    def exists_dir(name: str) -> bool:
        return (root / name).is_dir()

    def exists_file(*names: str) -> bool:
        return any((root / n).is_file() for n in names)

    def has_glob(pattern: str) -> bool:
        return bool(glob.glob(str(root / pattern)))

    readme_names = ["README.md", "README.rst", "README.txt", "README"]
    config_exts = ["*.yaml", "*.yml", "*.json"]

    has_config_dir = exists_dir("configs")
    has_config_file = any(has_glob(pat) for pat in config_exts)

    return {
        "readme": any(exists_file(n) for n in readme_names),
        "dependency_file": exists_file("requirements.txt", "pyproject.toml"),
        "configs": has_config_dir or has_config_file,
        "src_dir": exists_dir("src"),
        "tests_dir": exists_dir("tests"),
        "outputs_dir": exists_dir("outputs"),
    }
