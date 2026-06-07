"""Layout contract for Kimika workspaces and individual projects."""

from __future__ import annotations

from pathlib import Path

#: Filename used to mark a directory as a Kimika project.
KIMIKA_MARKER = ".kimika"


def project_marker(project_dir: Path) -> Path:
    """Return the marker file path for a project directory."""
    return project_dir / KIMIKA_MARKER


def is_project(project_dir: Path) -> bool:
    """Return True if ``project_dir`` looks like a Kimika project."""
    return project_marker(project_dir).is_file()


def iter_projects(workspace_root: Path) -> list[Path]:
    """List all project directories directly under ``workspace_root``."""
    if not workspace_root.is_dir():
        return []
    return sorted(child for child in workspace_root.iterdir() if is_project(child))
