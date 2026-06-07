"""Recipe execution orchestration.

The runner ties together a validated :class:`~kimika.schemas.recipe.Recipe`,
the task / engine registries, and the tracking backend. The actual execution
logic is filled in once concrete tasks land; this module only exposes the
intended entry point so that the CLI and UI can already wire to it.
"""

from __future__ import annotations

from pathlib import Path

from kimika.schemas.recipe import Recipe


class RecipeRunner:
    """Execute a recipe end-to-end."""

    def __init__(self, recipe: Recipe, *, recipe_dir: Path) -> None:
        self.recipe = recipe
        self.recipe_dir = recipe_dir

    def run(self) -> None:
        """Run the recipe.

        The execution pipeline (resolve task, look up engine, log to tracker,
        write results) will be implemented alongside the first concrete task.
        """
        raise NotImplementedError(
            "RecipeRunner.run will be implemented together with the first task."
        )
