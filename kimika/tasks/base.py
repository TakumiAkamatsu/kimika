"""Abstract base class for Kimika tasks."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from kimika.schemas.tasks import TaskConfig


class Task(ABC):
    """A unit of computational work described by a recipe.

    Subclasses implement :meth:`run` for a specific kind of calculation; the
    actual numerical work is delegated to a :class:`kimika.engines.base.Engine`.
    """

    #: Identifier used in recipes (``task.type``).
    name: str

    @abstractmethod
    def run(self, config: TaskConfig) -> dict[str, Any]:
        """Execute the task and return a result dictionary."""
