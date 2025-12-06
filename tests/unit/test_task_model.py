"""Unit tests for Task and TaskList models."""

import pytest
from datetime import datetime
from src.models.task import Task, TaskList


class TestTask:
    """Tests for Task dataclass."""

    def test_create_task_with_title_only(self) -> None:
        """Task can be created with just a title."""
        task = Task(id=1, title="Buy groceries")
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description is None
        assert task.completed is False
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)

    def test_create_task_with_description(self) -> None:
        """Task can be created with title and description."""
        task = Task(id=2, title="Meeting", description="Discuss Q4 plans")
        assert task.id == 2
        assert task.title == "Meeting"
        assert task.description == "Discuss Q4 plans"

    def test_task_default_completed_false(self) -> None:
        """New tasks default to incomplete status."""
        task = Task(id=1, title="Test")
        assert task.completed is False

    def test_task_empty_title_raises_error(self) -> None:
        """Empty title raises ValueError."""
        with pytest.raises(ValueError, match="empty"):
            Task(id=1, title="")

    def test_task_whitespace_title_raises_error(self) -> None:
        """Whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="empty"):
            Task(id=1, title="   ")

    def test_task_invalid_id_raises_error(self) -> None:
        """ID less than 1 raises ValueError."""
        with pytest.raises(ValueError, match="positive"):
            Task(id=0, title="Test")


class TestTaskList:
    """Tests for TaskList class."""

    def test_tasklist_starts_empty(self) -> None:
        """New TaskList has no tasks."""
        tasklist = TaskList()
        assert len(tasklist.get_all_tasks()) == 0

    def test_add_task_with_title_only(self) -> None:
        """Can add task with just a title."""
        tasklist = TaskList()
        task = tasklist.add_task("Buy milk")

        assert task.id == 1
        assert task.title == "Buy milk"
        assert task.description is None
        assert len(tasklist.get_all_tasks()) == 1

    def test_add_task_with_description(self) -> None:
        """Can add task with title and description."""
        tasklist = TaskList()
        task = tasklist.add_task("Meeting", "Discuss project")

        assert task.id == 1
        assert task.title == "Meeting"
        assert task.description == "Discuss project"

    def test_task_id_auto_increment(self) -> None:
        """Task IDs auto-increment correctly."""
        tasklist = TaskList()
        task1 = tasklist.add_task("First")
        task2 = tasklist.add_task("Second")
        task3 = tasklist.add_task("Third")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_trims_whitespace(self) -> None:
        """Leading/trailing whitespace is trimmed from title."""
        tasklist = TaskList()
        task = tasklist.add_task("  Task with spaces  ")
        assert task.title == "Task with spaces"

    def test_add_task_empty_description_becomes_none(self) -> None:
        """Empty or whitespace-only description becomes None."""
        tasklist = TaskList()
        task1 = tasklist.add_task("Task", "")
        task2 = tasklist.add_task("Task2", "   ")

        assert task1.description is None
        assert task2.description is None

    def test_get_all_tasks_returns_list(self) -> None:
        """get_all_tasks returns list of tasks."""
        tasklist = TaskList()
        tasklist.add_task("Task 1")
        tasklist.add_task("Task 2")

        tasks = tasklist.get_all_tasks()
        assert isinstance(tasks, list)
        assert len(tasks) == 2

    def test_find_by_id_existing_task(self) -> None:
        """find_by_id returns task when ID exists."""
        tasklist = TaskList()
        task = tasklist.add_task("Find me")

        found = tasklist.find_by_id(task.id)
        assert found is not None
        assert found.id == task.id
        assert found.title == "Find me"

    def test_find_by_id_nonexistent_task(self) -> None:
        """find_by_id returns None when ID doesn't exist."""
        tasklist = TaskList()
        tasklist.add_task("Task")

        found = tasklist.find_by_id(999)
        assert found is None
