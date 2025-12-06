# Feature Specification: Update Task in Todo App

**Feature Branch**: `003-update-task`
**Created**: 2025-12-06
**Status**: Ready for Planning
**Input**: User description: "Write specification for update feature of todo app"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Update Task Title (Priority: P1)

A user wants to modify the title of an existing task to correct a typo, add clarification, or update the task name as requirements change. This is the most common update operation.

**Why this priority**: This is the minimum viable update functionality. Users frequently need to correct typos or refine task names as they work. Without title editing, users must delete and recreate tasks, losing creation timestamps and context.

**Independent Test**: Can be fully tested by adding tasks, selecting "Update Task", entering a task ID, choosing to update the title, entering a new title, and verifying the change appears in the task list. Delivers standalone value as basic task modification functionality.

**Acceptance Scenarios**:

1. **Given** the task list contains task #5 with title "Buy grocceries", **When** user selects "Update Task", enters ID "5", chooses to update title, and enters new title "Buy groceries", **Then** system updates task #5 with the corrected title, preserves all other attributes (ID, description, status, timestamp), and displays confirmation "Task #5 title updated successfully"
2. **Given** user has just updated a task title, **When** user views the task list, **Then** the task appears with the new title while maintaining its original position, ID, and other attributes
3. **Given** the task list contains multiple tasks, **When** user updates one task title, **Then** all other tasks remain unchanged in content and order
4. **Given** user is updating a task title, **When** user enters a new title with maximum allowed characters (200 characters), **Then** system accepts the full title and updates the task successfully
5. **Given** user is at the update title prompt, **When** user enters a valid new title, **Then** system replaces the old title entirely (no merging or appending)

---

### User Story 2 - Update Task Description (Priority: P2)

A user wants to modify the description of an existing task to add more details, correct information, or update context as the task evolves.

**Why this priority**: While less common than title updates, description editing is important for maintaining accurate task context. Users often need to add details after initially creating a task or update instructions as circumstances change.

**Independent Test**: Can be tested by adding tasks with descriptions, selecting "Update Task", choosing to update description, entering new description, and verifying the change. Delivers value by enabling detailed task context management.

**Acceptance Scenarios**:

1. **Given** task #3 has description "Old details", **When** user selects "Update Task", enters ID "3", chooses to update description, and enters "Updated details with more information", **Then** system updates task #3 description, preserves title and other attributes, and displays confirmation "Task #3 description updated successfully"
2. **Given** task #7 has no description (empty/None), **When** user updates task #7 and adds a description "New description added", **Then** system adds the description to the previously description-less task
3. **Given** task #4 has a description, **When** user updates task #4 and enters an empty description (just presses Enter), **Then** system removes the description, leaving the task with title only and no description
4. **Given** user is updating a description, **When** user enters a multi-line description (spanning 3 lines), **Then** system accepts the full multi-line description up to maximum character limit (1000 characters)
5. **Given** user is updating a description, **When** user enters maximum allowed characters (1000 characters), **Then** system accepts the full description and updates successfully

---

### User Story 3 - Update Task Completion Status (Priority: P1)

A user wants to toggle a task's completion status from incomplete to complete (or vice versa) to track progress and manage their workflow.

**Why this priority**: Status toggling is essential for todo list functionality. Users need to mark tasks as done when completed and sometimes reopen tasks if they need to be redone. This is core to task management.

**Independent Test**: Can be tested by creating tasks, marking them complete, verifying status changes, unmarking them, and verifying the cycle. Delivers standalone value as task progress tracking.

**Acceptance Scenarios**:

1. **Given** task #2 is marked as incomplete (status=False), **When** user selects "Update Task", enters ID "2", and chooses to toggle completion status, **Then** system marks task #2 as complete (status=True) and displays "Task #2 marked as complete"
2. **Given** task #6 is marked as complete (status=True), **When** user toggles its completion status, **Then** system marks task #6 as incomplete (status=False) and displays "Task #6 marked as incomplete"
3. **Given** user marks a task as complete, **When** user views the task list, **Then** the task displays with visual indicator showing completed status (e.g., "[✓] Task title" or "Status: Complete")
4. **Given** user toggles a task status multiple times, **When** each toggle operation completes, **Then** system correctly alternates between complete and incomplete states
5. **Given** user updates a task status, **When** status changes, **Then** task title, description, ID, and creation timestamp remain unchanged

---

### User Story 4 - Update Multiple Task Fields in One Operation (Priority: P3)

A user wants to update both title and description (or other combinations) in a single operation rather than making multiple sequential updates.

**Why this priority**: Convenience feature that improves user experience but is not essential. Users can achieve the same result through multiple update operations, making this lower priority.

**Independent Test**: Can be tested by selecting to update multiple fields, verifying all changes apply simultaneously. Delivers value by streamlining the update workflow.

