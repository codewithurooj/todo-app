# Data Model: Update Task Feature

**Feature**: 003-update-task
**Date**: 2025-12-06
**Status**: Phase 1 - Design

## Overview

This document defines data model extensions for Update Task feature. Builds on existing Task and TaskList from 001-add-task, adding update operations while preserving all existing attributes and behaviors.

---

## 1. Task Entity

### Changes from 001-add-task

**No changes to Task entity**. The Task dataclass remains identical. All attributes are mutable (not frozen).

### Update Behavior

**When a task is updated**:
- Modified fields: title, description, or completed
- Immutable fields: id, created_at (never change)
- Unmodified fields: preserved exactly as-is
- No task recreation or copying

---

## 2. TaskList Collection

### Extended Operations

```python
class TaskList:
    # NEW methods for update feature:
    
    def update_task_title(self, task_id: int, new_title: str) -> tuple[bool, str]:
        """Update task title. Preserves all other fields."""
        task = self.get_task_by_id(task_id)
        if not task:
            return False, f"Error: Task #{task_id} not found"
        task.title = new_title
        return True, f"Task #{task_id} title updated successfully"
    
    def update_task_description(self, task_id: int, new_desc: str | None) -> tuple[bool, str]:
        """Update task description. None/empty removes description."""
        task = self.get_task_by_id(task_id)
        if not task:
            return False, f"Error: Task #{task_id} not found"
        task.description = new_desc
        return True, f"Task #{task_id} description updated successfully"
    
    def update_task_status(self, task_id: int) -> tuple[bool, str]:
        """Toggle task completion status."""
        task = self.get_task_by_id(task_id)
        if not task:
            return False, f"Error: Task #{task_id} not found"
        task.completed = not task.completed
        status_text = "complete" if task.completed else "incomplete"
        return True, f"Task #{task_id} marked as {status_text}"
```

### Update Invariants

1. **ID Immutability**: Task ID never changes during update
2. **Timestamp Preservation**: created_at never changes
3. **Atomic Updates**: Multi-field updates apply all or none
4. **Validation**: Title/description must pass same rules as create

---

## 3. Validation Model

### Reused Validators

**From 001-add-task** (no changes):
- `validate_title(title: str) -> tuple[bool, str]`
- `validate_description(description: str | None) -> tuple[bool, str]`

**Same validation rules apply**:
- Title: 1-200 chars, non-empty
- Description: 0-1000 chars, optional (None allowed)

---

## 4. Update State Flow

```
User selects "Update Task"
    ↓
Empty list check → If empty: "No tasks to update" → Menu
    ↓
Prompt for task ID
    ↓
Validate ID → Invalid: Error → Reprompt
             → Cancel: "Cancelled" → Menu
             → Valid: Continue
    ↓
Lookup task → Not found: "Task not found" → Menu
            → Found: Display current values
    ↓
Field selection menu
    ↓
For each selected field:
    - Show current value
    - Prompt for new value
    - Validate → Invalid: Error → Reprompt
              → Cancel: Abort update → Menu
              → Valid: Store
    ↓
Apply all changes atomically
    ↓
Show success message → Menu
```

---

## 5. Evolution Path

### Phase II (File Persistence)
- After update, save to JSON file
- No changes to update logic

### Phase IV (Database)
```sql
UPDATE tasks 
SET title = ?, description = ?, completed = ?
WHERE id = ?
```

---

## Summary

| Component | Changes from 001 | Evolution Ready |
|-----------|------------------|-----------------|
| Task Entity | None | ✅ Same |
| TaskList | Added 3 update methods | ✅ Maps to SQL UPDATE |
| Validation | Reused from 001 | ✅ No changes needed |
| Update Logic | Direct modification | ✅ Works for all phases |

**Status**: Phase 1 Design Complete
