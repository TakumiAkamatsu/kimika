# Official recipe catalog

This directory holds the recipes shipped with Kimika and exercised by the
test suite. Recipes here are read-only references — to drive your own
experiments, create a project in your workspace via `kimika init` and edit
the copy that lands there.

The catalog is split by task family:

```
recipes/
├── qm/        # Quantum chemistry (DFT, MP2, ...)
├── md/        # Molecular dynamics
└── docking/   # Protein-ligand docking
```

Each recipe lives in its own subdirectory and contains at least:

- `recipe.yaml` — the recipe document.
- `inputs/` — input geometries / topologies referenced by `recipe.yaml`.
- `README.md` — a short description.

The catalog is currently empty; concrete recipes will be added once the
matching tasks and engines are implemented.
