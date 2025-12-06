# Quickstart: View Tasks Feature Testing

**Feature**: 004-view-task
**Purpose**: Quick guide for developers to test the View Tasks feature

---

## Prerequisites

- Feature 001-add-task implemented (Task and TaskList entities exist)
- Feature 002-delete-task implemented (task ID validation exists)
- Feature 003-update-task implemented (task status can be modified)
- Python 3.13+ installed
- pytest installed

---

## Quick Test Scenarios

### Scenario 1: View All Tasks (Happy Path)

**Goal**: Verify all tasks display correctly with proper formatting.

**Steps**:
1. Run the application
2. Add 3 tasks:
   - "Buy groceries" with description "Get milk, bread, eggs"
   - "Finish report" with description "Complete quarterly report"
   - "Call dentist" with description ""
3. Select "View All Tasks"

**Expected Result**:
```
You have 3 task(s)

[1] [ ] Buy groceries
[2] [ ] Finish report
[3] [ ] Call dentist
```

**Verification**:
- ✅ Header shows correct count
- ✅ All 3 tasks appear
- ✅ IDs are in ascending order (1, 2, 3)
- ✅ Status shows "[ ]" for pending tasks
- ✅ Titles are displayed

---

### Scenario 2: View Empty List

**Goal**: Verify empty state message appears.

**Steps**:
1. Run the application with no tasks
2. Select "View All Tasks"

**Expected Result**:
```
No tasks found. Add a task to get started!
```

**Verification**:
- ✅ Helpful message appears
- ✅ No crash or empty output

---

### Scenario 3: View Task Details

**Goal**: Verify full task details display without truncation.

**Steps**:
1. Add a task with:
   - Title: "This is a very long task title that definitely exceeds fifty characters for testing purposes"
   - Description: "This is a detailed description with multiple sentences. It should appear in full in the detail view without any truncation at all."
2. Note the task ID (should be 1)
3. Select "View Task Details"
4. Enter task ID: 1

**Expected Result**:
```
ID: 1
Title: This is a very long task title that definitely exceeds fifty characters for testing purposes
Description: This is a detailed description with multiple sentences. It should appear in full in the detail view without any truncation at all.
Status: Pending
Created: 2025-12-06 10:00:00
Last Updated: 2025-12-06 10:00:00
```

**Verification**:
- ✅ Full title displayed (no truncation)
- ✅ Full description displayed (no truncation)
- ✅ All fields present (ID, Title, Description, Status, Created, Last Updated)
- ✅ Timestamps formatted as "YYYY-MM-DD HH:MM:SS"

---

### Scenario 4: Title Truncation in List View

**Goal**: Verify long titles are truncated in list view but not in detail view.

**Steps**:
1. Add task with title: "This is a very long task title that definitely exceeds fifty characters for testing truncation"
2. Select "View All Tasks"
3. Select "View Task Details" and enter the task ID

**Expected Result - List View**:
```
[1] [ ] This is a very long task title that exceeds ...
```

**Expected Result - Detail View**:
```
Title: This is a very long task title that definitely exceeds fifty characters for testing truncation
```

**Verification**:
- ✅ List view truncates at 50 chars with "..."
- ✅ Detail view shows full title
- ✅ Truncation is exactly 50 chars total (47 chars + "...")

---

### Scenario 5: Filter Pending Tasks

**Goal**: Verify pending filter shows only incomplete tasks.

**Steps**:
1. Add 5 tasks:
   - Task 1: "Pending 1" (leave as pending)
   - Task 2: "Completed 1" (mark as completed via Update feature)
   - Task 3: "Pending 2" (leave as pending)
   - Task 4: "Completed 2" (mark as completed)
   - Task 5: "Pending 3" (leave as pending)
2. Select "View Pending Tasks"

**Expected Result**:
```
You have 3 task(s)

[1] [ ] Pending 1
[3] [ ] Pending 2
[5] [ ] Pending 3
```

**Verification**:
- ✅ Only 3 tasks shown (tasks 1, 3, 5)
- ✅ All shown tasks have "[ ]" status
- ✅ Tasks 2 and 4 are NOT shown
- ✅ Tasks in ID ascending order

---

### Scenario 6: Filter Completed Tasks

**Goal**: Verify completed filter shows only finished tasks.

**Steps**:
1. Using the same 5 tasks from Scenario 5
2. Select "View Completed Tasks"

**Expected Result**:
```
You have 2 task(s)

[2] [✓] Completed 1
[4] [✓] Completed 2
```

**Verification**:
- ✅ Only 2 tasks shown (tasks 2, 4)
- ✅ All shown tasks have "[✓]" status
- ✅ Tasks 1, 3, 5 are NOT shown
- ✅ Tasks in ID ascending order

---

### Scenario 7: Empty Filter Results

**Goal**: Verify appropriate message when filter returns no results.

**Steps**:
1. Add 3 tasks, mark all as completed
2. Select "View Pending Tasks"

**Expected Result**:
```
No pending tasks found.
```

**Steps**:
1. Delete all tasks, add 2 new tasks, leave both as pending
2. Select "View Completed Tasks"

**Expected Result**:
```
No completed tasks found.
```

**Verification**:
- ✅ Context-specific empty messages appear
- ✅ No crash or confusing output

---

### Scenario 8: View Details - Non-Existent Task

**Goal**: Verify error handling for invalid task IDs.

**Steps**:
1. Add tasks with IDs 1, 2, 3
2. Select "View Task Details"
3. Enter task ID: 99

**Expected Result**:
```
Error: Task with ID 99 not found.
```

