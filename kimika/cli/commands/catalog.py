"""``kimika catalog`` — list the official recipe catalog shipped with Kimika."""

from __future__ import annotations

from importlib import resources
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()


def _catalog_root() -> Path | None:
    """Locate the ``recipes/`` directory shipped alongside the package source.

    The catalog lives at the repo root (not inside the installed package), so
    this only returns a path when running from a source checkout.
    """
    pkg_dir = Path(str(resources.files("kimika")))
    candidate = pkg_dir.parent / "recipes"
    return candidate if candidate.is_dir() else None


def catalog() -> None:
    root = _catalog_root()
    if root is None:
        console.print("[yellow]No bundled recipe catalog found in this install.[/yellow]")
        return

    table = Table(title="Kimika recipe catalog")
    table.add_column("Category")
    table.add_column("Recipe")
    table.add_column("Path")

    found = False
    for recipe_yaml in sorted(root.rglob("recipe.yaml")):
        rel = recipe_yaml.relative_to(root)
        category = rel.parts[0] if len(rel.parts) >= 2 else "-"
        name = rel.parts[-2] if len(rel.parts) >= 2 else recipe_yaml.parent.name
        table.add_row(category, name, str(recipe_yaml))
        found = True

    if not found:
        console.print(f"[dim]Catalog at {root} is empty.[/dim]")
        return
    console.print(table)
