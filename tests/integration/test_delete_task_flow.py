"""Integration tests for delete task end-to-end flows."""

import pytest
from src.models.task import TaskList


class TestDeleteTaskIntegration:
    """End-to-end integration tests for delete task feature."""

    # T018: Full delete flow
    def test_full_delete_flow_end_to_end(self) -> None:
        """Add task → Delete → Verify removed."""
        # Arrange: Create tasklist and add tasks
        tasklist = TaskList()
        task1 = tasklist.add_task("Task 1", "Description 1")
        task2 = tasklist.add_task("Task 2", "Description 2")
        task3 = tasklist.add_task("Task 3", "Description 3")

        # Act: Delete middle task
        success, msg = tasklist.delete_task(task2.id)

        # Assert: Task removed, others intact
        assert success is True
        remaining = tasklist.get_all_tasks()
        assert len(remaining) == 2
        assert [t.id for t in remaining] == [task1.id, task3.id]
        assert all(t.id != task2.id for t in remaining)

    # T019: Edge case - delete first task
    def test_delete_first_task_from_list(self) -> None:
        """Deleting first task works correctly."""
        tasklist = TaskList()
        task1 = tasklist.add_task("First")
        task2 = tasklist.add_task("Second")
        task3 = tasklist.add_task("Third")

        success, msg = tasklist.delete_task(task1.id)

        assert success is True
        remaining = tasklist.get_all_tasks()
        assert len(remaining) == 2
        assert remaining[0].id == task2.id
        assert remaining[1].id == task3.id

    # T019: Edge case - delete last task
    def test_delete_last_task_from_list(self) -> None:
        """Deleting last task works correctly."""
        tasklist = TaskList()
        task1 = tasklist.add_task("First")
        task2 = tasklist.add_task("Second")
        task3 = tasklist.add_task("Third")

        success, msg = tasklist.delete_task(task3.id)

        assert success is True
        remaining = tasklist.get_all_tasks()
        assert len(remaining) == 2
        assert remaining[0].id == task1.id
        assert remaining[1].id == task2.id

    # T019: Edge case - delete only task results in empty list
    def test_delete_only_task_results_in_empty_list(self) -> None:
        """Deleting only task shows empty list."""
        tasklist = TaskList()
        task = tasklist.add_task("Only task")

        success, msg = tasklist.delete_task(task.id)

        assert success is True
        assert len(tasklist.get_all_tasks()) == 0

    # T019: Edge case - rapid consecutive deletions
    def test_rapid_consecutive_deletions(self) -> None:
        """Multiple deletions in sequence work correctly."""
        tasklist = TaskList()
        tasks = [tasklist.add_task(f"Task {i}") for i in range(1, 6)]

        # Delete tasks 2, 4, 1 in that order
        tasklist.delete_task(tasks[1].id)
        tasklist.delete_task(tasks[3].id)
        tasklist.delete_task(tasks[0].id)

        remaining = tasklist.get_all_tasks()
        assert len(remaining) == 2
        assert [t.id for t in remaining] == [tasks[2].id, tasks[4].id]

    # T019: Edge case - delete then add maintains ID sequence
    def test_delete_then_add_maintains_id_sequence(self) -> None:
        """After deleting tasks, new tasks get next sequential ID."""
        tasklist = TaskList()
        task1 = tasklist.add_task("Task 1")
        task2 = tasklist.add_task("Task 2")
        task3 = tasklist.add_task("Task 3")

        # Delete task 2
        tasklist.delete_task(task2.id)

        # Add new task - should get ID 4, not 2
        task4 = tasklist.add_task("Task 4")

        assert task4.id == 4
        remaining_ids = [t.id for t in tasklist.get_all_tasks()]
        assert remaining_ids == [1, 3, 4]  # Gap at ID 2

    # T019: Edge case - attempt delete on already deleted ID
    def test_delete_already_deleted_task(self) -> None:
        """Attempting to delete already-deleted task returns error."""
        tasklist = TaskList()
        task = tasklist.add_task("Task")

        # First deletion succeeds
        success1, msg1 = tasklist.delete_task(task.id)
        assert success1 is True

        # Second deletion fails
        success2, msg2 = tasklist.delete_task(task.id)
        assert success2 is False
        assert "not found" in msg2.lower()

    # T019: Edge case - very large task IDs
    def test_delete_with_large_id_gaps(self) -> None:
        """Deletion works correctly even with large ID values."""
        tasklist = TaskList()
        # Simulate scenario where many tasks were created and deleted
        # Fast-forward the ID counter
        for i in range(100):
            tasklist.add_task(f"Task {i}")

        # Now delete all but a few
        all_tasks = tasklist.get_all_tasks()
        for task in all_tasks[:-3]:  # Keep last 3
            tasklist.delete_task(task.id)

        remaining = tasklist.get_all_tasks()
        assert len(remaining) == 3
        assert all(t.id >= 98 for t in remaining)  # IDs 98, 99, 100
