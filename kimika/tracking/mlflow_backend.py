"""MLflow backend wrappers.

Concrete logging logic is added when the runner needs to record runs; this
module currently exposes the URI resolution helpers used by the CLI.
"""

from __future__ import annotations

from kimika.utils.config import KimikaConfig


def resolve_tracking_uri(cfg: KimikaConfig) -> str:
    """Return the effective MLflow tracking URI for a config."""
    return cfg.mlflow_tracking_uri
