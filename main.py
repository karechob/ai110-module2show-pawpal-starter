"""PawPal demo script."""

from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    # 1. Create an owner with a daily time budget.
    owner = Owner(name="Miranda", minutes_available=90)

    # 2. Create at least two pets and add them to the owner.
    rex = Pet(name="Rex", species="dog", age=3)
    milo = Pet(name="Milo", species="cat", age=5)
    owner.add_pet(rex)
    owner.add_pet(milo)

    # 3. Add at least three tasks with different durations to the pets.
    rex.add_task(Task("Morning walk", "walk", duration=30, priority=5))
    rex.add_task(Task("Fetch training", "enrichment", duration=20, priority=2))
    rex.add_task(Task("Dinner", "feeding", duration=10, priority=4))
    milo.add_task(Task("Give medication", "meds", duration=5, priority=5))
    milo.add_task(Task("Laser play", "enrichment", duration=45, priority=1))

    # 4. Generate and print today's schedule.
    scheduler = Scheduler()
    scheduler.generate_plan(owner)

    print("=" * 40)
    print(f"Today's Schedule for {owner.name}")
    print(f"Time available: {owner.minutes_available} minutes")
    print("=" * 40)
    print(scheduler.explain())


if __name__ == "__main__":
    main()
