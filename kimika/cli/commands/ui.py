"""``kimika ui`` — launch the Streamlit UI."""

from __future__ import annotations

import subprocess
import sys
from importlib import resources

import typer


def ui(
    port: int = typer.Option(8501, "--port", help="Port to bind the Streamlit server to."),
    host: str = typer.Option("localhost", "--host", help="Host to bind to."),
) -> None:
    app_path = resources.files("kimika.ui").joinpath("app.py")
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(app_path),
        "--server.port",
        str(port),
        "--server.address",
        host,
    ]
    raise typer.Exit(code=subprocess.call(cmd))
