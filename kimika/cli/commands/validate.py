"""``kimika validate`` — load and validate a recipe.yaml file."""

from __future__ import annotations

from pathlib import Path

import typer
from pydantic import ValidationError
from rich.console import Console

from kimika.recipes.validator import validate_recipe

console = Console()


def validate(
    recipe_path: Path = typer.Argument(  # noqa: B008
        ..., exists=True, dir_okay=False, readable=True, help="Path to recipe.yaml."
    ),
) -> None:
    try:
        recipe = validate_recipe(recipe_path)
    except ValidationError as exc:
        console.print("[red]Recipe is invalid:[/red]")
        console.print(str(exc))
        raise typer.Exit(code=1) from exc
    console.print(f"[green]OK[/green] — recipe '{recipe.project.name}' validates.")
