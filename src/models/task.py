"""Task data models for the todo application.

This module defines the core Task and TaskList classes for managing tasks in memory.
Phase I implementation uses in-memory storage with no persistence.
"""

from dataclasses import dataclass, field
from datetime import UTC, datetime


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
    description: str | None = None
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

    def add_task(self, title: str, description: str | None = None) -> Task:
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

    def find_by_id(self, task_id: int) -> Task | None:
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

    def delete_task(self, task_id: int) -> tuple[bool, str]:
        """Delete a task by ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            Tuple of (success: bool, message: str)
            - (True, success_message) if task was deleted
            - (False, error_message) if task not found

        Side Effects:
            - Removes task from _tasks list
            - Does NOT decrement _next_id
            - Reduces list size by 1

        Guarantees:
            - Remaining tasks preserve their IDs
            - Remaining tasks maintain original order
            - Deleted ID is never reused
        """
        # Find the task first to get its title for the success message
        task = self.find_by_id(task_id)

        if not task:
            return False, f"Error: Task #{task_id} not found. Please enter a valid task ID."

        # Remove task using list comprehension (preserves order and IDs)
        self._tasks = [t for t in self._tasks if t.id != task_id]

        return True, f"Task #{task_id} '{task.title}' deleted successfully"

    def update_task_title(self, task_id: int, new_title: str) -> tuple[bool, str]:
        """Update a task's title.

        Args:
            task_id: The ID of the task to update
            new_title: The new title (will be stripped of whitespace)

        Returns:
            Tuple of (success: bool, message: str)
            - (True, success_message) if task was updated
            - (False, error_message) if task not found

        Side Effects:
            - Updates task title
            - Updates task updated_at timestamp
            - Preserves all other fields (ID, description, completed, created_at)
        """
        task = self.find_by_id(task_id)

        if not task:
            return False, f"Error: Task #{task_id} not found. Please enter a valid task ID."

        # Update title and timestamp
        task.title = new_title.strip()
        task.updated_at = datetime.now(UTC)

        return True, f"Task #{task_id} title updated successfully"

    def update_task_description(self, task_id: int, new_description: str | None) -> tuple[bool, str]:
        """Update a task's description.

        Args:
            task_id: The ID of the task to update
            new_description: The new description (will be stripped, None if empty)

        Returns:
            Tuple of (success: bool, message: str)
            - (True, success_message) if task was updated
            - (False, error_message) if task not found

        Side Effects:
            - Updates task description
            - Updates task updated_at timestamp
            - Preserves all other fields (ID, title, completed, created_at)
        """
        task = self.find_by_id(task_id)

        if not task:
            return False, f"Error: Task #{task_id} not found. Please enter a valid task ID."

        # Update description and timestamp
        if new_description and new_description.strip():
            task.description = new_description.strip()
        else:
            task.description = None

        task.updated_at = datetime.now(UTC)

        return True, f"Task #{task_id} description updated successfully"

    def update_task_status(self, task_id: int, completed: bool) -> tuple[bool, str]:
        """Update a task's completion status.

        Args:
            task_id: The ID of the task to update
            completed: The new completion status (True = complete, False = incomplete)

        Returns:
            Tuple of (success: bool, message: str)
            - (True, success_message) if task was updated
            - (False, error_message) if task not found

        Side Effects:
            - Updates task completed status
            - Updates task updated_at timestamp
            - Preserves all other fields (ID, title, description, created_at)
        """
        task = self.find_by_id(task_id)

        if not task:
            return False, f"Error: Task #{task_id} not found. Please enter a valid task ID."

        # Update status and timestamp
        task.completed = completed
        task.updated_at = datetime.now(UTC)

        status_msg = "complete" if completed else "incomplete"
        return True, f"Task #{task_id} marked as {status_msg}"

    def get_task_by_id(self, task_id: int) -> Task | None:
        """Get a task by its ID (alias for find_by_id for view feature).

        Args:
            task_id: Unique task identifier

        Returns:
            Task object if found, None otherwise
        """
        return self.find_by_id(task_id)

    def filter_tasks_by_status(self, completed: bool) -> list[Task]:
        """Filter tasks by completion status.

        Args:
            completed: True to get completed tasks, False for pending tasks

        Returns:
            List of Task objects matching the completion status

        Example:
            >>> tasklist.filter_tasks_by_status(completed=True)
            [Task(id=2, completed=True), Task(id=5, completed=True)]
            >>> tasklist.filter_tasks_by_status(completed=False)
            [Task(id=1, completed=False), Task(id=3, completed=False)]
        """
        return [task for task in self._tasks if task.completed == completed]

    def mark_complete(self, task_id: int) -> tuple[bool, str]:
        """Mark a pending task as complete.

        Args:
            task_id: Unique identifier of task to mark complete

        Returns:
            Tuple[bool, str]: (success, message)
                - (True, confirmation_msg) on success
                - (True, warning_msg) if already completed (idempotent)
                - (False, error_msg) if task not found

        Side Effects:
            On success:
            - Sets task.completed = True
            - Updates task.updated_at = datetime.now(UTC)
            - Preserves all other task fields
        """
        task = self.find_by_id(task_id)

        if task is None:
            return False, f"Error: Task with ID {task_id} not found"

        if task.completed:
            # Idempotent: Already completed, but not an error
            return True, f"Task {task_id} is already completed"

        # Atomic update
        task.completed = True
        task.updated_at = datetime.now(UTC)

        return True, f"✓ Task {task_id} marked as complete"

    def unmark_complete(self, task_id: int) -> tuple[bool, str]:
        """Reopen a completed task (change status to pending).

        Args:
            task_id: Unique identifier of task to reopen

        Returns:
            Tuple[bool, str]: (success, message)
                - (True, confirmation_msg) on success
                - (True, warning_msg) if already pending (idempotent)
                - (False, error_msg) if task not found

        Side Effects:
            On success:
            - Sets task.completed = False
            - Updates task.updated_at = datetime.now(UTC)
            - Preserves all other task fields
        """
        task = self.find_by_id(task_id)

        if task is None:
            return False, f"Error: Task with ID {task_id} not found"

        if not task.completed:
            # Idempotent: Already pending, but not an error
            return True, f"Task {task_id} is already pending"

        # Atomic update
        task.completed = False
        task.updated_at = datetime.now(UTC)

        return True, f"✓ Task {task_id} reopened (marked as pending)"
