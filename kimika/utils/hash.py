"""Hashing helpers for reproducibility and caching.

Concrete hashing strategies (recipe-content hash, input-file hash, etc.) will
be added when the runner needs them.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


def sha256_file(path: Path, chunk_size: int = 1 << 20) -> str:
    """Compute the SHA-256 of a file's contents in streamed chunks."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()
