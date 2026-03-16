from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Activity:
    activity_type: str
    duration_minutes: int
    priority: str
    earliest_start_time: str
    latest_start_time: str

    def is_within_window(self, start_time: str) -> bool:
        pass


@dataclass
class Pet:
    name: str
    species: str
    special_needs: str
    preferences: str
    activities: list[Activity] = field(default_factory=list)

    def add_activity(self, activity: Activity) -> None:
        pass

    def get_daily_activities(self) -> list[Activity]:
        pass


@dataclass
class Schedule:
    entries: list[tuple[Activity, str]] = field(default_factory=list)

    def add_entry(self, activity: Activity, start_time: str) -> None:
        pass

    def has_conflicts(self) -> bool:
        pass

    def to_ordered_list(self) -> list[tuple[Activity, str]]:
        pass


@dataclass
class Scheduler:
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def generate_daily_schedule(self) -> Schedule:
        pass

    def resolve_conflicts(self, schedule: Schedule) -> Schedule:
        pass

