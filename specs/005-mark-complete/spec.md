# Feature Specification: Mark Task Complete in Todo App

**Feature Branch**: `005-mark-complete`
**Created**: 2025-12-06
**Status**: Ready for Planning
**Input**: User description: "Write specifications for the Mark Complete feature of the todo application - users should be able to mark tasks as complete and unmark them to reopen"

---

## Overview

This specification defines the "Mark Task Complete" feature for the todo application (Phase I). Users must be able to toggle task completion status - marking pending tasks as complete and unmarking completed tasks to reopen them.

**Phase I Constraint**: In-memory implementation only. No file persistence or database required.

**Dependencies**:
- Relies on Task and TaskList entities from `001-add-task`
- Integrates with task viewing from `004-view-task` (completion status display)
- May use update mechanisms from `003-update-task` (status field modification)

---

## User Scenarios & Testing

### User Story 1: Mark Pending Task as Complete (Priority: P1)
**As a** user  
**I want to** mark a pending task as complete  
**So that** I can track which tasks I have finished

**Why this priority**: Core functionality for task management workflow.

**Independent Test**: Create pending task, mark complete, verify status and timestamp updates.

**Acceptance Scenarios**:

1. **Mark single task complete by ID**
   - **Given** I have a pending task with ID 5
   - **When** I select "Mark Task Complete" and enter ID 5
   - **Then** Task status changes to "Completed" and timestamp updates

---

### User Story 2: Unmark Completed Task to Reopen (Priority: P1)
**As a** user  
**I want to** unmark a completed task to reopen it  
**So that** I can resume work on tasks needing more attention

**Why this priority**: Essential for workflow flexibility.

**Independent Test**: Complete a task, reopen it, verify status returns to "Pending".

**Acceptance Scenarios**:

1. **Reopen completed task**
   - **Given** I have a completed task with ID 3
   - **When** I select "Unmark Task Complete" and enter ID 3
   - **Then** Task status changes to "Pending" and timestamp updates

---

### User Story 3: Handle Invalid Operations (Priority: P2)
**As a** user  
**I want to** receive clear error messages when operations fail  
**So that** I understand what went wrong

**Why this priority**: Important for UX but not core to functionality.

**Independent Test**: Attempt invalid operations, verify error messages.

**Acceptance Scenarios**:

1. **Mark non-existent task**
   - **Given** My task list has IDs 1, 2, 3
   - **When** I try to mark task ID 99 as complete
   - **Then** I see error "Error: Task with ID 99 not found"

---

## Functional Requirements

**FR-001**: System MUST allow users to mark pending tasks as complete by ID
**FR-002**: System MUST allow users to unmark completed tasks to reopen them
**FR-003**: System MUST update "Last Updated" timestamp on status changes
**FR-004**: System MUST validate task ID before status changes
**FR-005**: System MUST check current task status before changing it
**FR-006**: System MUST display confirmation messages on successful status changes
**FR-007**: System MUST display clear error messages for all failure cases
**FR-008**: Completed tasks MUST display with "[✓] Completed" indicator
**FR-009**: Task detail view MUST show completion status clearly
**FR-010**: Filter operations MUST respect completion status
**FR-011**: Status changes MUST NOT modify other task fields (ID, title, description, created)
**FR-012**: Status changes MUST be atomic (all-or-nothing)
**FR-013**: Main menu MUST include "Mark Task Complete" option
**FR-014**: Main menu MUST include option to reopen completed tasks

---

## Success Criteria

**SC-001**: Status changes complete within 1 second
**SC-002**: 100% of valid operations update status correctly
**SC-003**: Timestamps accurate within ±1 second
**SC-004**: 100% of invalid inputs caught with appropriate errors
**SC-005**: 0 unintended field modifications during status changes
**SC-006**: 100% of users understand messages
**SC-007**: 0 crashes during 1000 operations
**SC-008**: Users can manage task lifecycle without friction

---

## Edge Cases

1. Mark task when list is empty → Error message
2. Rapid toggle operations → Each succeeds
3. Mark deleted task → Not found error
4. Very large task ID → Not found error
5. Task ID with leading zeros → Parsed correctly
6. Mark during view operations → Status updates immediately
7. Special characters in title → Status displays correctly
8. All tasks completed → Filters work correctly
9. No completed tasks → Empty message displays

---

## Key Entities

### Task (from 001-add-task)
- ID, Title, Description (immutable by this feature)
- **Status**: MODIFIED BY THIS FEATURE
- Created (immutable)
- **Last Updated**: MODIFIED BY THIS FEATURE

### TaskList (from 001-add-task)
- Operations: Add, Update, Delete, View, **Mark Complete/Unmark**

---

## Assumptions

1. Status stored as boolean completed field
2. UTC ISO 8601 timestamps
3. Single user (Phase I)
4. No completion history tracking
5. Idempotent UI for already-complete/pending
6. Menu labels may vary

---

## Out of Scope

- Completion history
- Undo/redo
- Bulk operations
- Scheduled completion
- Partial completion tracking
- Notifications
- Task dependencies
- Persistent storage

---

## Notes

- Modifies status and updated_at fields only
- Integrates with 004-view-task and 003-update-task
- Reversible operations
- No audit trail (Phase I)
- Console-based UI
- Error handling prevents crashes
