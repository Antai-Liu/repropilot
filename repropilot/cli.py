import typer

app = typer.Typer()


@app.command("init")
def init_command(
    project_name: str = typer.Argument(..., help="Name of the project to create"),
    task: str = typer.Option("fake-image-detection", "--task"),
) -> None:
    from pathlib import Path

    from repropilot.generator.fake_image_template import get_templates
    from repropilot.generator.project_writer import write_project

    if task != "fake-image-detection":
        typer.echo(
            f"Unknown task: {task!r}. Supported: fake-image-detection", err=True
        )
        raise typer.Exit(1)

    dest = Path(project_name)
    if dest.exists():
        typer.echo(f"Directory {dest!r} already exists.", err=True)
        raise typer.Exit(1)

    templates = get_templates(project_name)
    write_project(dest, templates)
    typer.echo(f"Created '{project_name}' ({len(templates)} files)")


@app.command()
def check(
    path: str = typer.Argument(".", help="Repository path to check"),
    run_smoke_test: bool = typer.Option(False, "--run-smoke-test"),
) -> None:
    from repropilot.checker import scan_repo
    from repropilot.checker.scoring import compute_score

    result = compute_score(scan_repo(path), run_smoke_test=run_smoke_test)
    score = result["score"]

    typer.echo(f"ReproPilot check  —  {path}")
    typer.echo(f"Score : {score}/100  [mode: {result['mode']}]")
    typer.echo(f"Passed: {len(result['passed'])} rule(s)")
    typer.echo(f"Failed: {len(result['failed'])} rule(s)")

    if result["not_assessed"]:
        ids = ", ".join(r.id for r in result["not_assessed"])
        typer.echo(f"runnable evidence: not assessed ({ids})")

    if result["failed"]:
        typer.echo("")
        for rule in result["failed"]:
            typer.echo(f"  [{rule.id}] {rule.description}")
            typer.echo(f"         Fix: {rule.fix}")

    typer.echo("")
    if score >= 90:
        typer.echo(f"PASS  score {score} >= 90")
    else:
        typer.echo(f"FAIL  score {score} < 90")
        raise typer.Exit(1)


@app.command()
def version() -> None:
    typer.echo("repropilot 0.1.0")
