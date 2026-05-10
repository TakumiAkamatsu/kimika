"""Top-level Typer application that wires the ``kimika`` subcommands."""

from __future__ import annotations

import typer

from kimika import __version__
from kimika.cli.commands import (
    catalog as catalog_cmd,
)
from kimika.cli.commands import (
    config as config_cmd,
)
from kimika.cli.commands import (
    init as init_cmd,
)
from kimika.cli.commands import (
    run as run_cmd,
)
from kimika.cli.commands import (
    ui as ui_cmd,
)
from kimika.cli.commands import (
    validate as validate_cmd,
)

app = typer.Typer(
    name="kimika",
    help="Recipe-driven computational chemistry / biochemistry.",
    no_args_is_help=True,
    add_completion=False,
)

app.command("init", help="Create a new Kimika project from a template.")(init_cmd.init)
app.command("validate", help="Validate a recipe.yaml file.")(validate_cmd.validate)
app.command("run", help="Run a recipe.")(run_cmd.run)
app.command("ui", help="Launch the Streamlit UI.")(ui_cmd.ui)
app.command("catalog", help="List the official recipe catalog.")(catalog_cmd.catalog)
app.add_typer(config_cmd.app, name="config", help="Show or edit Kimika configuration.")


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"kimika {__version__}")
        raise typer.Exit


@app.callback()
def _root(
    version: bool = typer.Option(
        False,
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Show the installed Kimika version and exit.",
    ),
) -> None:
    """Root callback used to surface global options (``--version``)."""
    del version


if __name__ == "__main__":
    app()
