"""PawPal+ core system classes.

Implements the model from diagrams/uml.mmd.
Classes: Owner, Pet, Task, Scheduler.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field, replace
from datetime import date, timedelta

# How far ahead the next occurrence of a recurring task is due.
RECURRENCE_STEP = {
    "daily": timedelta(days=1),
    "weekly": timedelta(weeks=1),
}


@dataclass
class Task:
    """A single pet care task (walk, feeding, meds, enrichment, etc.)."""

    name: str
    category: str
    duration: int          # minutes
    priority: int          # higher = more important
    time: str | None = None    # scheduled start as "HH:MM"; None = unscheduled
    frequency: str = "once"    # "once", "daily", or "weekly"
    due_date: date | None = None  # which day this task is due
    completed: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @property
    def recurring(self) -> bool:
        """True when this task repeats (daily or weekly)."""
        return self.frequency in RECURRENCE_STEP

    def mark_done(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def next_occurrence(self) -> Task | None:
        """Build the next instance of a recurring task, or None if it doesn't
        repeat.

        The copy is a fresh, uncompleted task (new id) whose ``due_date`` is
        advanced by one step past this task's due date — using ``timedelta`` so
        month and year rollovers are handled correctly. If this task had no due
        date yet, the next one is due one step from today.
        """
        step = RECURRENCE_STEP.get(self.frequency)
        if step is None:
            return None
        base = self.due_date or date.today()
        return replace(
            self,
            due_date=base + step,
            completed=False,
            id=str(uuid.uuid4()),
        )

    def edit(
        self,
        name: str | None = None,
        category: str | None = None,
        duration: int | None = None,
        priority: int | None = None,
        time: str | None = None,
        frequency: str | None = None,
        due_date: date | None = None,
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
        if time is not None:
            self.time = time
        if frequency is not None:
            self.frequency = frequency
        if due_date is not None:
            self.due_date = due_date


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

    def mark_task_complete(self, task_id: str) -> Task | None:
        """Mark one of this pet's tasks complete.

        If the task recurs (daily/weekly), its next occurrence is created and
        added to this pet automatically, so the routine keeps rolling forward.
        Returns the newly scheduled task, or None if nothing recurred.
        """
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task is None:
            return None

        task.mark_done()
        upcoming = task.next_occurrence()
        if upcoming is not None:
            self.add_task(upcoming)
        return upcoming


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
        self.index_pets(owner)

        # Only plan tasks that still need doing, most important first.
        pending = [t for t in owner.all_tasks() if not t.completed]
        for task in self.prioritize(pending):
            if task.duration <= budget:
                self.scheduled.append(task)
                budget -= task.duration
            else:
                self.skipped.append(task)

        return self.scheduled

    def index_pets(self, owner: Owner) -> None:
        """Record which pet each task belongs to, so tasks can be labelled and
        filtered by pet name later.
        """
        self.pet_by_task = {
            task.id: pet.name for pet in owner.pets for task in pet.tasks
        }

    def prioritize(self, tasks: list[Task]) -> list[Task]:
        """Order tasks by priority (highest first), then by shortest duration.

        Ties break toward shorter tasks so more can fit within the budget.
        """
        return sorted(tasks, key=lambda t: (-t.priority, t.duration))

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks ordered by their scheduled ``time`` ("HH:MM").

        Because "HH:MM" strings are zero-padded, they sort correctly with plain
        string comparison, so the lambda key can hand each task's ``time`` string
        straight to ``sorted()``. Unscheduled tasks (``time is None``) sort last.
        """
        return sorted(tasks, key=lambda t: t.time if t.time is not None else "99:99")

    def filter_tasks(
        self,
        tasks: list[Task],
        pet_name: str | None = None,
        completed: bool | None = None,
    ) -> list[Task]:
        """Filter tasks by pet name and/or completion status.

        Pass only the criteria you care about; ``None`` means "don't filter on
        this". Pet-name filtering uses the ``pet_by_task`` index, so call
        ``generate_plan`` or ``index_pets`` first.
        """
        result = tasks
        if pet_name is not None:
            result = [t for t in result if self.pet_by_task.get(t.id) == pet_name]
        if completed is not None:
            result = [t for t in result if t.completed == completed]
        return result

    def detect_conflicts(self, tasks: list[Task]) -> list[tuple[Task, Task]]:
        """Find pairs of scheduled tasks whose times overlap on the same day.

        Two tasks conflict when the earlier one is still running (start +
        duration) at the moment the next one is due to start. Only tasks that
        share a ``due_date`` are compared, so tomorrow's recurring copy never
        clashes with today's. Unscheduled (no ``time``) and completed tasks are
        ignored.
        """
        candidates = [t for t in tasks if t.time is not None and not t.completed]

        # Compare tasks only against others due the same day.
        by_day: dict[date | None, list[Task]] = {}
        for task in candidates:
            by_day.setdefault(task.due_date, []).append(task)

        conflicts: list[tuple[Task, Task]] = []
        for same_day in by_day.values():
            timed = self.sort_by_time(same_day)
            for earlier, later in zip(timed, timed[1:]):
                if self._to_minutes(earlier.time) + earlier.duration > self._to_minutes(
                    later.time
                ):
                    conflicts.append((earlier, later))
        return conflicts

    @staticmethod
    def _to_minutes(hhmm: str) -> int:
        """Convert an "HH:MM" time string to minutes past midnight."""
        hours, minutes = hhmm.split(":")
        return int(hours) * 60 + int(minutes)

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
