"""Schemas describing the molecular / periodic system to operate on."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field

from kimika.schemas.base import KimikaModel


class SystemSource(KimikaModel):
    """Where the input geometry / topology comes from."""

    format: str = Field(description="Input format identifier, e.g. 'xyz', 'pdb', 'sdf'.")
    path: Path = Field(description="Path to the input file, relative to the recipe directory.")


class SystemConfig(KimikaModel):
    """Top-level description of a molecular or periodic system."""

    type: Literal["molecule", "periodic"] = "molecule"
    source: SystemSource
    charge: int = 0
    multiplicity: int = Field(default=1, ge=1)
