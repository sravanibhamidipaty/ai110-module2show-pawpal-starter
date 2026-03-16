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


def test_mark_task_completed_updates_status() -> None:
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(description="Brush coat", time_of_day="20:00"))
    owner.add_pet(pet)

    scheduler = Scheduler()
    updated = scheduler.mark_task_completed(owner, "Mochi", "Brush coat")

    assert updated is True
    assert pet.tasks[0].completed is True

