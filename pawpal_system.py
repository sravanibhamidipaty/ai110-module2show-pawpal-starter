from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time


@dataclass
class Task:
    """Represents one care activity for a pet."""

    description: str
    time_of_day: str
    frequency: str = "daily"
    completed: bool = False
    pet_name: str | None = None

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Reset this task to incomplete/pending status."""
        self.completed = False


@dataclass
class Pet:
    """Stores pet details and a task list."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's task list, auto-assigning pet_name if unset."""
        if task.pet_name is None:
            task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, description: str) -> bool:
        """Remove the first task matching the given description; return True if removed."""
        for index, task in enumerate(self.tasks):
            if task.description == description:
                del self.tasks[index]
                return True
        return False

    def get_tasks(self, include_completed: bool = True) -> list[Task]:
        """Return this pet's tasks, optionally filtering out completed ones."""
        if include_completed:
            return list(self.tasks)
        return [task for task in self.tasks if not task.completed]


@dataclass
class Owner:
    """Manages multiple pets and provides aggregate task access."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a new pet under this owner."""
        self.pets.append(pet)

    def get_pet(self, pet_name: str) -> Pet | None:
        """Return the pet with the given name, or None if not found."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet
        return None

    def remove_pet(self, pet_name: str) -> bool:
        """Remove the pet with the given name; return True if removed."""
        for index, pet in enumerate(self.pets):
            if pet.name == pet_name:
                del self.pets[index]
                return True
        return False

    def all_tasks(self, include_completed: bool = True) -> list[Task]:
        """Aggregate and return tasks from all pets, with optional completed filter."""
        tasks: list[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks(include_completed=include_completed))
        return tasks


@dataclass
class Scheduler:
    """Retrieves, organizes, and manages tasks across an owner's pets."""

    def retrieve_all_tasks(self, owner: Owner, include_completed: bool = False) -> list[Task]:
        """Fetch every task across all of the owner's pets."""
        return owner.all_tasks(include_completed=include_completed)

    def organize_tasks(
        self,
        owner: Owner,
        include_completed: bool = False,
    ) -> list[Task]:
        """Return tasks sorted chronologically with pending tasks before completed ones."""
        tasks = self.retrieve_all_tasks(owner, include_completed=include_completed)
        return sorted(tasks, key=self._task_sort_key)

    def build_daily_plan(self, owner: Owner) -> list[Task]:
        """Generate an ordered list of all pending tasks for today across every pet."""
        return self.organize_tasks(owner, include_completed=False)

    def mark_task_completed(self, owner: Owner, pet_name: str, description: str) -> bool:
        """Find a task by pet name and description, mark it complete, and return success."""
        pet = owner.get_pet(pet_name)
        if pet is None:
            return False

        for task in pet.tasks:
            if task.description == description:
                task.mark_complete()
                return True
        return False

    @staticmethod
    def _task_sort_key(task: Task) -> tuple[int, int, str, str]:
        """Produce a sort key: pending before completed, then by time, pet, and description."""
        parsed_time = Scheduler._parse_time(task.time_of_day)
        return (
            1 if task.completed else 0,
            parsed_time.hour * 60 + parsed_time.minute,
            task.pet_name or "",
            task.description,
        )

    @staticmethod
    def _parse_time(value: str) -> time:
        """Parse an HH:MM string to a time object; defaults to 23:59 for unrecognised values."""
        try:
            hour, minute = value.split(":", maxsplit=1)
            return time(hour=int(hour), minute=int(minute))
        except (ValueError, TypeError):
            return time(23, 59)
