"""Input validation functions for todo application.

This module provides validation for task fields (title, description) with
clear error messages for user feedback.
"""


def validate_title(title: str) -> tuple[bool, str]:
    """Validate task title input.

    Args:
        title: User-provided task title

    Returns:
        Tuple of (is_valid: bool, error_message: str)
        - (True, "") if valid
        - (False, error_message) if invalid

    Validation Rules:
        - Cannot be empty or whitespace-only
        - Maximum length: 200 characters
    """
    # Check if empty or whitespace
    if not title or not title.strip():
        return (False, "Error: Task title cannot be empty. Please enter a title.")

    # Check length (after stripping)
    stripped_title = title.strip()
    if len(stripped_title) > 200:
        return (
            False,
            f"Error: Task title too long ({len(stripped_title)} characters). "
            f"Maximum is 200 characters.",
        )

    return (True, "")


def validate_description(description: str | None) -> tuple[bool, str]:
    """Validate task description input.

    Args:
        description: User-provided task description (can be None or empty)

    Returns:
        Tuple of (is_valid: bool, error_message: str)
        - (True, "") if valid
        - (False, error_message) if invalid

    Validation Rules:
        - Optional (None or empty string is valid)
        - Maximum length: 1000 characters
    """
    # None or empty is valid (description is optional)
    if description is None or description == "":
        return (True, "")

    # Check length (after stripping)
    stripped_desc = description.strip()
    if len(stripped_desc) > 1000:
        return (
            False,
            f"Error: Task description too long ({len(stripped_desc)} characters). "
            f"Maximum is 1000 characters.",
        )

    return (True, "")


def validate_task_id(task_id_str: str) -> tuple[bool, int | None, str]:
    """Validate task ID input.

    Args:
        task_id_str: User-provided task ID as string

    Returns:
        Tuple of (is_valid: bool, task_id: int | None, error_message: str)
        - (True, task_id, "") if valid
        - (False, None, error_message) if invalid

    Validation Rules:
        - Cannot be empty
        - Must be numeric (parseable as int)
        - Must be positive (>= 1)
        - Leading zeros are acceptable ("007" → 7)
        - "cancel" keyword returns special signal
    """
    # Check for empty input
    if not task_id_str or not task_id_str.strip():
        return False, None, "Error: Task ID cannot be empty. Please enter a task ID."

    # Check for cancel keyword
    if task_id_str.strip().lower() == "cancel":
        return False, None, "CANCEL"  # Special signal for cancellation

    # Check if numeric
    try:
        task_id = int(task_id_str.strip())
    except ValueError:
        return (
            False,
            None,
            "Error: Invalid task ID. Please enter a numeric ID (e.g., 1, 2, 3).",
        )

    # Check if positive
    if task_id < 1:
        return False, None, "Error: Task ID must be a positive number (1 or greater)."

    return True, task_id, ""
