# Contract: CLI Mark Complete Handler

**Feature**: 005-mark-complete
**Component**: CLI menu handlers for mark complete and reopen operations
**Created**: 2025-12-06

---

## Purpose

Define the interface contract for CLI menu handlers that allow users to mark tasks as complete or reopen them. These handlers provide the user-facing interface for completion status operations.

---

## Handler: `handle_mark_complete()`

### Signature

```python
def handle_mark_complete(task_list: TaskList) -> None:
    """
    Handle user request to mark a task as complete.

    Prompts user for task ID, validates input, calls TaskList.mark_complete(),
    and displays result message.

    Args:
        task_list: TaskList instance containing tasks

    Returns:
        None

    Side Effects:
        - Prompts user for input via console
        - Prints confirmation or error message
        - Modifies task completion status if successful

    User Interaction Flow:
        1. Display prompt: "Enter task ID to mark as complete: "
        2. Read user input
        3. Validate input is positive integer
        4. Call task_list.mark_complete(task_id)
        5. Display success/error message
        6. Return to main menu
    """
```

### User Interaction Flow

```
┌──────────────────────────────────────┐
│  User selects "Mark Task Complete"   │
└───────────────┬──────────────────────┘
                │
                v
┌──────────────────────────────────────┐
│  Display: "Enter task ID to mark     │
│           as complete: "              │
└───────────────┬──────────────────────┘
                │
                v
┌──────────────────────────────────────┐
│  Read user input                      │
└───────────────┬──────────────────────┘
                │
                v
         ┌──────┴───────┐
         │  Valid int?   │
         └──┬────────┬───┘
            │        │
         No │        │ Yes
            │        │
            v        v
    ┌───────────┐  ┌────────────────────────┐
    │ Display:  │  │ Call task_list         │
    │ "Invalid  │  │ .mark_complete(id)     │
    │  input"   │  └──────────┬─────────────┘
    └───────────┘             │
                              v
                    ┌──────────┴──────────┐
                    │  Display result     │
                    │  message from       │
                    │  mark_complete()    │
                    └─────────────────────┘
```

### Input Validation

```python
def validate_task_id_input(user_input: str) -> Tuple[bool, Optional[int], str]:
    """
    Validate user input for task ID.

    Args:
        user_input: Raw string input from user

    Returns:
        Tuple[bool, Optional[int], str]: (valid, task_id, error_message)
            - (True, task_id, "") if valid
            - (False, None, error_msg) if invalid

    Validation Rules:
        - Input must be convertible to integer
        - Integer must be positive (>= 1)
    """
    try:
        task_id = int(user_input.strip())
        if task_id < 1:
            return (False, None, "Task ID must be a positive integer")
        return (True, task_id, "")
    except ValueError:
        return (False, None, "Invalid input. Please enter a valid task ID (number)")
```

### Example Implementation

```python
def handle_mark_complete(task_list: TaskList) -> None:
    """Handle marking task as complete."""
    print("\n--- Mark Task Complete ---")

    # Prompt for task ID
    user_input = input("Enter task ID to mark as complete: ")

    # Validate input
    valid, task_id, error_msg = validate_task_id_input(user_input)
    if not valid:
        print(error_msg)
        return

    # Execute operation
    success, message = task_list.mark_complete(task_id)

    # Display result
    if success:
        print(message)
    else:
        print(message)
```

### Console Output Examples

**Success**:
```
--- Mark Task Complete ---
Enter task ID to mark as complete: 1
✓ Task 1 marked as complete
```

**Already Completed** (Idempotent):
```
--- Mark Task Complete ---
Enter task ID to mark as complete: 1
Task 1 is already completed
```

**Task Not Found**:
```
--- Mark Task Complete ---
Enter task ID to mark as complete: 999
Error: Task with ID 999 not found
```

**Invalid Input**:
```
--- Mark Task Complete ---
Enter task ID to mark as complete: abc
Invalid input. Please enter a valid task ID (number)
```

---

## Handler: `handle_reopen_task()`

### Signature

```python
def handle_reopen_task(task_list: TaskList) -> None:
    """
    Handle user request to reopen a completed task.

    Prompts user for task ID, validates input, calls TaskList.unmark_complete(),
    and displays result message.

    Args:
        task_list: TaskList instance containing tasks

    Returns:
        None

    Side Effects:
        - Prompts user for input via console
        - Prints confirmation or error message
        - Modifies task completion status if successful

    User Interaction Flow:
        1. Display prompt: "Enter task ID to reopen: "
        2. Read user input
        3. Validate input is positive integer
        4. Call task_list.unmark_complete(task_id)
        5. Display success/error message
        6. Return to main menu
    """
```

### Example Implementation

```python
def handle_reopen_task(task_list: TaskList) -> None:
    """Handle reopening completed task."""
    print("\n--- Reopen Completed Task ---")

    # Prompt for task ID
    user_input = input("Enter task ID to reopen: ")

    # Validate input
    valid, task_id, error_msg = validate_task_id_input(user_input)
    if not valid:
        print(error_msg)
        return

    # Execute operation
    success, message = task_list.unmark_complete(task_id)

    # Display result
    if success:
        print(message)
    else:
        print(message)
```

