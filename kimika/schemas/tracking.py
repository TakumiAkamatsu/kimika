"""Schema for experiment-tracking configuration."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from kimika.schemas.base import KimikaModel


class TrackingConfig(KimikaModel):
    """Where and how experiment runs are recorded."""

    backend: Literal["mlflow", "none"] = "mlflow"
    experiment_name: str | None = None
    tracking_uri: str | None = Field(
        default=None,
        description="Override for the MLflow tracking URI; defaults to the workspace setting.",
    )
    log_artifacts: bool = True