**Verification**:
- ✅ Clear error message
- ✅ Returns to main menu (no crash)
- ✅ User can try again

---

### Scenario 9: View Details - Invalid Input

**Goal**: Verify input validation for task ID.

**Test A - Non-numeric input**:
1. Select "View Task Details"
2. Enter: "abc"

**Expected Result**:
```
Error: Invalid task ID format. Please enter a number.
```

**Test B - Negative number**:
1. Select "View Task Details"
2. Enter: "-5"

**Expected Result**:
```
Error: Task ID must be a positive number.
```

**Test C - Zero**:
1. Select "View Task Details"
2. Enter: "0"

**Expected Result**:
```
Error: Task ID must be a positive number.
```

**Verification**:
- ✅ All invalid inputs show appropriate error
- ✅ Returns to menu after each error
- ✅ No crash

---

### Scenario 10: View After Delete

**Goal**: Verify view operations handle deleted tasks correctly.

**Steps**:
1. Add 3 tasks (IDs 1, 2, 3)
2. View all tasks (should show 3)
3. Delete task ID 2
4. View all tasks (should show 2)
5. Try to view details of task ID 2

**Expected Result - After Delete**:
```
You have 2 task(s)

[1] [ ] Task 1
[3] [ ] Task 3
```

**Expected Result - View Deleted Task**:
```
Error: Task with ID 2 not found.
```

**Verification**:
- ✅ Deleted task doesn't appear in list
- ✅ IDs 1 and 3 still appear
- ✅ Viewing deleted task ID shows error
- ✅ No crash or data corruption

---

## Automated Testing

### Run All View Tests

```bash
# Run all tests for view feature
pytest tests/unit/test_task_service_view.py -v
pytest tests/unit/test_display.py -v
pytest tests/contract/test_view_contracts.py -v
pytest tests/integration/test_view_integration.py -v
```

### Run Specific Test Scenarios

```bash
# Test empty list handling
pytest tests/unit/test_display.py::test_format_task_list_empty_all -v

# Test title truncation
pytest tests/unit/test_display.py::test_truncate_title_long -v

# Test filters
pytest tests/unit/test_task_service_view.py::test_filter_pending_tasks -v
pytest tests/unit/test_task_service_view.py::test_filter_completed_tasks -v

# Test detail view errors
pytest tests/integration/test_view_integration.py::test_view_task_details_non_existent_id -v
```

---

## Common Issues and Solutions

### Issue: Titles Not Truncating in List View

**Symptom**: Long titles display fully in "View All Tasks"

**Check**:
- Verify `truncate_title()` is called in `format_task_list()`
- Verify max_len=50 is used
- Check truncation logic: `title[:47] + "..."` for titles > 50 chars

---

### Issue: Wrong Tasks Shown in Filter

**Symptom**: Completed tasks appear in "View Pending" or vice versa

**Check**:
- Verify `filter_tasks_by_status()` filters on `task.completed` attribute
- Check filter parameter: `completed=False` for pending, `completed=True` for completed
- Verify update feature correctly sets `completed` attribute

---

### Issue: Tasks Not Sorted by ID

**Symptom**: Tasks appear in random order

**Check**:
- Verify all query methods use `sorted(tasks, key=lambda t: t.id)`
- Check that sorting happens before returning from TaskList methods

---

### Issue: Empty Messages Not Appearing

**Symptom**: Blank output when no tasks exist

**Check**:
- Verify `format_task_list()` checks `if not tasks:`
- Verify context parameter is passed correctly ("all", "pending", "completed")
- Check correct message for each context

---

### Issue: Timestamps Not Formatted

**Symptom**: Timestamps show as datetime objects instead of strings

**Check**:
- Verify `format_timestamp()` uses `strftime("%Y-%m-%d %H:%M:%S")`
- Check that `format_task_detail()` calls `format_timestamp()` for both created_at and updated_at

---

## Performance Testing

### Large List Test (100+ Tasks)

**Goal**: Verify view operations work with large task lists.

**Steps**:
1. Add 150 tasks programmatically (or manually if patient!)
2. View all tasks
3. Filter pending tasks
4. View details of task ID 75

**Expected**:
- All operations complete in <2 seconds
- No memory issues
- No formatting issues
- Console scrolling works correctly

---

## Edge Case Testing

1. **Special Characters**: Add task with title containing quotes, apostrophes, emojis - verify displays correctly
2. **Exactly 50 Chars**: Add task with title exactly 50 chars - verify no truncation
3. **Empty Description**: Add task with no description - verify detail view handles gracefully
4. **Rapid Operations**: View all → view details → filter → repeat quickly - verify no crashes
5. **After Multiple Deletes**: Delete tasks 2, 4, 6, 8 → verify remaining tasks (1, 3, 5, 7, 9) display correctly

---

## Test Checklist

Before submitting feature as complete:

- [ ] All 10 quick test scenarios pass
- [ ] All automated tests pass (unit, contract, integration)
- [ ] Title truncation works correctly (47 + "...")
- [ ] All empty states show appropriate messages
- [ ] Filters show correct tasks
- [ ] Detail view shows all fields without truncation
- [ ] Input validation catches all invalid IDs
- [ ] No crashes with any input combination
- [ ] Large list test (100+ tasks) passes
- [ ] Edge cases handled correctly

---

## Success Criteria

✅ **All view operations work as specified**
✅ **Clear, readable output formatting**
✅ **Appropriate error messages for all failure cases**
✅ **No application crashes with any input**
✅ **Performance <2s for all operations**
✅ **All automated tests pass**
