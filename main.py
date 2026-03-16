from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(name="Jordan")

    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")

    mochi.add_task(Task(description="Morning walk",    time_of_day="07:00", frequency="daily"))
    mochi.add_task(Task(description="Breakfast feed",  time_of_day="07:30", frequency="daily"))
    mochi.add_task(Task(description="Evening walk",    time_of_day="18:00", frequency="daily"))

    luna.add_task(Task(description="Morning feed",     time_of_day="08:00", frequency="daily"))
    luna.add_task(Task(description="Brush coat",       time_of_day="20:00", frequency="weekly"))

    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler()
    daily_plan = scheduler.build_daily_plan(owner)

    print("=" * 40)
    print("       🐾  Today's Schedule  🐾")
    print("=" * 40)
    for task in daily_plan:
        status = "✅" if task.completed else "🔲"
        print(f"  {status}  {task.time_of_day}  |  {task.pet_name:<6}  |  {task.description}")
    print("=" * 40)
    print(f"  Total pending tasks: {len(daily_plan)}")
    print("=" * 40)


if __name__ == "__main__":
    main()

