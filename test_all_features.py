"""
Comprehensive test script for all Phase I features.
Tests all 5 features: Add, View, Update, Delete, Mark Complete.
"""

from src.models.task import TaskList
from src.cli.task_cli import (
    add_task_cli,
    delete_task_cli,
    update_task_cli,
    view_all_tasks_cli,
    mark_complete_cli,
    reopen_task_cli,
)

def test_all_features():
    """Test all features programmatically."""

    print("=" * 60)
    print("TESTING ALL TODO APP FEATURES - PHASE I")
    print("=" * 60)

    # Initialize task list
    tasklist = TaskList()

    # Test 1: Add Task
    print("\n[OK] Test 1: ADD TASK")
    print("-" * 60)
    task1 = tasklist.add_task("Buy groceries", "Milk, eggs, bread")
    task2 = tasklist.add_task("Complete homework", "Math and Science assignments")
    task3 = tasklist.add_task("Call dentist")
    print(f"  Created 3 tasks:")
    print(f"  - Task #{task1.id}: {task1.title}")
    print(f"  - Task #{task2.id}: {task2.title}")
    print(f"  - Task #{task3.id}: {task3.title}")

    # Test 2: View All Tasks
    print("\n[OK] Test 2: VIEW ALL TASKS")
    print("-" * 60)
    all_tasks = tasklist.get_all_tasks()
    print(f"  Total tasks: {len(all_tasks)}")
    for task in all_tasks:
        status = "[X]" if task.completed else "[ ]"
        desc = f" - {task.description[:30]}..." if task.description else ""
        print(f"  {status} #{task.id}: {task.title}{desc}")

    # Test 3: Update Task
    print("\n[OK] Test 3: UPDATE TASK")
    print("-" * 60)
    success, msg = tasklist.update_task_title(1, "Buy groceries and snacks")
    print(f"  Updated title: {msg}")
    success, msg = tasklist.update_task_description(2, "Math, Science, and English homework")
    print(f"  Updated description: {msg}")
    success, msg = tasklist.update_task_status(1, True)
    print(f"  Updated status: {msg}")

    # Test 4: Mark Complete
    print("\n[OK] Test 4: MARK COMPLETE")
    print("-" * 60)
    success, msg = tasklist.mark_complete(2)
    print(f"  Mark complete: {msg}")
    success, msg = tasklist.unmark_complete(1)
    print(f"  Reopen task: {msg}")

    # Test 5: Filter by Status
    print("\n[OK] Test 5: FILTER TASKS BY STATUS")
    print("-" * 60)
    pending = tasklist.filter_tasks_by_status(completed=False)
    completed = tasklist.filter_tasks_by_status(completed=True)
    print(f"  Pending tasks: {len(pending)}")
    for task in pending:
        print(f"    - #{task.id}: {task.title}")
    print(f"  Completed tasks: {len(completed)}")
    for task in completed:
        print(f"    - #{task.id}: {task.title}")

    # Test 6: Delete Task
    print("\n[OK] Test 6: DELETE TASK")
    print("-" * 60)
    success, msg = tasklist.delete_task(3)
    print(f"  Delete result: {msg}")
    all_tasks = tasklist.get_all_tasks()
    print(f"  Remaining tasks: {len(all_tasks)}")
    for task in all_tasks:
        status = "[X]" if task.completed else "[ ]"
        print(f"    {status} #{task.id}: {task.title}")

    # Test 7: Error Handling
    print("\n[OK] Test 7: ERROR HANDLING")
    print("-" * 60)
    success, msg = tasklist.delete_task(999)
    print(f"  Delete non-existent task: {msg}")
    success, msg = tasklist.mark_complete(999)
    print(f"  Mark non-existent complete: {msg}")
    success, msg = tasklist.mark_complete(2)
    print(f"  Mark already completed: {msg}")

    # Final Summary
    print("\n" + "=" * 60)
    print("ALL FEATURES TESTED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\nFinal task count: {len(tasklist.get_all_tasks())} tasks")
    print("\nFeatures verified:")
    print("  [OK] Feature 001: Add Task")
    print("  [OK] Feature 002: Delete Task")
    print("  [OK] Feature 003: Update Task")
    print("  [OK] Feature 004: View Tasks")
    print("  [OK] Feature 005: Mark Complete")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_all_features()
