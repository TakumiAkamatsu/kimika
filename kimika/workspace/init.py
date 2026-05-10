"""Implementation of ``kimika init``: project bootstrapping from a template."""

from __future__ import annotations

import shutil
from importlib import resources
from pathlib import Path

from kimika.workspace.layout import KIMIKA_MARKER, is_project

_TEMPLATE_PACKAGE = "kimika.workspace.templates"


def _template_dir(template: str) -> Path:
    """Return the on-disk path of a packaged template directory."""
    base = resources.files(_TEMPLATE_PACKAGE)
    target = base.joinpath(template)
    # ``resources.files`` returns a Traversable; converting via ``str()`` gives
    # us a usable filesystem path because templates ship as regular files.
    return Path(str(target))


def init_project(
    project_name: str,
    *,
    workspace_root: Path,
    template: str = "default",
    project_path: Path | None = None,
) -> Path:
    """Create a new Kimika project.

    By default the project is created at ``workspace_root / project_name``.
    Pass ``project_path`` to choose a custom location instead (in which case
    ``project_name`` is used only to substitute placeholders).
    """
    target = (project_path or (workspace_root / project_name)).expanduser().resolve()
    if target.exists():
        if any(target.iterdir()) or is_project(target):
            raise FileExistsError(f"Refusing to overwrite existing path: {target}")
    else:
        target.mkdir(parents=True)

    src = _template_dir(template)
    if not src.is_dir():
        raise FileNotFoundError(f"Unknown workspace template: {template!r} (looked in {src}).")

    for entry in src.rglob("*"):
        rel = entry.relative_to(src)
        dst = target / rel
        if entry.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(entry, dst)

    _substitute_placeholders(target, project_name=project_name)
    (target / KIMIKA_MARKER).write_text(f"project_name: {project_name}\n", encoding="utf-8")
    return target


def _substitute_placeholders(project_dir: Path, *, project_name: str) -> None:
    """Replace ``{{project_name}}`` placeholders in template text files."""
    for path in project_dir.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if "{{project_name}}" in text:
            path.write_text(text.replace("{{project_name}}", project_name), encoding="utf-8")
