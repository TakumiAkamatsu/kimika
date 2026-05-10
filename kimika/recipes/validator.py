"""Recipe validation entry points used by the CLI and UI."""

from __future__ import annotations

from pathlib import Path

from pydantic import ValidationError

from kimika.recipes.loader import load_recipe
from kimika.schemas.recipe import Recipe


def validate_recipe(path: Path | str) -> Recipe:
    """Validate a recipe file and return the parsed model.

    The function re-raises :class:`pydantic.ValidationError` so callers can
    render error reports as they see fit. It exists as a thin wrapper to make
    the validate-vs-load distinction explicit at call sites.
    """
    try:
        return load_recipe(path)
    except ValidationError:
        raise
