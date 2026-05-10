# Kimika

Recipe-driven software for computational chemistry and computational
biochemistry. Designed to scale from molecular simulations toward cell-level
biochemistry, with a Streamlit-based UI as the primary interface.

> **Project status: pre-alpha.** Only the package skeleton is in place. No
> tasks or engines are wired up yet.

## Supported platforms

- Linux and macOS only.
- Python 3.11–3.13.
- Managed with [uv](https://docs.astral.sh/uv/).

## Getting started

```bash
# Set up the development environment
uv sync --extra dev

# Verify the CLI works
uv run kimika --version

# Create a project in the default workspace (~/kimika)
uv run kimika init my_project

# Launch the Streamlit UI
uv run kimika ui
```

## Repository layout

- `kimika/` — the Python package (schemas, tasks, engines, recipe runner, UI, CLI).
- `recipes/` — the official recipe catalog (placeholder until concrete recipes land).
- `examples/` — quick-start examples.
- `tests/` — unit and integration tests.
- `docs/` — documentation sources (built with MkDocs).

User-owned experiments live **outside** this repository, under the workspace
root (default `~/kimika/`). See `CLAUDE.md` for the full design contract.

## License

To be decided.
