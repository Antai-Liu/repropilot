"""Generate a reproducibility report as Markdown."""

from __future__ import annotations

from pathlib import Path


def build_markdown(result: dict, repo_path: str = ".") -> str:
    """Return a Markdown string summarising the scoring result."""
    score: int = result["score"]
    mode: str = result["mode"]
    passed = result["passed"]
    failed = result["failed"]
    not_assessed = result["not_assessed"]

    lines = [
        "# ReproPilot Reproducibility Report",
        "",
        f"**Repository:** `{repo_path}`  ",
        f"**Score:** {score}/100  ",
        f"**Mode:** {mode}  ",
        "",
        "## Passed rules",
        "",
    ]

    if passed:
        for rule in passed:
            lines.append(f"- ✓ `{rule.id}` {rule.description}")
    else:
        lines.append("_(none)_")

    lines += ["", "## Failed rules", ""]

    if failed:
        for rule in failed:
            lines.append(f"- ✗ `{rule.id}` {rule.description}")
            lines.append(f"  - **Fix:** {rule.fix}")
    else:
        lines.append("_(none)_")

    if not_assessed:
        lines += ["", "## Not assessed (runnable evidence)", ""]
        for rule in not_assessed:
            lines.append(f"- `{rule.id}` {rule.description}")
        lines.append("")
        lines.append("> runnable evidence: not assessed")

    return "\n".join(lines) + "\n"


def write_report(result: dict, output_path: Path, repo_path: str = ".") -> None:
    """Write a Markdown reproducibility report to *output_path*."""
    output_path.write_text(build_markdown(result, repo_path), encoding="utf-8")
