from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time, timedelta


@dataclass
class Task:
    """Represents one care activity for a pet."""

    description: str
    time_of_day: str
    frequency: str = "daily"
    completed: bool = False
    pet_name: str | None = None
    due_date: date | None = None

    def mark_complete(self) -> None:
        self.completed = True

    def mark_incomplete(self) -> None:
        self.completed = False


@dataclass
class Pet:
    """Stores pet details and a task list."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        if task.pet_name is None:
            task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, description: str) -> bool:
        for index, task in enumerate(self.tasks):
            if task.description == description:
                del self.tasks[index]
                return True
        return False

    def get_tasks(self, include_completed: bool = True) -> list[Task]:
        if include_completed:
            return list(self.tasks)
        return [task for task in self.tasks if not task.completed]


@dataclass
class Owner:
    """Manages multiple pets and provides aggregate task access."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_pet(self, pet_name: str) -> Pet | None:
        for pet in self.pets:
            if pet.name == pet_name:
                return pet
        return None

    def remove_pet(self, pet_name: str) -> bool:
        for index, pet in enumerate(self.pets):
            if pet.name == pet_name:
                del self.pets[index]
                return True
        return False

    def all_tasks(self, include_completed: bool = True) -> list[Task]:
        tasks: list[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks(include_completed=include_completed))
        return tasks


@dataclass
class Scheduler:
    """Retrieves, organizes, and manages tasks across an owner's pets."""

    def retrieve_all_tasks(self, owner: Owner, include_completed: bool = False) -> list[Task]:
        return owner.all_tasks(include_completed=include_completed)

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by HH:MM time. Invalid times are placed last."""
        return sorted(
            tasks,
            key=lambda task: (
                self._minutes_from_time(task.time_of_day),
                task.pet_name or "",
                task.description,
            ),
        )

    def filter_tasks(
        self,
        owner: Owner,
        completed: bool | None = None,
        pet_name: str | None = None,
        include_completed: bool = True,
    ) -> list[Task]:
        """Filter tasks by completion status and/or pet name."""
        tasks = self.retrieve_all_tasks(owner, include_completed=include_completed)

        if completed is not None:
            tasks = [task for task in tasks if task.completed is completed]
        if pet_name is not None:
            tasks = [task for task in tasks if task.pet_name == pet_name]

        return tasks

    def sort_tasks(self, tasks: list[Task], pending_first: bool = True) -> list[Task]:
        tasks_by_time = self.sort_by_time(tasks)
        if not pending_first:
            return tasks_by_time

        pending = [task for task in tasks_by_time if not task.completed]
        completed = [task for task in tasks_by_time if task.completed]
        return pending + completed

    def organize_tasks(
        self,
        owner: Owner,
        include_completed: bool = False,
        pending_first: bool = True,
    ) -> list[Task]:
        tasks = self.retrieve_all_tasks(owner, include_completed=include_completed)
        return self.sort_tasks(tasks, pending_first=pending_first)

    def build_daily_plan(self, owner: Owner) -> list[Task]:
        return self.organize_tasks(owner, include_completed=False)

    def mark_task_completed(
        self,
        owner: Owner,
        pet_name: str,
        description: str,
        on_date: date | None = None,
    ) -> bool:
        pet = owner.get_pet(pet_name)
        if pet is None:
            return False

        completion_date = on_date or date.today()

        for task in pet.tasks:
            if task.description == description and not task.completed:
                task.mark_complete()
                self._create_next_recurring_task(pet, task, completion_date)
                return True
        return False

    @staticmethod
    def _create_next_recurring_task(pet: Pet, completed_task: Task, completion_date: date) -> None:
        frequency = completed_task.frequency.strip().lower()

        if frequency == "daily":
            next_due_date = completion_date + timedelta(days=1)
        elif frequency == "weekly":
            next_due_date = completion_date + timedelta(days=7)
        else:
            return

        pet.add_task(
            Task(
                description=completed_task.description,
                time_of_day=completed_task.time_of_day,
                frequency=completed_task.frequency,
                completed=False,
                pet_name=completed_task.pet_name,
                due_date=next_due_date,
            )
        )

    @staticmethod
    def _task_sort_key(task: Task, pending_first: bool = True) -> tuple[int, int, str, str]:
        parsed_time = Scheduler._parse_time(task.time_of_day)
        minutes = 23 * 60 + 59 if parsed_time is None else parsed_time.hour * 60 + parsed_time.minute
        completion_rank = 1 if pending_first and task.completed else 0
        return (
            completion_rank,
            minutes,
            task.pet_name or "",
            task.description,
        )

    @staticmethod
    def _parse_time(value: str) -> time | None:
        """Parse HH:MM. Returns None for invalid values so caller can decide fallback behavior."""
        try:
            hour, minute = value.split(":", maxsplit=1)
            return time(hour=int(hour), minute=int(minute))
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _minutes_from_time(value: str) -> int:
        parsed_time = Scheduler._parse_time(value)
        if parsed_time is None:
            return 23 * 60 + 59
        return parsed_time.hour * 60 + parsed_time.minute
