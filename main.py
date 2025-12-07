"""
Todo App - Console Application Entry Point

A simple in-memory todo list manager with CRUD operations.
Phase I: Console interface with in-memory storage (no persistence).
"""

from src.cli.task_cli import (
    add_task_cli,
    delete_task_cli,
    mark_complete_cli,
    reopen_task_cli,
    update_task_cli,
    view_all_tasks_cli,
)
from src.models.task import TaskList


def display_menu() -> None:
    """Display the main menu options."""
    print("\n" + "=" * 50)
    print("           MAIN MENU")
    print("=" * 50)
    print("  1. Add Task")
    print("  2. View Tasks")
    print("  3. Update Task")
    print("  4. Delete Task")
    print("  5. Mark Task Complete")
    print("  6. Reopen Completed Task")
    print("  0. Exit")
    print("=" * 50)


def main() -> None:
    """Main application entry point."""
    # Initialize task list (in-memory storage)
    tasklist = TaskList()

    print("=" * 50)
    print("     Todo App - In-Memory Task Manager")
    print("=" * 50)
    print("\nWelcome! Manage your tasks with ease.")
    print("Note: Tasks are stored in memory and will be")
    print("lost when you exit the application (Phase I).")

    # Main application loop
    while True:
        display_menu()

        try:
            choice = input("\nEnter your choice (0-6): ").strip()

            if choice == "1":
                add_task_cli(tasklist)

            elif choice == "2":
                view_all_tasks_cli(tasklist)

            elif choice == "3":
                update_task_cli(tasklist)

            elif choice == "4":
                delete_task_cli(tasklist)

            elif choice == "5":
                mark_complete_cli(tasklist)

            elif choice == "6":
                reopen_task_cli(tasklist)

            elif choice == "0":
                print("\n" + "=" * 50)
                print("Thank you for using Todo App!")
                print("Your tasks will not be saved (Phase I limitation).")
                print("=" * 50)
                break

            else:
                print("\nInvalid choice. Please enter a number between 0 and 6.")

        except KeyboardInterrupt:
            print("\n\nApplication interrupted. Exiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()
