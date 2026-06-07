"""Streamlit home page: lists projects in the active workspace."""

from __future__ import annotations

import streamlit as st

from kimika.utils.config import load_config
from kimika.workspace.layout import iter_projects


def render() -> None:
    cfg = load_config()
    st.header("Home")
    st.write(f"Workspace root: `{cfg.workspace.root}`")

    projects = iter_projects(cfg.workspace.root)
    if not projects:
        st.info("No projects found yet. Create one with `kimika init <name>`.")
        return

    for project in projects:
        st.write(f"- `{project.name}` ({project})")


if __name__ == "__main__":
    render()
