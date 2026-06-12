"""Write a dict of {relative-path: content} to disk under a root directory."""

from __future__ import annotations

from pathlib import Path


def write_project(dest: Path, templates: dict[str, str]) -> None:
    for rel_path, content in templates.items():
        target = dest / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
