"""Filesystem path helpers."""

from __future__ import annotations

import os
from pathlib import Path


def expand(path: str | os.PathLike[str]) -> Path:
    """Expand ``~`` and environment variables, then resolve to an absolute path."""
    return Path(os.path.expandvars(os.fspath(path))).expanduser().resolve()


def xdg_config_home() -> Path:
    """Return the XDG config home directory (``$XDG_CONFIG_HOME`` or ``~/.config``)."""
    raw = os.environ.get("XDG_CONFIG_HOME")
    if raw:
        return expand(raw)
    return Path.home() / ".config"
