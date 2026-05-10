"""Registry mapping task identifiers to implementations."""

from __future__ import annotations

from collections.abc import Callable

from kimika.tasks.base import Task

TASK_REGISTRY: dict[str, type[Task]] = {}


def register_task(name: str) -> Callable[[type[Task]], type[Task]]:
    """Decorator that registers a task implementation under ``name``."""

    def decorator(cls: type[Task]) -> type[Task]:
        if name in TASK_REGISTRY:
            raise ValueError(f"Task '{name}' is already registered.")
        TASK_REGISTRY[name] = cls
        cls.name = name
        return cls

    return decorator
