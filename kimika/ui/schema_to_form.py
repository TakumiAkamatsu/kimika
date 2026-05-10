"""Pydantic-to-Streamlit form generation.

Wraps :mod:`streamlit_pydantic` and adds custom widgets where the upstream
support is lacking. Concrete adapters will be added when individual schemas
need them.
"""

from __future__ import annotations
