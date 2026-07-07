"""PawPal+ core system classes (SKELETON).

Implements the model from diagrams/uml.mmd.
Classes: Owner, Pet, Task, Scheduler.

This is a skeleton: signatures, dataclass fields, and docstrings are in
place, but method bodies are unimplemented. Fill in the `...` / raise
statements with real logic.
"""

"""
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet care task (walk, feeding, meds, enrichment, etc.)."""

    name: str
    category: str
    duration: int          # minutes
    priority: int          # higher = more important
    completed: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def mark_done(self) -> None:
        """Mark this task as completed."""
        raise NotImplementedError

    def edit(
        self,
        name: str | None = None,
        category: str | None = None,
        duration: int | None = None,
        priority: int | None = None,
    ) -> None:
        """Update any of this task's editable fields (only non-None values)."""
        raise NotImplementedError


@dataclass
class Pet:
    """A pet that has care tasks associated with it."""

    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        raise NotImplementedError

    def remove_task(self, task_id: str) -> None:
        """Remove a care task from this pet by its id."""
        raise NotImplementedError


@dataclass
class Owner:
    """The pet owner, including their care constraints and preferences."""

    name: str
    minutes_available: int
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        raise NotImplementedError

    def set_availability(self, minutes: int) -> None:
        """Set how many minutes the owner has available today."""
        raise NotImplementedError

    def all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets (flattened)."""
        raise NotImplementedError


@dataclass
class Scheduler:
    """Builds a daily care plan from owner constraints and pet tasks.

    Reads the time budget from ``Owner.minutes_available`` and remembers its
    last result so the plan can be displayed and explained afterwards.
    """

    scheduled: list[Task] = field(default_factory=list)
    skipped: list[Task] = field(default_factory=list)
    pet_by_task: dict[str, str] = field(default_factory=dict)

    def generate_plan(self, owner: Owner) -> list[Task]:
        """Build a daily schedule from all of the owner's pets' tasks.

        Prioritizes tasks, fits as many as possible within
        ``owner.minutes_available``, and stores the result in ``scheduled``
        and ``skipped``. Returns the scheduled tasks.
        """
        raise NotImplementedError

    def prioritize(self, tasks: list[Task]) -> list[Task]:
        """Order tasks by priority (highest first), then by shortest duration.

        Ties break toward shorter tasks so more can fit within the budget.
        """
        raise NotImplementedError

    def explain(self) -> str:
        """Return a human-readable explanation of the last generated plan."""
        raise NotImplementedError
    