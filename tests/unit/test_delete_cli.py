"""Unit tests for delete task CLI handler."""

import pytest
from io import StringIO
from src.models.task import TaskList
from src.cli.task_cli import delete_task_cli


class TestDeleteCLI:
    """Tests for delete_task_cli function."""

    # T004: CLI delete handler with valid ID
    def test_delete_cli_with_valid_id(self, monkeypatch, capsys) -> None:
        """Valid ID input shows success message."""
        tasklist = TaskList()
        task = tasklist.add_task("Task to delete", "Description")

        # Mock user input: task ID, then confirmation 'y'
        inputs = iter([str(task.id), "y"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        delete_task_cli(tasklist)

        captured = capsys.readouterr()
        assert "deleted successfully" in captured.out.lower()
        assert str(task.id) in captured.out
        assert len(tasklist.get_all_tasks()) == 0

    # T004: CLI delete handler displays task title
    def test_delete_success_message_includes_task_details(self, monkeypatch, capsys) -> None:
        """Success message shows task ID and title."""
        tasklist = TaskList()
        task = tasklist.add_task("Meeting with team")

        inputs = iter([str(task.id), "y"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        delete_task_cli(tasklist)

        captured = capsys.readouterr()
        assert f"#{task.id}" in captured.out
        assert "Meeting with team" in captured.out or "meeting" in captured.out.lower()