### Console Output Examples

**Success**:
```
--- Reopen Completed Task ---
Enter task ID to reopen: 1
✓ Task 1 reopened (marked as pending)
```

**Already Pending** (Idempotent):
```
--- Reopen Completed Task ---
Enter task ID to reopen: 1
Task 1 is already pending
```

**Task Not Found**:
```
--- Reopen Completed Task ---
Enter task ID to reopen: 999
Error: Task with ID 999 not found
```

---

## Menu Integration

### Main Menu Structure

```python
def display_main_menu() -> None:
    """Display main menu options."""
    print("\n=== Todo App - Main Menu ===")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete")      # New
    print("6. Reopen Completed Task")   # New
    print("7. Exit")
    print("="*30)

def handle_menu_selection(choice: str, task_list: TaskList) -> bool:
    """
    Handle user menu selection.

    Args:
        choice: User's menu choice (string)
        task_list: TaskList instance

    Returns:
        bool: True to continue, False to exit

    New Cases:
        - "5": Call handle_mark_complete(task_list)
        - "6": Call handle_reopen_task(task_list)
    """
    if choice == "5":
        handle_mark_complete(task_list)
        return True
    elif choice == "6":
        handle_reopen_task(task_list)
        return True
    # ... existing cases for 1-4, 7 ...
```

---

## Error Handling

### Input Validation Errors

| Error Condition | User Message |
|-----------------|--------------|
| Non-numeric input | "Invalid input. Please enter a valid task ID (number)" |
| Negative number | "Task ID must be a positive integer" |
| Zero | "Task ID must be a positive integer" |

### Operation Errors

| Error Condition | User Message |
|-----------------|--------------|
| Task not found | "Error: Task with ID {task_id} not found" |
| Already completed | "Task {task_id} is already completed" (not an error) |
| Already pending | "Task {task_id} is already pending" (not an error) |

---

## Integration Points

### Dependencies

**Required**:
- `TaskList.mark_complete()` from tasklist_completion_methods.md
- `TaskList.unmark_complete()` from tasklist_completion_methods.md

**Integrates With**:
- Main menu display and routing
- View tasks handler (004-view-task) - displays completion status

---

## Testing Requirements

### Unit Tests

```python
def test_handle_mark_complete_valid_input(capsys):
    """Verify valid input marks task and displays confirmation."""

def test_handle_mark_complete_invalid_input(capsys):
    """Verify invalid input displays error without modifying tasks."""

def test_handle_mark_complete_nonexistent_task(capsys):
    """Verify error message for non-existent task ID."""

def test_handle_reopen_task_valid_input(capsys):
    """Verify valid input reopens task and displays confirmation."""

def test_handle_reopen_task_invalid_input(capsys):
    """Verify invalid input displays error without modifying tasks."""

def test_menu_integration_option_5(capsys):
    """Verify menu option 5 calls handle_mark_complete."""

def test_menu_integration_option_6(capsys):
    """Verify menu option 6 calls handle_reopen_task."""
```

### Integration Tests

```python
def test_full_mark_complete_workflow(capsys):
    """
    Integration test: Create task -> Mark complete -> Verify in view.

    Steps:
    1. Add task via CLI
    2. Mark complete via CLI (option 5)
    3. View tasks via CLI (option 2)
    4. Verify task shows "[✓] Completed" status
    """

def test_full_reopen_workflow(capsys):
    """
    Integration test: Create task -> Complete -> Reopen -> Verify.

    Steps:
    1. Add task via CLI
    2. Mark complete via CLI (option 5)
    3. Reopen via CLI (option 6)
    4. View tasks via CLI (option 2)
    5. Verify task shows pending status (no "[✓]")
    """
```

---

## User Experience Requirements

### Responsiveness (SC-001)

- Operation completes within 1 second
- Immediate feedback after input

### Clarity (SC-006)

- 100% of users understand messages
- Clear success indicators ("✓")
- Consistent error format ("Error: ...")

### Robustness (SC-007)

- 0 crashes during 1000 operations
- All input errors handled gracefully
- No data corruption on invalid input

---

## Evolution Notes

### Phase III: REST API

Replace CLI handlers with HTTP endpoints:

```python
from fastapi import FastAPI, HTTPException

@app.patch("/tasks/{task_id}/complete")
async def mark_complete_endpoint(task_id: int):
    """HTTP endpoint for marking task complete."""
    success, message = task_list.mark_complete(task_id)
    if not success:
        raise HTTPException(status_code=404, detail=message)
    return {"success": True, "message": message}
```

### Phase VI: Web UI

Replace console prompts with HTML forms:

```html
<form id="markCompleteForm">
  <label for="taskId">Enter Task ID:</label>
  <input type="number" id="taskId" min="1" required>
  <button type="submit">Mark Complete</button>
</form>
```

---

## Contract Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-06 | Initial contract for Phase I CLI implementation |

---

## Notes

- Handlers are stateless - all state in TaskList
- Input validation happens before calling TaskList methods
- Error messages match those from TaskList methods
- Both handlers return to main menu after execution
