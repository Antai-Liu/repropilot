"""Generate reproducibility score badges (shields.io)."""

from __future__ import annotations

_THRESHOLDS = [(90, "brightgreen"), (70, "yellow"), (50, "orange")]


def _colour(score: int) -> str:
    for threshold, colour in _THRESHOLDS:
        if score >= threshold:
            return colour
    return "red"


def shields_url(score: int) -> str:
    """Return a shields.io badge URL for *score*."""
    return (
        f"https://img.shields.io/badge/repropilot-{score}%2F100-{_colour(score)}"
    )


def markdown_badge(score: int, repo_path: str = "") -> str:
    """Return a Markdown image tag for the reproducibility badge."""
    url = shields_url(score)
    label = f"ReproPilot score: {score}/100"
    suffix = f" ({repo_path})" if repo_path else ""
    return f"![{label}{suffix}]({url})"
