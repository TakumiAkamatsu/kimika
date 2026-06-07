"""Streamlit entry point for the Kimika UI.

Run via ``kimika ui`` (which invokes ``streamlit run`` on this module) or
``streamlit run kimika/ui/app.py`` directly.
"""

from __future__ import annotations

import streamlit as st

from kimika import __version__
from kimika.utils.config import as_dict, load_config


def main() -> None:
    st.set_page_config(page_title="Kimika", layout="wide")
    st.title("Kimika")
    st.caption(f"v{__version__} — recipe-driven computational chemistry")

    cfg = load_config()
    st.subheader("Workspace")
    st.write(f"Workspace root: `{cfg.workspace.root}`")
    st.write(f"MLflow tracking URI: `{cfg.mlflow_tracking_uri}`")

    with st.expander("Active configuration"):
        st.json(as_dict(cfg))

    st.info(
        "This is the initial scaffold. Recipe builder, runner, and results "
        "viewer pages will land in subsequent commits."
    )


if __name__ == "__main__":
    main()
