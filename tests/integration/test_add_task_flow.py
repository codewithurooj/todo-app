"""Integration tests for add task end-to-end workflows."""

import pytest
from io import StringIO
from unittest.mock import patch
from src.models.task import TaskList
from src.cli.task_cli import add_task_cli


class TestAddTaskFlow:
    """End-to-end integration tests for add task feature."""

    def test_add_task_title_only_flow(self) -> None:
        """Full workflow: Add task with title only."""
        tasklist = TaskList()

        # Simulate user input: title, then empty description
        with patch("builtins.input", side_effect=["Buy groceries", ""]):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                add_task_cli(tasklist)

        # Verify task was added
        tasks = tasklist.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Buy groceries"
        assert tasks[0].description is None

    def test_add_task_with_description_flow(self) -> None:
        """Full workflow: Add task with title and description."""
        tasklist = TaskList()

        # Simulate user input: title, description
        with patch("builtins.input", side_effect=["Meeting", "Discuss Q4 plans"]):
            with patch("sys.stdout", new=StringIO()):
                add_task_cli(tasklist)

        # Verify task was added with description
        tasks = tasklist.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Meeting"
        assert tasks[0].description == "Discuss Q4 plans"

    def test_add_task_cancel_flow(self) -> None:
        """User can cancel task creation."""
        tasklist = TaskList()

        # Simulate user input: cancel
        with patch("builtins.input", return_value="cancel"):
            with patch("sys.stdout", new=StringIO()):
                add_task_cli(tasklist)

        # Verify no task was added
        assert len(tasklist.get_all_tasks()) == 0

    def test_add_task_invalid_then_valid_title(self) -> None:
        """Invalid title rejected, user retries with valid title."""
        tasklist = TaskList()

        # Simulate: empty title, then valid title, then empty description
        with patch("builtins.input", side_effect=["", "Valid task", ""]):
            with patch("sys.stdout", new=StringIO()):
                add_task_cli(tasklist)

        # Verify task created with valid title
        tasks = tasklist.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Valid task"

    def test_add_multiple_tasks_sequential(self) -> None:
        """Multiple tasks can be added in sequence with unique IDs."""
        tasklist = TaskList()

        # Add first task (title, empty description)
        with patch("builtins.input", side_effect=["First task", ""]):
            with patch("sys.stdout", new=StringIO()):
                add_task_cli(tasklist)

        # Add second task (title, empty description)
        with patch("builtins.input", side_effect=["Second task", ""]):
            with patch("sys.stdout", new=StringIO()):
                add_task_cli(tasklist)

        # Verify both tasks added with different IDs
        tasks = tasklist.get_all_tasks()
        assert len(tasks) == 2
        assert tasks[0].id == 1
        assert tasks[1].id == 2

    def test_add_task_with_unicode_title(self) -> None:
        """Task with unicode characters (emoji, international) works."""
        tasklist = TaskList()

        # Unicode title with emoji and international chars
        unicode_title = "📝 Café meeting with François"
        with patch("builtins.input", side_effect=[unicode_title, ""]):
            with patch("sys.stdout", new=StringIO()):
                add_task_cli(tasklist)

        tasks = tasklist.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == unicode_title

    def test_add_task_whitespace_trimming(self) -> None:
        """Leading/trailing whitespace is trimmed from title."""
        tasklist = TaskList()

        with patch("builtins.input", side_effect=["  Whitespace task  ", ""]):
            with patch("sys.stdout", new=StringIO()):
                add_task_cli(tasklist)

        tasks = tasklist.get_all_tasks()
        assert tasks[0].title == "Whitespace task"

    def test_add_task_empty_description_becomes_none(self) -> None:
        """Empty description (just Enter) results in None."""
        tasklist = TaskList()

        # Title, then empty description
        with patch("builtins.input", side_effect=["Task", ""]):
            with patch("sys.stdout", new=StringIO()):
                add_task_cli(tasklist)

        tasks = tasklist.get_all_tasks()
        assert tasks[0].description is None
