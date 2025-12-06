"""CLI handlers for task operations.

This module provides command-line interface functions for task management.
"""

from typing import Optional
from src.models.task import TaskList
from src.utils.validators import validate_title, validate_description


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
    description = input("> ").strip()

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
