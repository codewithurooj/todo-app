# Technical Research: Update Task Feature

**Feature**: 003-update-task
**Date**: 2025-12-06
**Status**: Completed

## Overview

This document captures technical research and decisions for the Update Task feature. All decisions build on existing patterns from 001-add-task and 002-delete-task while adding update-specific functionality.

---

## 1. Update Operation Design

### Decision

**Choice**: Direct attribute modification on existing Task object

**Rationale**:
- Simplest approach: modify attributes directly
- Preserves object identity and references
- No need to recreate task or manage copies
- Python dataclasses support attribute modification by default
- Memory efficient (no object copying)

**Alternatives Considered**:
- **Create new task**: Wasteful, loses object identity, complex ID management
- **Copy-and-modify**: Unnecessary complexity, risk of missing fields

**Implementation**:
```python
def update_task_title(self, task_id: int, new_title: str) -> tuple[bool, str]:
    task = self.get_task_by_id(task_id)
    if not task:
        return False, f"Error: Task #{task_id} not found"
    
    task.title = new_title  # Direct modification
    return True, f"Task #{task_id} title updated successfully"
```

**Evolution Path**: Phase II/IV same approach works (modify then persist).

---

## 2. Field Selection UI

### Decision

**Choice**: Menu-based field selection after ID entry

**Rationale**:
- Clear UX: user sees available options
- Flexible: can update one or multiple fields
- Follows CLI best practices
- Allows easy addition of new fields
- Cancel option at each step

**Implementation Flow**:
```
1. Prompt for task ID
2. Display task current values
3. Show menu: "What would you like to update?"
   - 1. Title
   - 2. Description
   - 3. Completion Status
   - 4. Multiple fields
   - 5. Cancel
4. Based on choice, prompt for new value(s)
5. Confirm and apply changes
```

**Evolution Path**: REST API won't need menu - client sends fields to update.

---

## 3. Validation Reuse Strategy

### Decision

**Choice**: Reuse validate_title() and validate_description() directly from 001-add-task

**Rationale**:
- DRY principle: same validation rules for create and update
- Already tested and proven
- Consistent error messages
- No code duplication
- Import from utils.validators

**Implementation**:
```python
from utils.validators import validate_title, validate_description

# In update_task_title()
valid, error = validate_title(new_title)
if not valid:
    return False, error
```

**No new validators needed** - existing ones cover all update scenarios.

**Evolution Path**: Phase III (API) might add Pydantic but logic stays same.

---

## 4. Partial Update Handling

### Decision

**Choice**: Separate methods for each field type (update_title, update_description, update_status)

**Rationale**:
- Clear API: each method has single responsibility
- Simple implementation: no complex optional parameters
- Easy to test: one method per operation
- Flexible: can be combined in multi-field update
- Follows Unix philosophy: do one thing well

**Alternatives Considered**:
- **Single update() with all fields optional**: Complex signatures, nullable parameters confusing
- **Pass dict of changes**: Harder to validate, less type-safe

**Implementation**:
```python
# TaskService methods
def update_task_title(self, task_id: int, new_title: str) -> tuple[bool, str]
def update_task_description(self, task_id: int, new_desc: str | None) -> tuple[bool, str]
def update_task_status(self, task_id: int) -> tuple[bool, str]  # Toggle
```

**Multi-field update**: Call multiple methods in sequence within a transaction-like pattern.

**Evolution Path**: Phase III can wrap these in single REST PUT endpoint.

---

## 5. Status Toggle Logic

### Decision

**Choice**: Dedicated toggle method (no parameter, flips current state)

**Rationale**:
- Common operation: mark done / mark undone
- Simple UX: no need to specify True/False
- Self-documenting: toggle means flip
- Idempotent: can be called multiple times safely

**Implementation**:
```python
def update_task_status(self, task_id: int) -> tuple[bool, str]:
    task = self.get_task_by_id(task_id)
    if not task:
        return False, f"Error: Task #{task_id} not found"
    
    task.completed = not task.completed  # Toggle
    status_text = "complete" if task.completed else "incomplete"
    return True, f"Task #{task_id} marked as {status_text}"
```

**Evolution Path**: REST API can provide both PATCH (set specific value) and POST toggle endpoint.

---

## 6. Empty Description Handling

### Decision

**Choice**: Allow setting description to None or empty string to remove description

**Rationale**:
- User might want to remove description
- Empty input (just pressing Enter) means "remove description"
- Consistent with optional field semantics
- Provides way to clean up tasks

**Implementation**:
```python
# If user enters empty string or just presses Enter
new_desc = input("Enter new description (empty to remove): ").strip()
if not new_desc:
    new_desc = None  # Remove description
```

**Evolution Path**: REST API can use PATCH with `null` or `""` to remove.

---

## 7. Show Current Value Before Update

### Decision

**Choice**: Display current values before prompting for new value

**Rationale**:
- User knows what they're replacing
- Helps prevent accidental overwrites
- Shows context for decision
- Improves UX: informed editing

**Implementation**:
```
Enter task ID to update: 5

Current task #5:
  Title: Buy groceries
  Description: Milk, eggs, bread
  Status: Incomplete

What would you like to update?
```

**Evolution Path**: Web UI naturally shows current values in form fields.

---

## 8. Cancel at Any Step

### Decision

**Choice**: Allow "cancel" keyword at any input prompt

**Rationale**:
- Safety: user can abort if they make mistake
- Consistent with delete feature (002)
- Prevents unwanted changes
- Good UX practice

**Implementation**:
```python
# At each prompt
user_input = input("Enter new title (or 'cancel'): ")
if user_input.lower() == 'cancel':
    return False, "Update cancelled"
```

**Evolution Path**: Web/API doesn't need this - user just doesn't submit form.

---

## 9. Multi-Field Update Strategy

### Decision

**Choice**: Prompt for each selected field sequentially, validate each, apply all or none

**Rationale**:
- Atomic update: all changes apply or none do
- Clear validation: error on any field cancels entire update
- Prevents partial updates leaving task in inconsistent state
- User can retry with corrected values

**Implementation**:
```python
# Collect all new values first
new_title = prompt_and_validate_title()
new_desc = prompt_and_validate_description()

# Only if all valid, apply all changes
if all_valid:
    task.title = new_title
    task.description = new_desc
    return True, "Task updated successfully (2 fields)"
else:
    return False, "Update cancelled - validation failed"
```

**Evolution Path**: REST API PATCH with multiple fields follows same atomic pattern.

---

## Summary of Decisions

| Decision Area | Choice |
|---------------|--------|
| Update Operation | Direct attribute modification |
| Field Selection UI | Menu-based after ID entry |
| Validation | Reuse from 001-add-task |
| Partial Updates | Separate methods per field |
| Status Toggle | Dedicated toggle method (flip) |
| Empty Description | None/empty removes description |
| Show Current Value | Display before prompting |
| Cancel Operation | Accept "cancel" at any prompt |
| Multi-Field Update | Sequential prompts, atomic apply |

---

**Status**: All research complete. Ready for Phase 1 (Design & Contracts).
