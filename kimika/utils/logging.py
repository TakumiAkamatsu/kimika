"""Loguru-based logging helpers.

The implementation here is intentionally minimal; richer configuration (log
levels per module, file sinks, etc.) is added once concrete tasks need it.
"""

from __future__ import annotations

from loguru import logger

__all__ = ["logger"]
