"""``kimika run`` — execute a recipe."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

console = Console()


def run(
    recipe_path: Path = typer.Argument(  # noqa: B008
        ..., exists=True, dir_okay=False, readable=True, help="Path to recipe.yaml."
    ),
) -> None:
    del recipe_path
    console.print(
        "[yellow]kimika run is not implemented yet.[/yellow] "
        "It will land alongside the first concrete task."
    )
    raise typer.Exit(code=2)
