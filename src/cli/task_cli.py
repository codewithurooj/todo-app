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


def update_task_cli(tasklist):
    """Handle update task user interaction via CLI.

    Prompts user for task ID, displays current values, allows field selection,
    validates input, updates task, and displays confirmation.

    Args:
        tasklist: TaskList instance to update task in
    """
    from src.utils.validators import validate_task_id, validate_title, validate_description

    print("\n" + "=" * 50)
    print("           UPDATE TASK")
    print("=" * 50)

    # Check if list is empty
    if not tasklist.get_all_tasks():
        print("\nNo tasks available to update.")
        print("Add some tasks first before updating.")
        return

    # Display current tasks for reference
    print("\nCurrent tasks:")
    for task in tasklist.get_all_tasks():
        status = "✓" if task.completed else " "
        print(f"  [{status}] #{task.id}: {task.title}")

    # Prompt for task ID with validation
    while True:
        task_id_input = input("\nEnter task ID to update (or 'cancel' to abort): ").strip()

        # Validate ID
        is_valid, task_id, error_msg = validate_task_id(task_id_input)

        # Handle cancel
        if error_msg == "CANCEL":
            print("Update operation cancelled.")
            return

        # Handle validation error
        if not is_valid:
            print(f"\n{error_msg}")
            print("Please try again.")
            continue

        # ID is valid, break the loop
        break

    # Find task to show details
    task = tasklist.find_by_id(task_id)

    if not task:
        print(f"\nError: Task #{task_id} not found. Please check the task ID and try again.")
        return

    # Display current task values
    print("\n" + "-" * 50)
    print(f"Current Task #{task.id}:")
    print(f"  Title: {task.title}")
    print(f"  Description: {task.description if task.description else '(none)'}")
    status_display = "Complete ✓" if task.completed else "Incomplete"
    print(f"  Status: {status_display}")
    print(f"  Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}")
    print(f"  Updated: {task.updated_at.strftime('%Y-%m-%d %H:%M')}")
    print("-" * 50)

    # Field selection menu
    print("\nWhat would you like to update?")
    print("  1. Title")
    print("  2. Description")
    print("  3. Status (Toggle Complete/Incomplete)")
    print("  0. Cancel")

    while True:
        choice = input("\nEnter your choice (0-3): ").strip()

        if choice == "0":
            print("Update cancelled.")
            return

        elif choice == "1":
            # Update Title
            print(f"\nCurrent title: {task.title}")

            while True:
                new_title = input("Enter new title (or 'cancel' to abort): ").strip()

                # Handle cancel
                if new_title.lower() == "cancel":
                    print("Title update cancelled.")
                    return

                # Validate title
                is_valid, error_msg = validate_title(new_title)
                if is_valid:
                    break
                else:
                    print(f"\n{error_msg}")
                    print(f"Current title: {task.title}")
                    print("Please try again.")

            # Update title
            success, msg = tasklist.update_task_title(task_id, new_title)

            # Display confirmation
            print("\n" + "-" * 50)
            if success:
                print(f"✓ {msg}")
                print(f"  New title: {task.title}")
            else:
                print(f"✗ {msg}")
            print("-" * 50)
            return

        elif choice == "2":
            # Update Description
            current_desc = task.description if task.description else "(none)"
            print(f"\nCurrent description: {current_desc}")
            print("Enter new description (or press Enter to clear, 'cancel' to abort):")
            new_description = input("> ").strip()

            # Handle cancel
            if new_description.lower() == "cancel":
                print("Description update cancelled.")
                return

            # Handle empty description
            if not new_description:
                new_description = None
                print("Description will be cleared.")
            else:
                # Validate description
                is_valid, error_msg = validate_description(new_description)
                if not is_valid:
                    print(f"\n{error_msg}")
                    print("Description update cancelled.")
                    return

            # Update description
            success, msg = tasklist.update_task_description(task_id, new_description)

            # Display confirmation
            print("\n" + "-" * 50)
            if success:
                print(f"✓ {msg}")
                new_desc_display = task.description if task.description else "(cleared)"
                print(f"  New description: {new_desc_display}")
            else:
                print(f"✗ {msg}")
            print("-" * 50)
            return

        elif choice == "3":
            # Toggle Status
            current_status = "Complete" if task.completed else "Incomplete"
            new_status = not task.completed
            new_status_display = "Complete" if new_status else "Incomplete"

            print(f"\nCurrent status: {current_status}")
            print(f"Change to: {new_status_display}")

            confirm = input("Confirm (y/n): ").strip().lower()
            if confirm not in ["y", "yes"]:
                print("Status update cancelled.")
                return

            # Update status
            success, msg = tasklist.update_task_status(task_id, new_status)

            # Display confirmation
            print("\n" + "-" * 50)
            if success:
                print(f"✓ {msg}")
                status_icon = "✓" if new_status else " "
                print(f"  Status: [{status_icon}] {new_status_display}")
            else:
                print(f"✗ {msg}")
            print("-" * 50)
            return

        else:
            print("Invalid choice. Please enter a number between 0 and 3.")


def view_all_tasks_cli(tasklist):
    """Display all tasks in the task list.

    Shows tasks with ID, status icon, and title (truncated at 50 chars).
    Displays empty message if no tasks exist.

    Args:
        tasklist: TaskList instance

    Returns:
        None (prints to console)
    """
    from src.lib.display import format_task_list

    print("\n" + "=" * 50)
    print("ALL TASKS")
    print("=" * 50)

    tasks = tasklist.get_all_tasks()
    output = format_task_list(tasks, context="all")
    print(output)
    print("=" * 50)
