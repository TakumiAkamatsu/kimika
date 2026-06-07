"""Top-level recipe schema."""

from __future__ import annotations

from pydantic import Field

from kimika.schemas.base import KimikaModel
from kimika.schemas.system import SystemConfig
from kimika.schemas.tasks import TaskConfig
from kimika.schemas.tracking import TrackingConfig


class ProjectInfo(KimikaModel):
    name: str
    description: str = ""
    tags: list[str] = Field(default_factory=list)


class OutputConfig(KimikaModel):
    results_dir: str = "results"
    save_wavefunction: bool = False


class Recipe(KimikaModel):
    """The full recipe document loaded from ``recipe.yaml``."""

    version: str
    project: ProjectInfo
    system: SystemConfig
    task: TaskConfig
    tracking: TrackingConfig = Field(default_factory=TrackingConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
