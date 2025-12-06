# Task Service Contract: Update Operations

**Feature**: 003-update-task
**Type**: Service Interface Contract

## TaskService Extended Interface

```python
class TaskService:
    # NEW for update feature:
    
    def update_task_title(self, task_id: int, new_title: str) -> tuple[bool, str]:
        """Update task title. Must validate using validate_title()."""
        
    def update_task_description(self, task_id: int, new_desc: str | None) -> tuple[bool, str]:
        """Update description. None removes it. Must validate."""
        
    def update_task_status(self, task_id: int) -> tuple[bool, str]:
        """Toggle completion status."""
```

## Return Value Contract

**Success**: `(True, "Task #5 title updated successfully")`
**Failure**: `(False, "Error: Task #5 not found")`

## Testing Requirements

- ✅ Update existing task returns success
- ✅ Update non-existent task returns error
- ✅ Updated fields change, others preserved
- ✅ Validation enforced
- ✅ ID and timestamp never change
