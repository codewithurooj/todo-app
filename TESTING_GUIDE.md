# Todo App - Testing Guide

## Quick Start

You are now on the **main** branch with ALL 5 features fully integrated!

### Current Branch Status
```bash
git branch
# * main  <- You should see this
```

## How to Test the App

### Option 1: Run the Interactive CLI App

```bash
python main.py
```

This will launch the interactive menu where you can manually test all features:

```
==================================================
           MAIN MENU
==================================================
  1. Add Task
  2. View Tasks
  3. Update Task
  4. Delete Task
  5. Mark Task Complete
  6. Reopen Completed Task
  0. Exit
==================================================
```

**Try this workflow:**

1. **Add some tasks** (Option 1)
   - Add task with title only
   - Add task with title and description

2. **View all tasks** (Option 2)
   - See all your tasks listed

3. **Update a task** (Option 3)
   - Change a task title
   - Update a description
   - Toggle completion status

4. **Mark tasks complete** (Option 5)
   - Mark a task as complete
   - View tasks again to see status changed

5. **Reopen a task** (Option 6)
   - Reopen a completed task

6. **Delete a task** (Option 4)
   - Delete a task by ID
   - Verify it's gone from the list

7. **Exit** (Option 0)

### Option 2: Run the Automated Test Script

```bash
python test_all_features.py
```

This will automatically test all 5 features and show you the results:

```
============================================================
TESTING ALL TODO APP FEATURES - PHASE I
============================================================

[OK] Test 1: ADD TASK
[OK] Test 2: VIEW ALL TASKS
[OK] Test 3: UPDATE TASK
[OK] Test 4: MARK COMPLETE
[OK] Test 5: FILTER TASKS BY STATUS
[OK] Test 6: DELETE TASK
[OK] Test 7: ERROR HANDLING

============================================================
ALL FEATURES TESTED SUCCESSFULLY!
============================================================
```

## All Available Features

### ✅ Feature 001: Add Task
- Create tasks with title (required)
- Add optional description
- Automatic ID assignment
- Input validation
- Cancel support

### ✅ Feature 002: Delete Task
- Delete by task ID
- Confirmation prompt
- ID preservation (no renumbering)
- Error handling for invalid IDs

### ✅ Feature 003: Update Task
- Update task title
- Update task description
- Toggle completion status
- Field validation

### ✅ Feature 004: View Tasks
- View all tasks
- Display with ID, title, status
- Empty list handling
- Filter by completion status

### ✅ Feature 005: Mark Complete
- Mark pending tasks complete
- Reopen completed tasks
- Idempotent operations
- Timestamp tracking

## Switching Between Branches (if needed)

If you want to test individual features in isolation:

```bash
# View all branches
git branch -a

# Switch to a feature branch
git checkout 001-add-task      # Only Add Task feature
git checkout 002-delete-task   # Add + Delete features
git checkout 003-update-task   # Add + Delete + Update features
git checkout 004-view-task     # Add + Delete + Update + View features
git checkout 005-mark-complete # All 5 features

# Return to main (all features)
git checkout main
```

## Verify Your Current Setup

Run this to confirm you have all features:

```bash
# Check you're on main branch
git branch

# Check all CLI functions exist
python -c "from src.cli.task_cli import add_task_cli, delete_task_cli, update_task_cli, view_all_tasks_cli, mark_complete_cli, reopen_task_cli; print('All features available!')"

# Run automated tests
python test_all_features.py
```

## Branch Structure

```
main (ALL FEATURES)
  |
  └── 005-mark-complete (merged)
        |
        └── 004-view-task (merged)
              |
              └── 003-update-task (merged)
                    |
                    └── 002-delete-task (merged)
                          |
                          └── 001-add-task (merged)
```

The **main** branch now contains the complete, cumulative implementation of all features!

## Technical Details

- **Language**: Python 3.13+
- **Storage**: In-memory (tasks lost on exit - Phase I limitation)
- **Architecture**: CRUD operations with TaskList and Task models
- **All files**:
  - `main.py` - Application entry point
  - `src/models/task.py` - Task and TaskList classes
  - `src/cli/task_cli.py` - All CLI handlers
  - `src/utils/validators.py` - Input validation
  - `test_all_features.py` - Automated test script

## Next Steps

Now that you have all features working on main:

1. **Test thoroughly** using both manual and automated methods
2. **Phase II**: Add file persistence (coming soon)
3. **Phase III**: REST API with FastAPI (future)

Enjoy your fully functional todo app! 🎉
