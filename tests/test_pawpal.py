from pawpal_system import Pet, Task


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
