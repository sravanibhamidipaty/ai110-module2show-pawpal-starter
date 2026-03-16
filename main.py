from pawpal_system import Owner, Pet, Scheduler, Task


def _print_tasks(title: str, tasks: list[Task]) -> None:
    print("=" * 50)
    print(title)
    print("=" * 50)
    for task in tasks:
        status = "done" if task.completed else "todo"
        print(f"{task.time_of_day:<5} | {task.pet_name:<6} | {status:<4} | {task.description}")
    if not tasks:
        print("(no tasks)")
    print()


def main() -> None:
    owner = Owner(name="Jordan")

    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")

    # Intentionally add tasks out of order to test sorting.
    mochi.add_task(Task(description="Evening walk", time_of_day="18:00", frequency="daily"))
    mochi.add_task(Task(description="Morning walk", time_of_day="07:00", frequency="daily"))
    mochi.add_task(Task(description="Breakfast feed", time_of_day="07:30", frequency="daily"))

    luna.add_task(Task(description="Brush coat", time_of_day="20:00", frequency="weekly"))
    luna.add_task(Task(description="Morning feed", time_of_day="08:00", frequency="daily"))

    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler()

    # Mark one task complete to test completion filtering.
    scheduler.mark_task_completed(owner, "Luna", "Brush coat")

    all_tasks_unsorted = scheduler.retrieve_all_tasks(owner, include_completed=True)
    sorted_by_time = scheduler.sort_by_time(all_tasks_unsorted)
    mochi_tasks = scheduler.filter_tasks(owner, pet_name="Mochi", include_completed=True)
    completed_tasks = scheduler.filter_tasks(owner, completed=True, include_completed=True)

    _print_tasks("All Tasks Sorted by Time", sorted_by_time)
    _print_tasks("Filtered: Mochi Tasks", scheduler.sort_by_time(mochi_tasks))
    _print_tasks("Filtered: Completed Tasks", scheduler.sort_by_time(completed_tasks))


if __name__ == "__main__":
    main()
