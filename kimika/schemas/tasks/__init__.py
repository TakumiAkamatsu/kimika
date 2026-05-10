"""Per-task schemas.

Concrete task schemas (``qm``, ``md``, ``docking`` ...) will be added as the
corresponding tasks are implemented. The ``TaskConfig`` alias here is a typed
placeholder so that :class:`kimika.schemas.recipe.Recipe` can already reference
it.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from kimika.schemas.base import KimikaModel


class TaskConfig(KimikaModel):
    """Generic task configuration placeholder.

    Until task-specific schemas are introduced, recipes are validated against
    this permissive structure: a discriminator (``type``), a target engine, and
    a free-form ``parameters`` mapping.
    """

    type: str
    engine: str
    parameters: dict[str, Any] = Field(default_factory=dict)


__all__ = ["TaskConfig"]
