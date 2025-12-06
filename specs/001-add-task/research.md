# Technical Research: Add Task Feature

**Feature**: 001-add-task
**Date**: 2025-12-06
**Status**: Completed

## Overview

This document captures technical research and decisions made during the planning phase for the Add Task feature. All decisions prioritize simplicity (Phase I constraints) while maintaining evolvability for future phases.

---

## 1. Task ID Generation Strategy

### Decision

**Choice**: Sequential integer IDs starting from 1

**Rationale**:
- Simplest solution for Phase I in-memory application
- Human-readable and easy to reference in console UI
- Predictable ordering matches task creation sequence
- No external dependencies required
- Sufficient for single-user, non-distributed Phase I

**Alternatives Considered**:
- **UUID**: Globally unique but harder to remember/type in console, overkill for Phase I
- **Timestamp-based**: Natural ordering but collision risk if tasks created rapidly
- **Hash-based**: Unique content signatures but complex, harder to reference

**Implementation**: Simple counter in TaskList class, increments on each task creation

**Evolution Path**: Phase IV (distributed system) will require UUIDs or distributed ID generation (Snowflake pattern).

---

## 2. Timestamp Format & Timezone Handling

### Decision

**Choice**: UTC timestamps stored as datetime objects, ISO 8601 for display

**Rationale**:
- UTC avoids timezone ambiguity
- Python datetime stdlib sufficient for Phase I
- ISO 8601 format (YYYY-MM-DDTHH:MM:SS) is human-readable and standard
- Consistent with future API evolution

**Evolution Path**: Phase III (REST API) will leverage existing ISO 8601 format.

---

## 3. Input Validation Patterns

### Decision

**Choice**: Dedicated validator functions with clear error messages

**Rationale**:
- Testable in isolation (unit tests)
- Reusable across different entry points
- Separates validation logic from business logic
- No external dependencies (built-in Python only)

**Evolution Path**: Phase III (REST API) may adopt Pydantic for request validation.

---

## 4. Data Structure Choice

### Decision

**Choice**: List of Task objects (dataclass-based)

**Rationale**:
- Object-oriented design matches future class-based evolution
- Type hints provide IDE support and mypy checking
- Dataclass reduces boilerplate
- List preserves insertion order

**Evolution Path**: Phase II can serialize to JSON, Phase IV can map to ORM models.

---

## 5. Testing Strategy

### Decision

**Choice**: pytest with capsys fixture for I/O testing

**Rationale**:
- pytest is Python standard for modern testing
- capsys fixture captures stdout/stdin for CLI testing
- Clear separation: unit tests (models/validators), integration tests (full flows)
- No mocking for simple Phase I logic

**Evolution Path**: Phase III adds contract tests with OpenAPI schema validation.

---

## 6. Error Handling Strategy

### Decision

**Choice**: Clear error messages with recovery prompts (no exceptions for user errors)

**Rationale**:
- User input errors are expected, not exceptional
- Clear error messages guide users to correct input
- Loop-based prompts allow retry without exiting flow

**Evolution Path**: REST API (Phase III) will use HTTP status codes (400 for validation errors).

---

## 7. Character Encoding & Special Characters

### Decision

**Choice**: UTF-8 encoding with full Unicode support

**Rationale**:
- Python 3 strings are Unicode by default
- Support emoji, international characters, special symbols
- Future-proof for global users

---

## 8. Performance Considerations

### Decision

**Choice**: No optimization for Phase I; linear search acceptable

**Rationale**:
- Phase I scope: ~1000 tasks maximum
- Linear search O(n) is fast enough for n=1000
- Premature optimization violates YAGNI principle

**Benchmark Targets**:
- Add task: < 1 second
- View 1000 tasks: < 2 seconds
- Memory usage: < 100MB for 1000 tasks

---

## Summary of Decisions

| Decision Area | Choice |
|---------------|--------|
| ID Generation | Sequential integers |
| Timestamps | UTC datetime, ISO 8601 |
| Validation | Dedicated validator functions |
| Data Structure | List of Task dataclasses |
| Testing | pytest with capsys |
| Error Handling | Clear messages, no exceptions |
| Encoding | UTF-8, full Unicode |
| Performance | No optimization (Phase I) |

---

**Status**: All research complete. Ready for Phase 1 (Design & Contracts).
