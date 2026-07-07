"""PawPal+ core system classes.

Implements the model from diagrams/uml.mmd.
Classes: Owner, Pet, Task, Scheduler.
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
        self.completed = True

    def edit(
        self,
        name: str | None = None,
        category: str | None = None,
        duration: int | None = None,
        priority: int | None = None,
    ) -> None:
        """Update any of this task's editable fields (only non-None values)."""
        if name is not None:
            self.name = name
        if category is not None:
            self.category = category
        if duration is not None:
            self.duration = duration
        if priority is not None:
            self.priority = priority


@dataclass
class Pet:
    """A pet that has care tasks associated with it."""

    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove a care task from this pet by its id."""
        self.tasks = [t for t in self.tasks if t.id != task_id]


@dataclass
class Owner:
    """The pet owner, including their care constraints and preferences."""

    name: str
    minutes_available: int
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def set_availability(self, minutes: int) -> None:
        """Set how many minutes the owner has available today."""
        self.minutes_available = minutes

    def all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets (flattened)."""
        return [task for pet in self.pets for task in pet.tasks]


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
        budget = owner.minutes_available
        self.scheduled = []
        self.skipped = []

        # Remember which pet each task belongs to, so the plan can label them.
        self.pet_by_task = {
            task.id: pet.name for pet in owner.pets for task in pet.tasks
        }

        # Only plan tasks that still need doing, most important first.
        pending = [t for t in owner.all_tasks() if not t.completed]
        for task in self.prioritize(pending):
            if task.duration <= budget:
                self.scheduled.append(task)
                budget -= task.duration
            else:
                self.skipped.append(task)

        return self.scheduled

    def prioritize(self, tasks: list[Task]) -> list[Task]:
        """Order tasks by priority (highest first), then by shortest duration.

        Ties break toward shorter tasks so more can fit within the budget.
        """
        return sorted(tasks, key=lambda t: (-t.priority, t.duration))

    def explain(self) -> str:
        """Return a human-readable explanation of the last generated plan."""
        if not self.scheduled and not self.skipped:
            return "No plan has been generated yet."

        lines: list[str] = []
        total = sum(t.duration for t in self.scheduled)
        lines.append(
            f"Scheduled {len(self.scheduled)} task(s) using {total} minute(s):"
        )
        for t in self.scheduled:
            pet = self.pet_by_task.get(t.id, "?")
            lines.append(
                f"  • [{pet}] {t.name} ({t.category}) — {t.duration} min, priority {t.priority}"
            )

        if self.skipped:
            lines.append(
                f"Skipped {len(self.skipped)} task(s) that didn't fit the time budget:"
            )
            for t in self.skipped:
                pet = self.pet_by_task.get(t.id, "?")
                lines.append(
                    f"  • [{pet}] {t.name} ({t.category}) — {t.duration} min, priority {t.priority}"
                )

        return "\n".join(lines)
