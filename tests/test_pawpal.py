from datetime import date, timedelta

from pawpal_system import Pet, Scheduler, Task


def test_task_completion():
    """Calling mark_done() flips the task's status to completed."""
    task = Task("Morning walk", "walk", duration=30, priority=5)
    assert task.completed is False

    task.mark_done()

    assert task.completed is True


def test_task_addition():
    """Adding a task to a Pet increases that pet's task count."""
    pet = Pet(name="Rex", species="dog", age=3)
    assert len(pet.tasks) == 0

    pet.add_task(Task("Dinner", "feeding", duration=10, priority=4))

    assert len(pet.tasks) == 1


def test_sort_by_time_is_chronological():
    """Scheduler.sort_by_time returns tasks in ascending time-of-day order."""
    scheduler = Scheduler()

    # Deliberately create tasks out of order so sorting has work to do.
    noon = Task("Lunch walk", "walk", duration=20, priority=3, time="12:00")
    morning = Task("Breakfast", "feeding", duration=10, priority=5, time="08:00")
    evening = Task("Meds", "meds", duration=5, priority=4, time="18:30")

    ordered = scheduler.sort_by_time([noon, evening, morning])

    # The times should now read earliest-to-latest.
    assert [t.time for t in ordered] == ["08:00", "12:00", "18:30"]


def test_completing_daily_task_creates_next_days_occurrence():
    """Marking a daily task done rolls the routine forward one day.

    A daily task should spawn a fresh, uncompleted copy due the following day
    and add it to the pet automatically.
    """
    pet = Pet(name="Rex", species="dog", age=3)
    today = date.today()
    walk = Task(
        "Morning walk",
        "walk",
        duration=30,
        priority=5,
        time="08:00",
        frequency="daily",
        due_date=today,
    )
    pet.add_task(walk)

    upcoming = pet.mark_task_complete(walk.id)

    # The original is completed; a brand-new task now exists for tomorrow.
    assert walk.completed is True
    assert upcoming is not None
    assert upcoming.completed is False
    assert upcoming.due_date == today + timedelta(days=1)
    assert upcoming.id != walk.id
    assert len(pet.tasks) == 2  # original + next occurrence


def test_detect_conflicts_flags_duplicate_times():
    """Scheduler flags two tasks scheduled at the same time on the same day."""
    scheduler = Scheduler()
    today = date.today()

    # Two tasks demanding attention at exactly 08:00 — an unavoidable clash.
    feeding = Task(
        "Feed", "feeding", duration=15, priority=5, time="08:00", due_date=today
    )
    walk = Task(
        "Walk", "walk", duration=30, priority=4, time="08:00", due_date=today
    )

    conflicts = scheduler.detect_conflicts([feeding, walk])

    assert len(conflicts) == 1  # exactly one overlapping pair detected
    pair = conflicts[0]
    assert feeding in pair and walk in pair
