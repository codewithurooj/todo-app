"""CLI handlers for task operations.

This module provides command-line interface functions for task management.
"""

from src.models.task import TaskList
from src.utils.validators import validate_description, validate_title


def add_task_cli(tasklist: TaskList) -> None:
    """Handle add task user interaction via CLI.

    Prompts user for task title and optional description,
    validates input, creates task, and displays confirmation.

    Args:
        tasklist: TaskList instance to add task to
    """
    print("\n" + "=" * 50)
    print("           ADD NEW TASK")
    print("=" * 50)

    # Prompt for title with validation
    while True:
        title = input("\nEnter task title (or 'cancel' to abort): ").strip()

        # Check for cancel
        if title.lower() == "cancel":
            print("Task creation cancelled.")
            return

        # Validate title
        is_valid, error_msg = validate_title(title)
        if is_valid:
            break
        else:
            print(f"\n{error_msg}")
            print("Please try again.")

    # Prompt for description (optional)
    print("\nEnter description (optional, press Enter to skip):")
    description: str | None = input("> ").strip()

    # Validate description if provided
    if description:
        is_valid, error_msg = validate_description(description)
        if not is_valid:
            print(f"\n{error_msg}")
            print("Task will be created without description.")
            description = None
    else:
        description = None

    # Create task
    task = tasklist.add_task(title, description)

    # Display confirmation
    print("\n" + "-" * 50)
    print(f"✓ Task #{task.id} created successfully!")
    print(f"  Title: {task.title}")
    if task.description:
        print(f"  Description: {task.description[:50]}...")
    print(f"  Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}")
    print("-" * 50)


def delete_task_cli(tasklist: TaskList) -> None:
    """Handle delete task user interaction via CLI.

    Prompts user for task ID, validates input, requests confirmation,
    deletes task, and displays confirmation.

    Args:
        tasklist: TaskList instance to delete task from
    """
    from src.utils.validators import validate_task_id

    print("\n" + "=" * 50)
    print("           DELETE TASK")
    print("=" * 50)

    # Check if list is empty
    if not tasklist.get_all_tasks():
        print("\nNo tasks available to delete.")
        print("Add some tasks first before deleting.")
        return

    # Display current tasks for reference
    print("\nCurrent tasks:")
    for task in tasklist.get_all_tasks():
        status = "✓" if task.completed else " "
        print(f"  [{status}] #{task.id}: {task.title}")

    # Prompt for task ID with validation
    while True:
        task_id_input = input("\nEnter task ID to delete (or 'cancel' to abort): ").strip()

        # Validate ID
        is_valid, task_id, error_msg = validate_task_id(task_id_input)

        # Handle cancel
        if error_msg == "CANCEL":
            print("Delete operation cancelled.")
            return

        # Handle validation error
        if not is_valid:
            print(f"\n{error_msg}")
            print("Please try again.")
            continue

        # ID is valid, break the loop
        break

    # Find task to show details in confirmation
    task = tasklist.find_by_id(task_id)

    if not task:
        print(f"\nError: Task #{task_id} not found. Please check the task ID and try again.")
        return

    # Confirmation prompt (User Story 3 - P3)
    print(f"\nDelete task #{task.id}: '{task.title}'?")
    while True:
        confirm = input("Confirm (y/n): ").strip().lower()

        if confirm in ["y", "yes"]:
            # Proceed with deletion
            break
        elif confirm in ["n", "no"]:
            print("Deletion cancelled.")
            return
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

    # Delete task
    success, msg = tasklist.delete_task(task_id)

    # Display result
    print("\n" + "-" * 50)
    if success:
        print(f"✓ {msg}")
    else:
        print(f"✗ {msg}")
    print("-" * 50)
