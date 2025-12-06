# Feature Specification: Mark Task Complete in Todo App

**Feature Branch**: `005-mark-complete`
**Created**: 2025-12-06
**Status**: Ready for Planning
**Input**: User description: "Write specification for the Mark Complete feature of the todo-application"

---

## Overview

This specification defines the "Mark Task Complete" feature for the todo application (Phase I). Users must be able to mark tasks as complete, unmark completed tasks to reopen them, view completion status clearly, and handle edge cases where marking operations fail.

**Phase I Constraint**: In-memory implementation only. No file persistence or database required.

**Dependencies**:
- Relies on Task and TaskList entities from `001-add-task`
- Assumes tasks can be created (001), updated (003), and deleted (002)

---

## User Scenarios & Testing

### User Story 1: View All Tasks (Priority: P1)
**As a** user
**I want to** view all tasks in my task list
**So that** I can see an overview of everything I need to do

**Why this priority**: Core viewing functionality - users need to see all their tasks to understand their workload.

**Acceptance Scenarios**:

1. **View all tasks when list has multiple tasks**
   - **Given** I have 5 tasks in my task list (mix of completed and pending)
   - **When** I select the "View All Tasks" option
   - **Then** I see all 5 tasks displayed with ID, title, and status

2. **View all tasks showing task IDs**
   - **Given** I have 3 tasks with IDs 1, 2, and 3
   - **When** I view all tasks
   - **Then** Each task displays its ID clearly

3. **View all tasks showing completion status**
   - **Given** I have 2 completed tasks and 3 pending tasks
   - **When** I view all tasks
   - **Then** Each task clearly indicates whether it is completed or pending

4. **View all tasks in order**
   - **Given** I have tasks added in a specific sequence
   - **When** I view all tasks
   - **Then** Tasks are displayed in a consistent order (by ID ascending)

5. **View all tasks showing truncated descriptions**
   - **Given** I have tasks with long descriptions (>50 characters)
   - **When** I view all tasks
   - **Then** Descriptions are truncated to keep the display clean

**Independent Test Description**: Create multiple tasks with varying titles, descriptions, and statuses. View all tasks and verify all fields display correctly with proper formatting.

---

### User Story 2: View Empty Task List (Priority: P1)
**As a** user
**I want to** see a helpful message when my task list is empty
**So that** I understand there are no tasks and know what to do next

**Why this priority**: Essential edge case - users must understand when they have no tasks rather than seeing confusing empty output.

**Acceptance Scenarios**:

1. **View tasks when list is empty**
   - **Given** I have no tasks in my task list
   - **When** I select "View All Tasks"
   - **Then** I see the message "No tasks found. Add a task to get started!"

2. **View tasks after deleting all tasks**
   - **Given** I had 3 tasks and deleted all of them
   - **When** I view all tasks
   - **Then** I see the empty list message

3. **View tasks on fresh application start**
   - **Given** I just started the application (no tasks created yet)
   - **When** I view all tasks
   - **Then** I see the empty list message

**Independent Test Description**: Start with an empty task list and verify the empty state message displays correctly. Then add tasks, delete them all, and verify the message reappears.

---

### User Story 3: View Single Task Details (Priority: P2)
**As a** user
**I want to** view the complete details of a single task
**So that** I can see the full title, description, status, and metadata without truncation

**Why this priority**: Important for understanding task details - the "view all" list may truncate information, so users need a detail view.

**Acceptance Scenarios**:

1. **View details of a task by ID**
   - **Given** I have a task with ID 5
   - **When** I select "View Task Details" and enter ID 5
   - **Then** I see the complete title, description, status, creation timestamp, and last updated timestamp

2. **View details showing full description**
   - **Given** I have a task with a 500-character description
   - **When** I view its details
   - **Then** I see the entire description without truncation

3. **View details of completed task**
   - **Given** I have a completed task
   - **When** I view its details
   - **Then** The status clearly shows "Completed"

4. **View details of pending task**
   - **Given** I have a pending task
   - **When** I view its details
   - **Then** The status clearly shows "Pending"

5. **Attempt to view details of non-existent task**
   - **Given** I have tasks with IDs 1, 2, 3
   - **When** I try to view details for ID 99
   - **Then** I see error message "Error: Task with ID 99 not found"

**Independent Test Description**: Create tasks with various description lengths. View details for each and verify all fields display completely. Test with invalid IDs to verify error handling.

---

### User Story 4: Filter Tasks by Status (Priority: P2)
**As a** user
**I want to** filter tasks by completion status (completed or pending)
**So that** I can focus on only the tasks that are relevant to my current needs

**Why this priority**: Improves usability - users often want to see only pending tasks (to know what's left) or only completed tasks (to review what's done).

