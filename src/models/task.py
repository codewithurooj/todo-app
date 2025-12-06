"""Task data models for the todo application.

This module defines the core Task and TaskList classes for managing tasks in memory.
Phase I implementation uses in-memory storage with no persistence.
"""

from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Optional


@dataclass
class Task:
    """Represents a single todo task.

    Attributes:
        id: Unique identifier (auto-assigned by TaskList)
        title: Task summary/title (required, max 200 chars)
        description: Detailed description (optional, max 1000 chars)
        completed: Completion status (default False)
        created_at: Timestamp when task was created (UTC)
        updated_at: Timestamp when task was last modified (UTC)
    """

    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        """Validate task data after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")
        if self.id < 1:
            raise ValueError("Task ID must be a positive integer")


class TaskList:
    """Manages a collection of tasks with in-memory storage.

    This class handles task creation, storage, and retrieval using Python lists.
    Phase I: No file persistence - data lost on exit.

    Attributes:
        _tasks: Internal list storing Task objects
        _next_id: Counter for auto-incrementing task IDs
    """

    def __init__(self) -> None:
        """Initialize empty task list."""
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add_task(
        self, title: str, description: Optional[str] = None
    ) -> Task:
        """Create and add a new task to the list.

        Args:
            title: Task title (required)
            description: Task description (optional)

        Returns:
            The newly created Task object with assigned ID and timestamps

        Raises:
            ValueError: If title is empty or invalid
        """
        # Create new task with auto-incremented ID
        task = Task(
            id=self._next_id,
            title=title.strip(),
            description=description.strip() if description and description.strip() else None,
        )

        # Add to list and increment counter
        self._tasks.append(task)
        self._next_id += 1

        return task

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks.

        Returns:
            List of all Task objects (returns reference, not copy)
        """
        return self._tasks

    def find_by_id(self, task_id: int) -> Optional[Task]:
        """Find a task by its ID.

        Args:
            task_id: Unique task identifier

        Returns:
            Task object if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None
