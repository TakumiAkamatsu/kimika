"""User workspace management.

The workspace is the place where user-owned experiments live (entirely outside
the Kimika source tree). See :mod:`kimika.workspace.layout` for the directory
contract and :mod:`kimika.workspace.init` for project bootstrapping.
"""

from kimika.workspace.init import init_project
from kimika.workspace.layout import KIMIKA_MARKER, project_marker
from kimika.workspace.project import KimikaProject

__all__ = ["KIMIKA_MARKER", "KimikaProject", "init_project", "project_marker"]
