from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


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


def test_sorting_returns_tasks_in_chronological_order() -> None:
    scheduler = Scheduler()
    tasks = [
        Task(description="Dinner", time_of_day="18:00", pet_name="Mochi"),
        Task(description="Breakfast", time_of_day="07:30", pet_name="Mochi"),
        Task(description="Lunch", time_of_day="12:00", pet_name="Luna"),
    ]

    ordered = scheduler.sort_by_time(tasks)

    assert [task.description for task in ordered] == ["Breakfast", "Lunch", "Dinner"]


def test_daily_completion_creates_next_day_task() -> None:
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(description="Morning walk", time_of_day="07:00", frequency="daily"))
    owner.add_pet(pet)

    scheduler = Scheduler()
    updated = scheduler.mark_task_completed(owner, "Mochi", "Morning walk", on_date=date(2026, 3, 16))

    assert updated is True
    assert len(pet.tasks) == 2
    assert pet.tasks[0].completed is True
    assert pet.tasks[1].completed is False
    assert pet.tasks[1].due_date == date(2026, 3, 17)


def test_conflict_detection_flags_duplicate_times() -> None:
    scheduler = Scheduler()
    tasks = [
        Task(description="Walk", time_of_day="08:00", pet_name="Mochi"),
        Task(description="Feed", time_of_day="08:00", pet_name="Luna"),
        Task(description="Brush", time_of_day="09:00", pet_name="Luna"),
    ]

    conflicts = scheduler.detect_conflicts(tasks)

    assert len(conflicts) == 1
    first, second = conflicts[0]
    assert {first.description, second.description} == {"Walk", "Feed"}


def test_conflict_detection_with_no_tasks_returns_empty_list() -> None:
    scheduler = Scheduler()

    assert scheduler.detect_conflicts([]) == []
