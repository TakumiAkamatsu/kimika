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

# Create a project in the default workspace (~/.kimika)
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
root (default `~/.kimika/`). See `CLAUDE.md` for the full design contract.

## License

Kimika is distributed under the [GNU General Public License v3.0 or
later](LICENSE) (`GPL-3.0-or-later`). You are free to use, study, modify,
and redistribute it under the terms of that license. In particular, any
distributed derivative work must also be released under the same license
and ship its complete corresponding source code.

The choice of GPL is intended to keep the project useful for research and
to ensure that improvements made on top of Kimika flow back to the
community rather than being absorbed into closed-source forks.
