# Contributing to Kimika

Thank you for your interest in contributing.

## Development environment

```bash
uv sync --extra dev
uv run pre-commit install
```

## Code style

- `ruff check` and `ruff format` for linting and formatting.
- `mypy` (strict) for static type checking.
- `pytest` for tests.

Run all checks with:

```bash
uv run ruff check kimika tests
uv run ruff format --check kimika tests
uv run mypy
uv run pytest
```

## Repository conventions

- Code and experiment data must remain separated. The repository contains
  source code and the official recipe catalog only; user experiments live in
  the workspace (default `~/kimika/`).
- Do not edit recipes in `recipes/` to drive your own experiments — copy them
  into your workspace via `kimika init` instead.
- Add new dependencies with `uv add <pkg>` (or `uv add --dev <pkg>` for dev
  tools). Computational engines belong in core dependencies.
