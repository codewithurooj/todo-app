# Task Service Contract: Delete Operations

**Feature**: 002-delete-task
**Date**: 2025-12-06
**Type**: Service Interface Contract

---

## Overview

This contract extends the TaskService interface from 001-add-task with delete operations. All components that delete tasks must adhere to this contract.

---

## TaskService Extended Interface

```python
from typing import Optional, List

class TaskService:
    """Task service interface including delete operations."""

    # EXISTING from 001-add-task:
    def create_task(self, title: str, description: Optional[str] = None) -> tuple[bool, Task | str]:
        ...

    # NEW for delete feature:
    def delete_task(self, task_id: int) -> tuple[bool, str]:
        """
        Delete a task by ID.

        Args:
            task_id: The ID of the task to delete (pre-validated as positive integer)

        Returns:
            On success: (True, success_message)
            On failure: (False, error_message)

        Contract:
            - MUST validate that task exists before deletion
            - MUST return error if task not found
            - MUST remove task from storage
            - MUST NOT modify other tasks
            - MUST NOT reuse deleted task IDs
            - MUST include task title in success message
            - MUST NOT raise exceptions for not-found errors
        """
        pass

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieve task by ID (needed for confirmation flow).

        Returns:
            Task if found, None if not found

        Contract:
            - MUST return actual Task object (not copy)
            - MUST return None for non-existent IDs
            - MUST NOT raise exceptions
        """
        pass
```

---

## Return Value Contract

### Success Case

```python
# When task exists and is deleted
(True, "Task #5 'Buy groceries' deleted successfully")
```

**Format**: `"Task #[ID] '[TITLE]' deleted successfully"`

**Requirements**:
- Boolean first element MUST be `True`
- Message MUST include task ID
- Message MUST include task title in single quotes
- Message MUST end with "deleted successfully"

### Failure Case: Task Not Found

```python
# When task doesn't exist
(False, "Error: Task #99 not found. Please enter a valid task ID.")
```

**Format**: `"Error: Task #[ID] not found. Please enter a valid task ID."`

**Requirements**:
- Boolean first element MUST be `False`
- Message MUST start with "Error:"
- Message MUST include the attempted task ID
- Message MUST guide user to enter valid ID

---

## Testing Requirements

### Unit Tests

- ✅ Delete existing task returns (True, success_message)
- ✅ Delete non-existent task returns (False, error_message)
- ✅ Delete removes task from storage
- ✅ Delete preserves other tasks
- ✅ Success message includes ID and title
- ✅ Error message includes attempted ID
- ✅ Deleted task ID not reused by new tasks

### Integration Tests

- ✅ Delete flow integrates with validation
- ✅ Confirmation flow receives correct task details
- ✅ Error messages displayed to user correctly

---

**Status**: Contract Defined
**Version**: 1.0.0
**Last Updated**: 2025-12-06
