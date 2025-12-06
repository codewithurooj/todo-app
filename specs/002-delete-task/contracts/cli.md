# CLI Contract: Delete Task

**Feature**: 002-delete-task
**Date**: 2025-12-06
**Type**: CLI Interface Contract

---

## Overview

This contract defines the command-line interface behavior for the Delete Task feature.

---

## Delete Task CLI Flow

### Function Signature

```python
def delete_task_cli(task_service: TaskService) -> None:
    """
    CLI flow for deleting a task.

    Args:
        task_service: TaskService instance

    Contract:
        - MUST check for empty list before prompting
        - MUST validate task ID input
        - MUST handle cancel operation
        - MUST display confirmation prompt (P3)
        - MUST show success or error message
        - MUST return to main menu after completion
        - MUST NOT crash on invalid input
    """
```

---

## UI Flow Contract

### Step 1: Empty List Check

```
IF task_service.get_all_tasks() is empty:
    DISPLAY: "No tasks available to delete"
    RETURN to main menu
```

### Step 2: ID Input Prompt

```
DISPLAY: "Enter task ID to delete (or 'cancel' to abort): "
READ: user_input
```

**Validation**:
- Call `validate_task_id(user_input)`
- If invalid: Show error, re-prompt
- If "CANCEL": Show "Delete operation cancelled", return to menu
- If valid: Continue to Step 3

### Step 3: Task Existence Check

```
task = task_service.get_task_by_id(task_id)
IF task is None:
    DISPLAY: "Error: Task #{{id}} not found. Please enter a valid task ID."
    RETURN to main menu
```

### Step 4: Confirmation Prompt (P3 Optional)

```
DISPLAY: "Delete task #{{id}}: '{{title}}'? (y/n): "
READ: confirmation
```

**Validation**:
- Call `validate_confirmation(confirmation)`
- If invalid: Show error, re-prompt
- If No: Show "Deletion cancelled", return to menu
- If Yes: Continue to Step 5

### Step 5: Delete and Confirm

```
success, message = task_service.delete_task(task_id)
DISPLAY: message
RETURN to main menu
```

---

## Message Format Contract

### Empty List

```
No tasks available to delete
```

### Cancel Operation

```
Delete operation cancelled
```

### Invalid ID Format

```
Error: Invalid task ID. Please enter a numeric ID.
```

### Task Not Found

```
Error: Task #99 not found. Please enter a valid task ID.
```

### Confirmation Prompt

```
Delete task #5: 'Buy groceries'? (y/n):
```

**Format**: `"Delete task #[ID]: '[TITLE]'? (y/n): "`

### Deletion Cancelled at Confirmation

```
Deletion cancelled
```

### Success

```
Task #5 'Buy groceries' deleted successfully
```

**Format**: `"Task #[ID] '[TITLE]' deleted successfully"`

---

## Error Handling Contract

### Invalid Input Recovery

- **Invalid ID**: Re-prompt for ID (loop)
- **Invalid confirmation**: Re-prompt for confirmation (loop)
- **Task not found**: Display error, return to menu (no loop)
- **Empty list**: Display message, return to menu immediately

### Exit Conditions

- User types "cancel" at ID prompt
- User types "n"/"no" at confirmation
- Task successfully deleted
- Task not found error

---

## Testing Requirements

### Unit Tests (CLI Functions)

- ✅ Empty list displays correct message
- ✅ Cancel at ID prompt displays message and exits
- ✅ Invalid ID triggers re-prompt
- ✅ Valid ID proceeds to confirmation
- ✅ Confirmation "no" cancels deletion
- ✅ Confirmation "yes" deletes task
- ✅ Success message format correct
- ✅ Error message format correct

### Integration Tests

- ✅ Complete happy path (ID → confirm → delete → success)
- ✅ Cancel path (ID → cancel → menu)
- ✅ Confirmation cancel path (ID → confirm no → cancelled → menu)
- ✅ Not found path (invalid ID → error → menu)
- ✅ Empty list path (delete option → empty message → menu)

---

**Status**: Contract Defined
**Version**: 1.0.0
**Last Updated**: 2025-12-06
