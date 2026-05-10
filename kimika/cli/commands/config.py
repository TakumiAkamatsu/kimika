"""``kimika config`` — show or edit Kimika configuration."""

from __future__ import annotations

import json

import typer
from rich.console import Console

from kimika.utils.config import as_dict, load_config, user_config_path

app = typer.Typer(help="Show or edit Kimika configuration.", no_args_is_help=True)
console = Console()


@app.command("show")
def show() -> None:
    """Print the resolved configuration as JSON."""
    cfg = load_config()
    console.print(f"[dim]config file: {user_config_path()}[/dim]")
    console.print_json(json.dumps(as_dict(cfg)))


@app.command("path")
def path() -> None:
    """Print the path to the user config file."""
    typer.echo(str(user_config_path()))