**Acceptance Scenarios**:

1. **Filter to show only pending tasks**
   - **Given** I have 3 pending tasks and 2 completed tasks
   - **When** I select "View Pending Tasks"
   - **Then** I see only the 3 pending tasks

2. **Filter to show only completed tasks**
   - **Given** I have 3 pending tasks and 2 completed tasks
   - **When** I select "View Completed Tasks"
   - **Then** I see only the 2 completed tasks

3. **Filter pending tasks when all tasks are completed**
   - **Given** All my tasks are completed
   - **When** I select "View Pending Tasks"
   - **Then** I see message "No pending tasks found"

4. **Filter completed tasks when all tasks are pending**
   - **Given** All my tasks are pending
   - **When** I select "View Completed Tasks"
   - **Then** I see message "No completed tasks found"

5. **Filter tasks preserves all display fields**
   - **Given** I have pending and completed tasks
   - **When** I filter by any status
   - **Then** The filtered results show ID, title, and status for each matching task

**Independent Test Description**: Create mix of completed and pending tasks. Test each filter option and verify only matching tasks appear. Verify messages for empty filter results.

---

### User Story 5: Handle View Errors Gracefully (Priority: P2)
**As a** user
**I want to** receive clear error messages when viewing operations fail
**So that** I understand what went wrong and can take corrective action

**Why this priority**: Essential for good user experience - users must understand when and why view operations fail.

**Acceptance Scenarios**:

1. **View details with invalid task ID format**
   - **Given** I am viewing task details
   - **When** I enter "abc" instead of a number
   - **Then** I see error "Error: Invalid task ID format. Please enter a number."

2. **View details with negative task ID**
   - **Given** I am viewing task details
   - **When** I enter "-5"
   - **Then** I see error "Error: Task ID must be a positive number."

3. **View details with zero task ID**
   - **Given** I am viewing task details
   - **When** I enter "0"
   - **Then** I see error "Error: Task ID must be a positive number."

4. **View details with non-existent task ID**
   - **Given** My task list has IDs 1, 2, 3
   - **When** I try to view task ID 100
   - **Then** I see error "Error: Task with ID 100 not found."

5. **Recover from view error**
   - **Given** I received an error viewing a task
   - **When** The error is displayed
   - **Then** I am returned to the main menu and can continue using the application

**Independent Test Description**: Test all invalid inputs (non-numeric, negative, zero, non-existent IDs) and verify appropriate error messages. Verify application remains stable after errors.

---

## Functional Requirements

### Display Requirements

**FR-001: Display All Tasks**
- **Description**: When user selects "View All Tasks", system displays all tasks in the task list
- **Acceptance**:
  - All tasks are shown
  - Each task shows: ID, title (truncated to 50 chars if needed), status
  - Tasks are ordered by ID ascending
- **Example**: User has 5 tasks → all 5 tasks appear in the list

**FR-002: Display Task ID**
- **Description**: Each task in the list view displays its unique ID
- **Acceptance**:
  - ID is displayed prominently
  - ID is numeric and matches the task's actual ID
- **Example**: Task with ID 7 shows "7" clearly in the display

**FR-003: Display Task Title**
- **Description**: Each task in the list view displays its title
- **Acceptance**:
  - Title is displayed
  - If title exceeds 50 characters, it is truncated with "..." appended
- **Example**: Title "Buy groceries" shows as "Buy groceries", but "This is a very long task title that exceeds fifty characters" shows as "This is a very long task title that exceeds fif..."

**FR-004: Display Task Status**
- **Description**: Each task in the list view displays its completion status
- **Acceptance**:
  - Status is displayed as "Completed" or "Pending"
  - Status is clearly distinguishable
- **Example**: Completed task shows "[✓] Completed", pending shows "[ ] Pending"

**FR-005: Display Empty List Message**
- **Description**: When task list is empty, system displays a helpful message
- **Acceptance**:
  - Message is "No tasks found. Add a task to get started!"
  - No task list is shown (since there are no tasks)
- **Example**: New user views tasks → sees empty message

**FR-006: Display Task Count**
- **Description**: When displaying all tasks, system shows total count
- **Acceptance**:
  - Count is displayed before the task list
  - Format: "You have X task(s)"
- **Example**: "You have 5 task(s)" appears above the list

### Detail View Requirements

**FR-007: View Single Task Details**
- **Description**: User can view complete details of a specific task by ID
- **Acceptance**:
  - User is prompted to enter task ID
  - System retrieves and displays the task
- **Example**: User enters ID 3 → sees all details of task 3

**FR-008: Display Full Title in Details**
- **Description**: Detail view shows complete task title without truncation
- **Acceptance**:
  - Entire title is displayed regardless of length
  - No "..." truncation
