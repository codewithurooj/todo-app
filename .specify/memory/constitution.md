<!--
Sync Impact Report:
- Version Change: None → 1.0.0 (Initial constitution)
- Modified Principles: N/A (Initial creation)
- Added Sections: All (Initial creation)
- Removed Sections: None
- Templates Requiring Updates:
  ✅ spec-template.md - Validated alignment with constitution principles
  ✅ plan-template.md - Constitution Check section references this file
  ✅ tasks-template.md - Task organization reflects TDD and simplicity principles
  ✅ commands/*.md - Agent-specific guidance aligned
- Follow-up TODOs: None
-->

# Todo App Evolution Project Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

Every feature MUST start with a specification that defines:
- User scenarios and acceptance criteria (Given/When/Then format)
- Functional requirements (FR-XXX format with MUST statements)
- Success criteria (measurable outcomes)
- Edge cases and error scenarios

**Rationale**: Specifications ensure shared understanding between humans and AI agents, prevent scope creep, and provide a single source of truth for feature requirements. In a project evolving from simple script to distributed system, clear specs prevent architectural misalignment.

### II. Test-Driven Development (NON-NEGOTIABLE)

For every feature:
1. Write tests FIRST based on specification
2. Verify tests FAIL (red)
3. Implement minimum code to pass (green)
4. Refactor for quality (refactor)
5. Obtain user approval before implementation

**Rationale**: TDD ensures code correctness, prevents regressions during evolution, and creates a safety net for refactoring. As the project grows from in-memory to distributed, tests validate each transformation step.

### III. Evolutionary Architecture

The project MUST:
- Start with the simplest solution (Phase I: in-memory console app)
- Add complexity only when requirements demand it
- Maintain backward compatibility during evolution phases
- Document architectural decisions (ADRs) for significant changes
- Preserve core functionality while adding capabilities

**Rationale**: This project simulates real-world software evolution. Each phase (in-memory → file → database → distributed → event-driven → AI-powered) builds on the previous foundation without breaking existing functionality.

### IV. Clean Code & Python Standards

All code MUST:
- Follow PEP 8 style guidelines
- Use type hints (Python 3.13+)
- Include docstrings for modules, classes, and functions
- Use meaningful variable and function names
- Keep functions small and single-purpose (max 20 lines preferred)
- Avoid global state (except when required by current phase)

**Rationale**: Clean code enables smooth evolution. As the project grows to Kubernetes-managed distributed systems, code clarity prevents technical debt and facilitates team collaboration.

### V. Project Structure & Organization

The project MUST maintain:
```
todo-app/
├── .specify/
│   ├── memory/
│   │   └── constitution.md          # This file
│   ├── templates/                    # Spec-Kit Plus templates
│   └── scripts/                      # Automation scripts
├── specs/
│   └── [###-feature-name]/          # Per-feature specifications
│       ├── spec.md                   # Requirements
│       ├── plan.md                   # Architecture
│       ├── tasks.md                  # Implementation tasks
│       └── research.md               # Technical research
├── history/
│   ├── prompts/                      # Prompt History Records
│   │   ├── constitution/             # Constitution-related
│   │   ├── [feature-name]/           # Feature-specific
│   │   └── general/                  # General interactions
│   └── adr/                          # Architecture Decision Records
├── src/                              # Source code
│   ├── models/                       # Data models
│   ├── services/                     # Business logic
│   ├── cli/                          # Command-line interface
│   └── utils/                        # Utilities
├── tests/                            # Test suite
│   ├── unit/                         # Unit tests
│   ├── integration/                  # Integration tests
│   └── contract/                     # Contract tests
├── CLAUDE.md                         # Claude Code instructions
└── README.md                         # Project documentation
```

**Rationale**: Consistent structure enables navigation across evolution phases, supports AI agent workflows, and maintains documentation alongside code.

### VI. Simplicity First (YAGNI)

The project MUST:
- Implement only requested features (You Aren't Gonna Need It)
- Avoid premature optimization
- Choose simple solutions over clever ones
- Defer complexity until the phase requires it
- Resist over-engineering

**Rationale**: Each phase introduces complexity intentionally. Adding unnecessary complexity early undermines the learning objective of evolutionary architecture.

### VII. Comprehensive Documentation

Every phase MUST include:
- Updated README.md with setup and usage instructions
- Specification documents for all features
- Architecture Decision Records for significant choices
- Prompt History Records for all AI-assisted development
- Code comments for non-obvious logic
- Migration guides between phases

**Rationale**: Documentation enables knowledge transfer, supports onboarding, and preserves the reasoning behind architectural evolution decisions.

## Technology Standards

### Required Stack (Phase I)

- **Language**: Python 3.13+
- **Package Manager**: UV (fast Python package installer)
- **Development Tools**: Claude Code, Spec-Kit Plus
- **Testing Framework**: pytest
- **Code Quality**: ruff (linting), black (formatting)
- **Type Checking**: mypy

### Evolution Readiness

The codebase MUST be structured to facilitate future phases:
- **Phase II**: File persistence (JSON/SQLite)
- **Phase III**: REST API (FastAPI/Flask)
- **Phase IV**: Database (PostgreSQL/MongoDB)
- **Phase V**: Event-driven (Kafka/Redis)
- **Phase VI**: Distributed (Kubernetes)
- **Phase VII**: AI-powered (LLM integration)

## Development Workflow

### Feature Development Process

1. **Specification** (`/sp.specify`):
   - Create feature branch: `###-feature-name`
   - Document user scenarios with acceptance criteria
   - Define functional requirements
   - Establish success criteria

2. **Planning** (`/sp.plan`):
   - Research technical approach
   - Design data models and contracts
   - Create implementation plan
   - Identify architectural decisions

3. **Task Generation** (`/sp.tasks`):
   - Break plan into testable tasks
   - Order by dependencies
   - Mark parallel opportunities
   - Map to user stories

4. **Implementation** (`/sp.implement`):
   - Write tests first (TDD)
   - Implement minimum viable code
   - Refactor for quality
   - Validate against spec

5. **Review & Documentation**:
   - Record Prompt History Records
   - Create ADRs for significant decisions
   - Update README and docs
   - Commit and create PR

### Quality Gates

Before merging any feature:
- ✅ All tests pass (100% of written tests)
- ✅ Code passes linting (ruff) and formatting (black)
- ✅ Type checking passes (mypy)
- ✅ Specification acceptance criteria met
- ✅ Documentation updated
- ✅ PHR created and filed

### Commit Standards

- Use conventional commits: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`
- Reference specification: `feat(###-feature): add task creation`
- Keep commits atomic and focused
- Write clear commit messages explaining why, not what

## Phase-Specific Rules

### Phase I: In-Memory Console App (Current Phase)

**Constraints**:
- Data stored in memory only (Python lists/dicts)
- Command-line interface only
- No external dependencies beyond testing tools
- Focus on core CRUD operations

**Features Required**:
1. Add task
2. Delete task
3. Update task
4. View tasks
5. Mark task complete

**Success Criteria**:
- All 5 basic operations functional
- Tests cover all operations
- Clean console UI with clear prompts
- Error handling for invalid inputs

### Future Phases

Future phase constitutions will be amendments to this document, preserving core principles while adding phase-specific requirements.

## Governance

### Constitution Authority

This constitution:
- Supersedes conflicting practices or preferences
- Guides all AI agent interactions (Claude Code)
- Informs all architectural decisions
- Applies to all contributors

### Amendment Process

Constitution amendments require:
1. Documented rationale for change
2. Version bump (semantic versioning)
3. Impact analysis on existing code
4. Migration plan if breaking changes
5. User approval
6. PHR creation documenting the change

**Version Bump Rules**:
- **MAJOR**: Breaking changes to core principles or workflow
- **MINOR**: New principles or expanded guidance
- **PATCH**: Clarifications, typos, non-semantic fixes

### Compliance Review

Every pull request MUST:
- Verify alignment with constitution principles
- Check specification completeness
- Validate test coverage
- Confirm documentation updates
- Pass all quality gates

### Complexity Justification

Any violation of constitution principles (e.g., adding complexity early, skipping tests, avoiding specs) MUST be:
1. Explicitly called out
2. Justified with rationale
3. Documented in plan.md Complexity Tracking table
4. Approved by user before proceeding

### Development Guidance

For runtime development guidance and AI agent instructions, see:
- `CLAUDE.md` - Claude Code specific instructions
- `.specify/templates/commands/` - Command workflows
- `specs/[feature]/plan.md` - Feature-specific architecture

---

**Version**: 1.0.0 | **Ratified**: 2025-12-05 | **Last Amended**: 2025-12-05
