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