- **Example**: 200-character title displays completely in detail view

**FR-009: Display Full Description in Details**
- **Description**: Detail view shows complete task description without truncation
- **Acceptance**:
  - Entire description is displayed regardless of length
  - Multi-line descriptions preserve line breaks
- **Example**: 1000-character description displays completely

**FR-010: Display Status in Details**
- **Description**: Detail view shows task completion status
- **Acceptance**:
  - Status is clearly labeled as "Status: Completed" or "Status: Pending"
- **Example**: Completed task shows "Status: Completed"

**FR-011: Display Timestamps in Details**
- **Description**: Detail view shows creation and last updated timestamps
- **Acceptance**:
  - Creation timestamp is displayed
  - Last updated timestamp is displayed
  - Format is human-readable (e.g., "2025-12-06 14:30:00")
- **Example**: "Created: 2025-12-06 10:00:00, Last Updated: 2025-12-06 14:30:00"

### Filter Requirements

**FR-012: Filter Pending Tasks**
- **Description**: User can view only pending (incomplete) tasks
- **Acceptance**:
  - Only tasks with status "Pending" are displayed
  - Display format matches "View All Tasks" format
- **Example**: User has 3 pending and 2 completed → only 3 pending tasks shown

**FR-013: Filter Completed Tasks**
- **Description**: User can view only completed tasks
- **Acceptance**:
  - Only tasks with status "Completed" are displayed
  - Display format matches "View All Tasks" format
- **Example**: User has 3 pending and 2 completed → only 2 completed tasks shown

**FR-014: Filter Empty Result Message**
- **Description**: When filter returns no tasks, display appropriate message
- **Acceptance**:
  - For pending filter: "No pending tasks found."
  - For completed filter: "No completed tasks found."
- **Example**: All tasks completed → pending filter shows "No pending tasks found."

**FR-015: Filter Preserves Sort Order**
- **Description**: Filtered tasks maintain the same sort order as full list (ID ascending)
- **Acceptance**:
  - Filtered tasks are sorted by ID ascending
- **Example**: Pending tasks with IDs 1, 5, 8 appear in that order

### Input Validation Requirements

**FR-016: Validate Task ID Format**
- **Description**: When user enters task ID for detail view, system validates format
- **Acceptance**:
  - Only numeric input is accepted
  - Non-numeric input produces error: "Error: Invalid task ID format. Please enter a number."
- **Example**: User enters "abc" → sees format error

**FR-017: Validate Task ID Range**
- **Description**: System validates task ID is positive
- **Acceptance**:
  - Zero and negative numbers are rejected
  - Error message: "Error: Task ID must be a positive number."
- **Example**: User enters "-5" → sees range error

**FR-018: Validate Task Existence**
- **Description**: System validates task ID exists before showing details
- **Acceptance**:
  - If task ID not found, error message: "Error: Task with ID [X] not found."
