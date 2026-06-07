"""Task implementations.

A *task* is the "what" — e.g. a single-point QM calculation or an MD run. Each
task delegates to one or more :mod:`kimika.engines` to perform the work.
"""

from kimika.tasks.base import Task
from kimika.tasks.registry import TASK_REGISTRY, register_task

__all__ = ["TASK_REGISTRY", "Task", "register_task"]
