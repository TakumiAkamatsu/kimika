"""Project-level helpers for a single Kimika project directory."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from kimika.workspace.layout import is_project


@dataclass(slots=True)
class KimikaProject:
    """A handle to a single project on disk."""

    path: Path

    @classmethod
    def open(cls, path: Path | str) -> KimikaProject:
        project_path = Path(path).expanduser().resolve()
        if not is_project(project_path):
            raise FileNotFoundError(f"{project_path} is not a Kimika project.")
        return cls(path=project_path)

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def recipe_path(self) -> Path:
        return self.path / "recipe.yaml"

    @property
    def inputs_dir(self) -> Path:
        return self.path / "inputs"

    @property
    def results_dir(self) -> Path:
        return self.path / "results"