- **Example**: User enters ID 99 (doesn't exist) → sees not found error

### Error Handling Requirements

**FR-019: Handle Non-Existent Task Gracefully**
- **Description**: When user tries to view non-existent task, system shows error and returns to menu
- **Acceptance**:
  - Error message is displayed
  - User returns to main menu
  - Application does not crash
- **Example**: User enters invalid ID → sees error → can continue using app

**FR-020: Handle Empty List Gracefully**
- **Description**: Viewing empty list does not cause errors
- **Acceptance**:
  - Empty message is displayed
  - No error or crash occurs
  - User returns to main menu
- **Example**: User views tasks when list empty → sees helpful message

**FR-021: Handle Invalid Input Gracefully**
- **Description**: Invalid input during view operations shows error and allows retry
- **Acceptance**:
  - Error message is clear
  - User is returned to menu (can try again)
  - No application crash
- **Example**: User enters "xyz" as ID → sees error → can select menu option again

### Display Formatting Requirements

**FR-022: Consistent Task Display Format**
- **Description**: All list views use consistent formatting
- **Acceptance**:
  - Same format for "View All", "View Pending", "View Completed"
  - Format: "[ID] [Status Icon] Title (truncated if needed)"
- **Example**: "[3] [✓] Buy groceries" for completed task

**FR-023: Detail View Formatting**
- **Description**: Detail view uses clear label-value pairs
- **Acceptance**:
  - Each field has a clear label (ID:, Title:, Description:, Status:, Created:, Last Updated:)
  - Values are aligned and easy to read
- **Example**:
  ```
  ID: 5
  Title: Buy groceries
  Description: Get milk, bread, eggs from the store
  Status: Pending
  Created: 2025-12-06 10:00:00
  Last Updated: 2025-12-06 10:00:00
  ```

**FR-024: Title Truncation Rules**
- **Description**: Titles in list view are truncated at 50 characters
- **Acceptance**:
  - Titles <= 50 chars: displayed fully
  - Titles > 50 chars: first 47 chars + "..."
  - Detail view always shows full title
- **Example**: "This is a very long task title that exceeds the fifty character limit" → "This is a very long task title that exceeds ..."

---

## Success Criteria

**SC-001: View All Tasks Performance**
- **Metric**: Time to display all tasks
- **Target**: All tasks displayed within 2 seconds
- **Measurement**: User selects "View All Tasks" → complete list appears ≤ 2 seconds

**SC-002: View Details Performance**
- **Metric**: Time to display single task details
- **Target**: Task details displayed within 2 seconds after entering valid ID
- **Measurement**: User enters ID → details appear ≤ 2 seconds

**SC-003: Empty List Handling**
- **Metric**: Correct empty state message
- **Target**: 100% of empty list scenarios show proper message
- **Measurement**: Test empty list on startup, after deleting all tasks → verify message appears

**SC-004: Data Display Accuracy**
- **Metric**: All task fields display correctly
- **Target**: 100% accuracy in displaying ID, title, description, status, timestamps
- **Measurement**: Create tasks with various data → verify all fields match expected values

**SC-005: Filter Accuracy**
- **Metric**: Filters show correct tasks
- **Target**: 100% of filtered tasks match the filter criteria
- **Measurement**: Create mix of completed/pending → verify each filter shows only matching tasks

**SC-006: Error Detection**
- **Metric**: Invalid inputs are caught and reported
- **Target**: 100% of invalid inputs (non-numeric, negative, zero, non-existent) show appropriate error
- **Measurement**: Test all invalid input types → verify correct error messages

**SC-007: Application Stability**
- **Metric**: View operations do not crash application
- **Target**: 0 crashes during view operations
- **Measurement**: Perform 100 view operations (valid and invalid inputs) → verify no crashes

**SC-008: User Experience**
- **Metric**: Clear, readable display formatting
- **Target**: All tasks and details are easy to read and understand
- **Measurement**: Manual review of display output → verify clarity, alignment, readability

---

## Edge Cases

1. **Empty Task List on Startup**
   - **Scenario**: User launches app for first time and views tasks
   - **Expected**: Empty message displays correctly

2. **View Task After Deletion**
   - **Scenario**: User views details of task ID 5, then deletes it, then tries to view it again
   - **Expected**: Second view attempt shows "Task not found" error

3. **Very Long Titles (>200 characters)**
   - **Scenario**: Task has 300-character title
   - **Expected**: List view truncates at 50 chars, detail view shows all 300 chars

4. **Very Long Descriptions (>1000 characters)**
   - **Scenario**: Task has 2000-character description
   - **Expected**: Detail view displays all 2000 characters

5. **Special Characters in Title/Description**
   - **Scenario**: Title contains quotes, apostrophes, emojis
   - **Expected**: All characters display correctly without encoding issues

6. **Filter When All Tasks Same Status**
   - **Scenario**: All tasks are completed, user filters for pending
   - **Expected**: "No pending tasks found" message displays

7. **Large Number of Tasks (100+)**
   - **Scenario**: User has 150 tasks and views all
   - **Expected**: All 150 tasks display (may require scrolling in console)

8. **Task ID with Leading Zeros**
   - **Scenario**: User enters "007" when trying to view task 7
   - **Expected**: System interprets as 7 and displays task 7 (numeric parsing handles leading zeros)

9. **Rapid View Operations**
   - **Scenario**: User views all tasks, then details, then filter multiple times quickly
   - **Expected**: Each operation completes correctly without data corruption or crashes

---

## Key Entities

### Task (defined in 001-add-task)
- **ID**: Unique numeric identifier (auto-incremented)
- **Title**: User-provided task title (1-200 characters)
- **Description**: User-provided task description (0-1000 characters, optional)
- **Status**: Completion status ("Pending" or "Completed")
- **Created**: Timestamp of task creation
- **Last Updated**: Timestamp of last modification

### TaskList (defined in 001-add-task)
- **Tasks**: Collection of Task objects
- **Operations**: Add, Update (003), Delete (002), View (this feature)

---

## Out of Scope

- Sorting tasks by criteria other than ID (e.g., by creation date, title)
- Searching tasks by keyword
- Pagination of task list
- Exporting task list to file
- Calendar or date-based views
- Task categories or tags
- Persistent storage (Phase II feature)

---

## Notes

- This specification focuses on viewing tasks that already exist (created via 001-add-task)
- Viewing is read-only - this feature does not modify tasks
- All view operations work with in-memory data only (Phase I constraint)
- The UI remains console-based for Phase I
- Display formatting should be clear and consistent across all view types
- Error handling must ensure application never crashes due to view operations
