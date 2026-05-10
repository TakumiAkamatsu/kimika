"""Configuration system for Kimika.

Resolution order (highest priority first):

1. Environment variables (``KIMIKA_WORKSPACE_ROOT``, ``KIMIKA_MLFLOW_URI`` ...)
2. The user config file at ``$XDG_CONFIG_HOME/kimika/config.toml`` (default
   ``~/.config/kimika/config.toml``).
3. Built-in defaults.

Only the data structures and accessor logic are implemented here. Reading and
writing the config file uses the standard-library :mod:`tomllib` for parsing;
writing is performed by serialising a small subset of TOML by hand to avoid
adding a writer dependency.
"""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from kimika.utils.paths import expand, xdg_config_home


def _default_workspace_root() -> Path:
    return Path.home() / "kimika"


def _default_mlflow_uri(workspace_root: Path) -> str:
    return f"file:{workspace_root / '.mlruns'}"


@dataclass(slots=True)
class WorkspaceConfig:
    root: Path = field(default_factory=_default_workspace_root)


@dataclass(slots=True)
class UIConfig:
    default_page: str = "home"


@dataclass(slots=True)
class MLflowConfig:
    tracking_uri: str | None = None
    """When ``None`` it defaults to ``file:<workspace_root>/.mlruns``."""


@dataclass(slots=True)
class KimikaConfig:
    workspace: WorkspaceConfig = field(default_factory=WorkspaceConfig)
    ui: UIConfig = field(default_factory=UIConfig)
    mlflow: MLflowConfig = field(default_factory=MLflowConfig)

    @property
    def mlflow_tracking_uri(self) -> str:
        if self.mlflow.tracking_uri:
            return self.mlflow.tracking_uri
        return _default_mlflow_uri(self.workspace.root)


def user_config_path() -> Path:
    """Return the canonical user config file path."""
    return xdg_config_home() / "kimika" / "config.toml"


def _load_config_file(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    with path.open("rb") as handle:
        return tomllib.load(handle)


def _apply_file(cfg: KimikaConfig, data: dict[str, Any]) -> None:
    workspace = data.get("workspace", {})
    if "root" in workspace:
        cfg.workspace.root = expand(workspace["root"])

    ui = data.get("ui", {})
    if "default_page" in ui:
        cfg.ui.default_page = str(ui["default_page"])

    mlflow = data.get("mlflow", {})
    if "tracking_uri" in mlflow:
        cfg.mlflow.tracking_uri = str(mlflow["tracking_uri"])


def _apply_env(cfg: KimikaConfig) -> None:
    if (value := os.environ.get("KIMIKA_WORKSPACE_ROOT")) is not None:
        cfg.workspace.root = expand(value)
    if (value := os.environ.get("KIMIKA_UI_DEFAULT_PAGE")) is not None:
        cfg.ui.default_page = value
    if (value := os.environ.get("KIMIKA_MLFLOW_URI")) is not None:
        cfg.mlflow.tracking_uri = value


def load_config(*, config_path: Path | None = None) -> KimikaConfig:
    """Build a :class:`KimikaConfig` by layering defaults, file, and env."""
    cfg = KimikaConfig()
    path = config_path or user_config_path()
    _apply_file(cfg, _load_config_file(path))
    _apply_env(cfg)
    cfg.workspace.root = expand(cfg.workspace.root)
    return cfg


def as_dict(cfg: KimikaConfig) -> dict[str, Any]:
    """Render a config as a plain dict suitable for display / serialization."""
    return {
        "workspace": {"root": str(cfg.workspace.root)},
        "ui": {"default_page": cfg.ui.default_page},
        "mlflow": {"tracking_uri": cfg.mlflow_tracking_uri},
    }
