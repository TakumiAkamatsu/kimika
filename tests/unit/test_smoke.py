"""Trivial smoke tests for the initial scaffold.

These tests ensure that the package imports and the CLI is wired correctly.
They will be replaced by proper unit tests once concrete functionality lands.
"""

from __future__ import annotations

from typer.testing import CliRunner

from kimika import __version__
from kimika.cli.main import app


def test_version_string() -> None:
    assert isinstance(__version__, str)
    assert __version__


def test_cli_help() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "kimika" in result.stdout.lower()


def test_cli_version() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout


def test_config_show() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["config", "show"])
    assert result.exit_code == 0
    assert "workspace" in result.stdout
