"""Format scoring results for terminal display."""

from __future__ import annotations

import typer

from .rules import CheckableRule


def print_report(result: dict, path: str = ".") -> None:
    """Print a human-readable scoring report to stdout.

    Marks runnable evidence as 'not assessed' per project policy.
    """
    score: int = result["score"]
    mode: str = result["mode"]
    passed: list[CheckableRule] = result["passed"]
    failed: list[CheckableRule] = result["failed"]
    not_assessed: list[CheckableRule] = result["not_assessed"]

    typer.echo(f"ReproPilot check  —  {path}")
    typer.echo(f"Score : {score}/100  [mode: {mode}]")
    typer.echo(f"Passed: {len(passed)} rule(s)")
    typer.echo(f"Failed: {len(failed)} rule(s)")

    if not_assessed:
        ids = ", ".join(r.id for r in not_assessed)
        typer.echo(f"runnable evidence: not assessed ({ids})")

    if failed:
        typer.echo("")
        for rule in failed:
            typer.echo(f"  [{rule.id}] {rule.description}")
            typer.echo(f"         Fix: {rule.fix}")

    typer.echo("")
    if score >= 90:
        typer.echo(f"PASS  score {score} >= 90")
    else:
        typer.echo(f"FAIL  score {score} < 90")
