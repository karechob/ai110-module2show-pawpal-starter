"""PawPal demo script."""

from datetime import date

from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    # 1. Create an owner with a daily time budget.
    owner = Owner(name="Miranda", minutes_available=90)

    # 2. Create at least two pets and add them to the owner.
    rex = Pet(name="Rex", species="dog", age=3)
    milo = Pet(name="Milo", species="cat", age=5)
    owner.add_pet(rex)
    owner.add_pet(milo)

    # 3. Add tasks *out of order* (times are not chronological) with different
    #    durations, so the sorting logic has something real to fix.
    today = date.today()
    rex.add_task(Task("Dinner", "feeding", duration=10, priority=4, time="18:00",
                      due_date=today))
    rex.add_task(Task("Morning walk", "walk", duration=30, priority=5, time="08:00",
                      frequency="daily", due_date=today))
    rex.add_task(Task("Fetch training", "enrichment", duration=20, priority=2,
                      time="12:15", frequency="weekly", due_date=today))
    milo.add_task(Task("Laser play", "enrichment", duration=45, priority=1,
                       time="19:30", due_date=today))
    milo.add_task(Task("Give medication", "meds", duration=5, priority=5,
                       time="08:15", frequency="daily", due_date=today))
    # Two tasks booked for the SAME time (08:00) on different pets — the
    # scheduler should warn that Miranda can't be in two places at once.
    milo.add_task(Task("Breakfast", "feeding", duration=10, priority=4,
                       time="08:00", due_date=today))

    scheduler = Scheduler()
    # Build the pet index up front so filtering by pet works before planning.
    scheduler.index_pets(owner)

    # 4. Sorting: show every task ordered chronologically by its "HH:MM" time.
    print("=" * 40)
    print(f"All tasks for {owner.name}, sorted by time")
    print("=" * 40)
    for t in scheduler.sort_by_time(owner.all_tasks()):
        repeats = " (recurring)" if t.recurring else ""
        print(f"  {t.time}  [{scheduler.pet_by_task[t.id]}] {t.name}"
              f" — {t.duration} min{repeats}")

    # 5. Conflict detection: print a warning for any overlapping tasks
    #    (same pet or different pets) without crashing the program.
    print("\nTime conflicts:")
    warnings = scheduler.conflict_warnings(owner.all_tasks())
    if warnings:
        for warning in warnings:
            print(f"  {warning}")
    else:
        print("  none 🎉")

    # 6. Recurring tasks: completing Milo's daily meds auto-creates tomorrow's.
    meds = milo.tasks[1]
    next_meds = milo.mark_task_complete(meds.id)
    scheduler.index_pets(owner)  # re-index so the new task is labelled
    print(f"\nCompleted '{meds.name}' (due {meds.due_date}).")
    if next_meds is not None:
        print(f"  → auto-scheduled next '{next_meds.name}' for {next_meds.due_date}")

    # 7. Filtering: only Rex's tasks, and only tasks still to be done.
    print("\nRex's tasks only:")
    for t in scheduler.filter_tasks(owner.all_tasks(), pet_name="Rex"):
        print(f"  • {t.name} ({t.category})")
    print("\nStill to do (not completed) across all pets:")
    for t in scheduler.filter_tasks(owner.all_tasks(), completed=False):
        print(f"  • [{scheduler.pet_by_task[t.id]}] {t.name}")

    # 8. Generate and print today's schedule.
    scheduler.generate_plan(owner)
    print("\n" + "=" * 40)
    print(f"Today's Schedule for {owner.name}")
    print(f"Time available: {owner.minutes_available} minutes")
    print("=" * 40)
    print(scheduler.explain())


if __name__ == "__main__":
    main()
