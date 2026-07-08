from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List

@dataclass
class Task:
    """Represents a single pet care task."""
    description: str
    due_time: str
    frequency: str
    priority: str
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self):
        """Marks the task as complete and reschedules if recurring."""
        self.completed = True
        if self.frequency == "daily":
            return Task(
                description=self.description,
                due_time=self.due_time,
                frequency=self.frequency,
                priority=self.priority,
                due_date=self.due_date + timedelta(days=1)
            )
        elif self.frequency == "weekly":
            return Task(
                description=self.description,
                due_time=self.due_time,
                frequency=self.frequency,
                priority=self.priority,
                due_date=self.due_date + timedelta(weeks=1)
            )
        return None


@dataclass
class Pet:
    """Represents a pet with its care tasks."""
    name: str
    species: str
    breed: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Adds a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task):
        """Removes a task from this pet's task list."""
        self.tasks.remove(task)

    def get_tasks(self):
        """Returns all tasks for this pet."""
        return self.tasks

    def get_pending_tasks(self):
        """Returns only incomplete tasks."""
        return [t for t in self.tasks if not t.completed]


@dataclass
class Owner:
    """Represents a pet owner managing multiple pets."""
    name: str
    email: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Adds a pet to the owner's list."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet):
        """Removes a pet from the owner's list."""
        self.pets.remove(pet)

    def get_all_tasks(self):
        """Returns all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            for task in pet.get_tasks():
                all_tasks.append((pet.name, task))
        return all_tasks

    def get_pet_names(self):
        """Returns list of all pet names."""
        return [pet.name for pet in self.pets]


class Scheduler:
    """The brain that organizes and manages tasks across all pets."""

    def __init__(self, owner: Owner):
        """Initializes the Scheduler with an Owner."""
        self.owner = owner

    def get_all_tasks(self):
        """Retrieves all tasks from all pets."""
        return self.owner.get_all_tasks()

    def sort_by_time(self):
        """Sorts all tasks by due time across all pets."""
        all_tasks = self.get_all_tasks()
        return sorted(all_tasks, key=lambda x: x[1].due_time)

    def sort_by_priority(self):
        """Sorts tasks by priority: high > medium > low, then by time."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        all_tasks = self.get_all_tasks()
        return sorted(all_tasks, key=lambda x: (
            priority_order.get(x[1].priority, 3), x[1].due_time
        ))

    def filter_by_pet(self, pet_name: str):
        """Filters tasks to show only a specific pet's tasks."""
        return [(name, task) for name, task in self.get_all_tasks()
                if name == pet_name]

    def filter_by_status(self, completed: bool = False):
        """Filters tasks by completion status."""
        return [(name, task) for name, task in self.get_all_tasks()
                if task.completed == completed]

    def detect_conflicts(self):
        """Detects tasks scheduled at the same time across all pets."""
        all_tasks = self.get_all_tasks()
        time_map = {}
        conflicts = []
        for pet_name, task in all_tasks:
            if task.due_time in time_map:
                conflicts.append((
                    task.due_time,
                    time_map[task.due_time],
                    (pet_name, task)
                ))
            else:
                time_map[task.due_time] = (pet_name, task)
        return conflicts

    def mark_task_complete(self, pet_name: str, task: Task):
        """Marks a task complete and handles recurring rescheduling."""
        new_task = task.mark_complete()
        if new_task:
            for pet in self.owner.pets:
                if pet.name == pet_name:
                    pet.add_task(new_task)
        return new_task

    def generate_daily_plan(self):
        """Generates a sorted daily plan with conflict warnings."""
        sorted_tasks = self.sort_by_time()
        conflicts = self.detect_conflicts()
        conflict_times = [c[0] for c in conflicts]
        plan = []
        for pet_name, task in sorted_tasks:
            status = "⚠️ CONFLICT" if task.due_time in conflict_times else ""
            plan.append({
                "time": task.due_time,
                "pet": pet_name,
                "task": task.description,
                "priority": task.priority,
                "completed": task.completed,
                "conflict": status
            })
        return plan