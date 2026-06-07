"""Wrappers around external computational chemistry / biochemistry engines.

Each engine adapts a third-party library (PySCF, OpenMM, RDKit, ASE ...) to
the Kimika :class:`~kimika.engines.base.Engine` interface so that tasks can
treat them uniformly.
"""

from kimika.engines.base import Engine
from kimika.engines.registry import ENGINE_REGISTRY, register_engine

__all__ = ["ENGINE_REGISTRY", "Engine", "register_engine"]
