# CLI Contract: Update Task

**Feature**: 003-update-task
**Type**: CLI Interface Contract

## Update Task CLI Flow

```
1. Prompt for task ID
2. Validate ID
3. Lookup task (show error if not found)
4. Display current values
5. Show field selection menu:
   1. Update Title
   2. Update Description
   3. Toggle Status
   4. Update Multiple Fields
   5. Cancel
6. Based on choice, prompt for new value(s)
7. Validate input
8. Apply changes
9. Show confirmation
```

## Message Formats

**Empty list**: `"No tasks available to update"`
**Task not found**: `"Error: Task #99 not found"`
**Success**: `"Task #5 title updated successfully"`
**Cancel**: `"Update cancelled"`

## Testing Requirements

- ✅ Empty list handled
- ✅ Invalid ID handled
- ✅ Field selection works
- ✅ Current values shown
- ✅ Cancel at any step
- ✅ Multi-field atomic update
