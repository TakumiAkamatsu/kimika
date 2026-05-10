"""``kimika init`` — create a new project from a workspace template."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from kimika.utils.config import load_config
from kimika.workspace.init import init_project

console = Console()


def init(
    project_name: str = typer.Argument(..., help="Name of the new project."),
    path: Path | None = typer.Option(  # noqa: B008
        None,
        "--path",
        help="Custom project location. Defaults to <workspace_root>/<project_name>.",
    ),
    template: str = typer.Option(
        "default",
        "--template",
        help="Workspace template to use.",
    ),
) -> None:
    cfg = load_config()
    target = init_project(
        project_name,
        workspace_root=cfg.workspace.root,
        template=template,
        project_path=path,
    )
    console.print(f"[green]Created project[/green] [bold]{project_name}[/bold] at {target}")
