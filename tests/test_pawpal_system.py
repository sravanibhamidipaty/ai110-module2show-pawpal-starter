from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def test_owner_aggregates_tasks_across_pets() -> None:
    owner = Owner(name="Jordan")
    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Luna", species="cat")

    dog.add_task(Task(description="Walk", time_of_day="08:00"))
    cat.add_task(Task(description="Feed", time_of_day="07:30"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    tasks = owner.all_tasks()
    assert len(tasks) == 2
    assert {task.pet_name for task in tasks} == {"Mochi", "Luna"}


def test_scheduler_organizes_by_time_and_pending_first() -> None:
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")

    done_task = Task(description="Morning meds", time_of_day="07:00", completed=True)
    pending_late = Task(description="Evening walk", time_of_day="18:00")
    pending_early = Task(description="Breakfast", time_of_day="06:30")

    pet.add_task(done_task)
    pet.add_task(pending_late)
    pet.add_task(pending_early)
    owner.add_pet(pet)

    scheduler = Scheduler()
    ordered = scheduler.organize_tasks(owner, include_completed=True)

    assert [task.description for task in ordered] == [
        "Breakfast",
        "Evening walk",
        "Morning meds",
    ]


def test_scheduler_invalid_time_sorts_last() -> None:
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")

    pet.add_task(Task(description="Bad time", time_of_day="abc"))
    pet.add_task(Task(description="Valid time", time_of_day="09:00"))
    owner.add_pet(pet)

    scheduler = Scheduler()
    ordered = scheduler.organize_tasks(owner, include_completed=True)

    assert [task.description for task in ordered] == ["Valid time", "Bad time"]


def test_scheduler_same_time_uses_stable_tie_breakers() -> None:
    owner = Owner(name="Jordan")
    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")

    mochi.add_task(Task(description="Brush", time_of_day="08:00"))
    luna.add_task(Task(description="Feed", time_of_day="08:00"))
    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler()
    ordered = scheduler.organize_tasks(owner, include_completed=True)

    assert [task.pet_name for task in ordered] == ["Luna", "Mochi"]
    assert [task.description for task in ordered] == ["Feed", "Brush"]


def test_scheduler_can_sort_without_pending_priority() -> None:
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")

    pet.add_task(Task(description="Completed early", time_of_day="07:00", completed=True))
    pet.add_task(Task(description="Pending later", time_of_day="08:00", completed=False))
    owner.add_pet(pet)

    scheduler = Scheduler()
    ordered = scheduler.organize_tasks(owner, include_completed=True, pending_first=False)

    assert [task.description for task in ordered] == ["Completed early", "Pending later"]


def test_scheduler_sort_by_time_orders_hhmm_values() -> None:
    scheduler = Scheduler()
    tasks = [
        Task(description="Later", time_of_day="18:00", pet_name="Mochi"),
        Task(description="Earlier", time_of_day="07:00", pet_name="Mochi"),
        Task(description="Middle", time_of_day="12:30", pet_name="Luna"),
    ]

    ordered = scheduler.sort_by_time(tasks)

    assert [task.description for task in ordered] == ["Earlier", "Middle", "Later"]


def test_scheduler_filter_tasks_by_pet_and_completion() -> None:
    owner = Owner(name="Jordan")
    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")

    mochi.add_task(Task(description="Walk", time_of_day="07:00"))
    luna.add_task(Task(description="Brush", time_of_day="20:00", completed=True))

    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler()

    mochi_only = scheduler.filter_tasks(owner, pet_name="Mochi", include_completed=True)
    done_only = scheduler.filter_tasks(owner, completed=True, include_completed=True)

    assert [task.description for task in mochi_only] == ["Walk"]
    assert [task.description for task in done_only] == ["Brush"]


def test_mark_task_completed_updates_status() -> None:
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(description="Brush coat", time_of_day="20:00"))
    owner.add_pet(pet)

    scheduler = Scheduler()
    updated = scheduler.mark_task_completed(owner, "Mochi", "Brush coat")

    assert updated is True
    assert pet.tasks[0].completed is True


def test_mark_task_completed_creates_next_daily_task() -> None:
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(description="Morning walk", time_of_day="07:00", frequency="daily"))
    owner.add_pet(pet)

    scheduler = Scheduler()
    updated = scheduler.mark_task_completed(
        owner,
        "Mochi",
        "Morning walk",
        on_date=date(2026, 3, 16),
    )

    assert updated is True
    assert len(pet.tasks) == 2
    assert pet.tasks[0].completed is True
    assert pet.tasks[1].description == "Morning walk"
    assert pet.tasks[1].completed is False
    assert pet.tasks[1].due_date == date(2026, 3, 17)


def test_mark_task_completed_creates_next_weekly_task() -> None:
    owner = Owner(name="Jordan")
    pet = Pet(name="Luna", species="cat")
    pet.add_task(Task(description="Brush coat", time_of_day="20:00", frequency="weekly"))
    owner.add_pet(pet)

    scheduler = Scheduler()
    updated = scheduler.mark_task_completed(
        owner,
        "Luna",
        "Brush coat",
        on_date=date(2026, 3, 16),
    )

    assert updated is True
    assert len(pet.tasks) == 2
    assert pet.tasks[1].due_date == date(2026, 3, 23)


def test_mark_task_completed_does_not_repeat_as_needed_task() -> None:
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(description="Nail trim", time_of_day="10:00", frequency="as needed"))
    owner.add_pet(pet)

    scheduler = Scheduler()
    updated = scheduler.mark_task_completed(
        owner,
        "Mochi",
        "Nail trim",
        on_date=date(2026, 3, 16),
    )

    assert updated is True
    assert len(pet.tasks) == 1
    assert pet.tasks[0].completed is True