**Acceptance Scenarios**:

1. **Given** task #8 has title "Old Title" and description "Old Desc", **When** user selects "Update Task", enters ID "8", chooses to update multiple fields, updates title to "New Title" and description to "New Desc", **Then** system updates both fields simultaneously and displays "Task #8 updated successfully (2 fields modified)"
2. **Given** user is in multi-field update mode, **When** user chooses to update only some fields (e.g., title only) and skips others, **Then** system updates selected fields and leaves unselected fields unchanged
3. **Given** user updates multiple fields, **When** one field has validation error (e.g., title too long), **Then** system displays error, cancels all updates for that task, and prompts user to retry without partial updates
4. **Given** user completes multi-field update, **When** confirmation is displayed, **Then** message lists all fields that were modified (e.g., "Updated: title, description")

---

### User Story 5 - Handle Update Errors Gracefully (Priority: P2)

A user encounters an error during task update (e.g., invalid task ID, empty title, oversized text) and receives clear guidance on how to correct the issue.

**Why this priority**: Error handling ensures application reliability and prevents data corruption. While less critical than core update functionality, it prevents user frustration and maintains data quality.

**Independent Test**: Can be tested by deliberately entering invalid inputs and verifying appropriate error messages appear without corrupting existing data. Delivers value by preventing bad updates and guiding users.

**Acceptance Scenarios**:

1. **Given** the task list contains tasks 1, 2, 3, **When** user attempts to update task ID "99" (non-existent), **Then** system displays error "Error: Task #99 not found. Please enter a valid task ID." and returns to menu without modifying any task
2. **Given** user is updating a task title, **When** user enters empty title (blank/whitespace only), **Then** system displays error "Error: Task title cannot be empty. Please enter a valid title." and prompts again without applying the update
3. **Given** user is updating a task title, **When** user enters title exceeding 200 characters, **Then** system displays error "Error: Task title too long (maximum 200 characters)." and prompts for valid input
4. **Given** user is updating a task description, **When** user enters description exceeding 1000 characters, **Then** system displays error "Error: Description too long (maximum 1000 characters)." and prompts for valid input
5. **Given** user is in update flow, **When** user enters "cancel" at any prompt, **Then** system discards all changes, displays "Update cancelled", and returns to main menu with original task data intact
6. **Given** user encounters a validation error, **When** error is displayed, **Then** message includes specific constraint violated, maximum/minimum values, and clear instruction on how to fix
7. **Given** validation error occurs during update, **When** user is re-prompted, **Then** system shows the current/original value so user knows what they're replacing

---

### Edge Cases

