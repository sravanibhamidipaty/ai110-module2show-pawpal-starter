from pawpal_system import Pet, Task


def test_mark_complete_changes_task_status() -> None:
    task = Task(description="Morning walk", time_of_day="07:00")

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count() -> None:
    pet = Pet(name="Mochi", species="dog")

    assert len(pet.tasks) == 0

    pet.add_task(Task(description="Breakfast feed", time_of_day="07:30"))

    assert len(pet.tasks) == 1

    pet.add_task(Task(description="Evening walk", time_of_day="18:00"))

    assert len(pet.tasks) == 2

