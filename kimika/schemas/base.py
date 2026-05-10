"""Common base classes for Pydantic schemas."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class KimikaModel(BaseModel):
    """Base model with project-wide defaults."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
        populate_by_name=True,
    )