- What happens when user tries to update a task that was just deleted by another operation?
- How does system handle updating a task title to be identical to another existing task's title?
- What happens when user enters special characters or unicode in updated title/description?
- How does system handle very long titles/descriptions in update confirmation messages (truncation)?
- What happens when user tries to update with leading or trailing whitespace?
- How does system behave during rapid consecutive updates to the same task?
- What happens when user provides task ID with special characters (e.g., "#5" or "5.")?
- How does system handle updating task ID with leading zeros (e.g., "007" for task #7)?
- What happens when the task list is empty and user tries to update?


## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide an "Update Task" option in the main menu
  - **Acceptance**: User can navigate to "Update Task" option from main menu
  - **Example**: User types "3" (or "update") at main menu, system initiates update flow

- **FR-002**: System MUST prompt user to enter the ID of the task to update
  - **Acceptance**: After selecting "Update Task", system displays "Enter task ID to update:" prompt
  - **Example**: Console shows "Enter task ID to update: " and cursor waits for input

- **FR-003**: System MUST validate that the entered task ID is numeric
  - **Acceptance**: If user enters non-numeric input, system rejects with error and re-prompts
  - **Example**: User enters "abc", system shows "Error: Invalid task ID. Please enter a numeric ID."

- **FR-004**: System MUST validate that the task ID exists in the current task list
  - **Acceptance**: If ID does not exist, system displays specific error with the attempted ID
  - **Example**: User enters "99" when only IDs 1-5 exist, system shows "Error: Task #99 not found"

- **FR-005**: System MUST display the current task details before prompting for updates
  - **Acceptance**: After valid ID entry, system shows current title, description, and status
  - **Example**: Console displays current task information: title, description, completion status

- **FR-006**: System MUST present user with update options menu
  - **Acceptance**: System displays menu with options for updating title, description, or status
  - **Example**: User sees options: "1. Update title  2. Update description  3. Toggle status  4. Cancel"

- **FR-007**: System MUST allow user to update task title
  - **Acceptance**: When user selects title update, system prompts for new title and updates it
  - **Example**: User selects option 1, enters "New Title", system updates title only

- **FR-008**: System MUST validate new task title is not empty
  - **Acceptance**: If user submits empty title, system rejects with error and re-prompts
  - **Example**: User enters empty string, system shows "Error: Task title cannot be empty"

- **FR-009**: System MUST enforce maximum 200 characters for updated titles
  - **Acceptance**: If user enters 201+ characters, system rejects with error
  - **Example**: System shows "Error: Task title too long (maximum 200 characters)"

- **FR-010**: System MUST trim leading and trailing whitespace from updated titles
  - **Acceptance**: Title with extra spaces is stored without leading/trailing whitespace
  - **Example**: "  New Title  " is stored as "New Title"

- **FR-011**: System MUST allow user to update task description
  - **Acceptance**: When user selects description update, system prompts for new description
  - **Example**: User selects option 2, enters new description, system updates description only

- **FR-012**: System MUST allow user to clear task description by entering empty value
  - **Acceptance**: Entering empty description removes it from the task
  - **Example**: User presses Enter without text, description is set to None/empty

- **FR-013**: System MUST enforce maximum 1000 characters for updated descriptions
  - **Acceptance**: If user enters 1001+ characters, system rejects with error
  - **Example**: System shows "Error: Description too long (maximum 1000 characters)"

- **FR-014**: System MUST allow user to toggle task completion status
  - **Acceptance**: When user selects status toggle, system flips between complete/incomplete
  - **Example**: Incomplete task becomes complete; complete task becomes incomplete

- **FR-015**: System MUST display appropriate confirmation based on new status
  - **Acceptance**: Confirmation message reflects the new status
  - **Example**: "Task #5 marked as complete" or "Task #5 marked as incomplete"

- **FR-016**: System MUST preserve task ID when updating any field
  - **Acceptance**: Task ID never changes during any update operation
  - **Example**: Updating task #5 title, description, or status keeps ID as 5

- **FR-017**: System MUST preserve task creation timestamp when updating
  - **Acceptance**: Creation timestamp remains unchanged after any update
  - **Example**: Task created 2025-12-05 retains that timestamp after 2025-12-06 update

- **FR-018**: System MUST preserve unmodified fields when updating specific fields
  - **Acceptance**: Updating one field leaves other fields unchanged
  - **Example**: Updating title preserves description and status

- **FR-019**: System MUST display success confirmation after update
  - **Acceptance**: After successful update, user sees confirmation with task ID
  - **Example**: "Task #5 title updated successfully"

- **FR-020**: System MUST return user to main menu after successful update
  - **Acceptance**: After confirmation message, main menu is displayed
  - **Example**: User sees success message, then main menu options

- **FR-021**: System MUST allow user to cancel update operation
  - **Acceptance**: Typing "cancel" at any prompt cancels and returns to menu
  - **Example**: User types "cancel", sees "Update cancelled", returns to menu

- **FR-022**: System MUST handle empty task list scenario
  - **Acceptance**: If list is empty, shows message and returns to menu
  - **Example**: "No tasks available to update" message displayed

- **FR-023**: System MUST handle special characters, unicode, and emoji
  - **Acceptance**: Updated tasks can contain special characters
  - **Example**: "Review Maria's presentation 📊" is stored correctly

- **FR-024**: System MUST handle task ID input with leading zeros
  - **Acceptance**: Leading zeros are ignored when parsing task ID
  - **Example**: "007" is treated as task ID 7

### Key Entities

- **Task**: Represents a single todo item (defined in 001-add-task)
  - **Attributes**: ID (immutable), title (updatable), description (updatable), status (updatable), timestamp (immutable)
  - **Update Behavior**: Fields can be updated individually; ID and timestamp never change; unmodified fields preserved

- **Task List**: In-memory collection of tasks (defined in 001-add-task)
  - **Update Behavior**: Task modified in-place; no reordering; all data preserved

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can update task title in under 10 seconds
  - **Measurement**: Timed testing from menu selection to confirmation

- **SC-002**: Users can toggle completion status in under 5 seconds
  - **Measurement**: Timed testing from menu selection to confirmation

- **SC-003**: System rejects 100% of invalid updates with clear error messages
  - **Measurement**: Automated tests with invalid inputs verify error handling

- **SC-004**: System maintains 100% data integrity after updates
  - **Measurement**: Automated tests verify unchanged fields remain intact

- **SC-005**: Users successfully update tasks without data corruption in 100% of operations
  - **Measurement**: Automated tests with hundreds of update operations

- **SC-006**: Users recover from update errors without external help
  - **Measurement**: User testing tracks self-correction success rate

- **SC-007**: Users can cancel operations and return to menu in under 2 seconds
  - **Measurement**: Timed testing of cancel functionality

- **SC-008**: System displays current values before updates in 100% of cases
  - **Measurement**: Automated tests verify prompts show existing data
