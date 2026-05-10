"""Load recipe YAML files into Pydantic models."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ruamel.yaml import YAML

from kimika.schemas.recipe import Recipe

_yaml = YAML(typ="safe")


def _read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = _yaml.load(handle)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"Recipe at {path} must be a YAML mapping at the top level.")
    return data


def load_recipe(path: Path | str) -> Recipe:
    """Read a YAML file from ``path`` and return a validated :class:`Recipe`."""
    return Recipe.model_validate(_read_yaml(Path(path)))
