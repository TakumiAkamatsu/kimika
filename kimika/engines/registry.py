"""Registry mapping engine identifiers to wrapper classes."""

from __future__ import annotations

from collections.abc import Callable

from kimika.engines.base import Engine

ENGINE_REGISTRY: dict[str, type[Engine]] = {}


def register_engine(name: str) -> Callable[[type[Engine]], type[Engine]]:
    """Decorator that registers an engine wrapper under ``name``."""

    def decorator(cls: type[Engine]) -> type[Engine]:
        if name in ENGINE_REGISTRY:
            raise ValueError(f"Engine '{name}' is already registered.")
        ENGINE_REGISTRY[name] = cls
        cls.name = name
        return cls

    return decorator
