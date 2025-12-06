# Service Layer Contract

**Feature**: 001-add-task
**Date**: 2025-12-06
**Type**: Service Interface Contract

---

## Overview

This contract defines the service layer interface for the Add Task feature. The service layer handles business logic and coordinates between validation, data storage, and presentation layers.

---

## TaskService Interface

```python
from typing import Optional

class TaskService:
    """
    Task service contract for business logic.
    """

    def __init__(self, task_list: TaskList):
        """
        Initialize service with task storage.

        Args:
            task_list: TaskList instance for data storage

        Contract:
            - MUST accept TaskList instance
            - MUST NOT create internal TaskList
        """
        pass

    def create_task(
        self,
        title: str,
        description: Optional[str] = None
    ) -> tuple[bool, Task | str]:
        """
        Create a new task with validation.

        Args:
            title: Task title (may be invalid)
            description: Optional task description (may be invalid)

        Returns:
            On success: (True, Task)
            On failure: (False, error_message)

        Contract:
            - MUST validate title using validate_title()
            - MUST validate description using validate_description()
            - MUST return first validation error if any
            - MUST call task_list.add_task() only if all valid
            - MUST NOT raise exceptions for validation errors
            - MUST strip title whitespace before storage
        """
        pass
```

---

## Validation Integration

### Contract

The service layer MUST:
1. Call `validate_title()` before processing title
2. Call `validate_description()` before processing description
3. Return validation error immediately if validation fails
4. Process title stripping only after validation passes
5. Never pass invalid data to TaskList

### Error Flow

```python
# Example implementation contract
def create_task(self, title: str, description: Optional[str] = None):
    # 1. Validate title
    valid_title, error = validate_title(title)
    if not valid_title:
        return False, error

    # 2. Validate description
    valid_desc, error = validate_description(description)
    if not valid_desc:
        return False, error

    # 3. Process title (strip whitespace)
    processed_title = title.strip()

    # 4. Create task
    task = self._task_list.add_task(processed_title, description)

    # 5. Return success
    return True, task
```

---

## Testing Requirements

### Unit Tests

- ✅ Create task with valid title only
- ✅ Create task with valid title and description
- ✅ Reject task with invalid title
- ✅ Reject task with invalid description
- ✅ Strip title whitespace before storage
- ✅ Do not strip description whitespace
- ✅ Return error message on validation failure
- ✅ Return Task object on success

### Integration Tests

- ✅ Created task has auto-generated ID
- ✅ Created task has current timestamp
- ✅ Created task has completed=False
- ✅ Task added to TaskList collection

---

**Status**: Contract Defined
**Version**: 1.0.0
**Last Updated**: 2025-12-06
