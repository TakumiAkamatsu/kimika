"""Abstract base class for engine wrappers."""

from __future__ import annotations

from abc import ABC


class Engine(ABC):
    """Adapter around an external computational engine.

    Concrete subclasses expose engine-specific entry points (``run_scf``,
    ``run_md`` ...). The base class only fixes the registration contract.
    """

    #: Identifier used in recipes (``task.engine``).
    name: str
