# Todo App Evolution Project

> **Simulating Real-World Software Evolution**: From Simple Script to Kubernetes-Managed, Event-Driven, AI-Powered Distributed System

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📋 Table of Contents

- [Overview](#overview)
- [Project Philosophy](#project-philosophy)
- [Current Phase](#current-phase)
- [Evolution Roadmap](#evolution-roadmap)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Constitution](#constitution)
- [Contributing](#contributing)
- [Documentation](#documentation)

## 🎯 Overview

This project demonstrates the **real-world evolution of software architecture**. Starting as a simple in-memory console application, it will progressively evolve through multiple phases, each adding complexity and capabilities while maintaining backward compatibility and code quality.

**Learning Objectives:**
- Experience architectural evolution firsthand
- Practice spec-driven and test-driven development
- Build production-ready systems incrementally
- Document architectural decisions and trade-offs
- Master modern Python development practices

## 🧭 Project Philosophy

This project follows **7 Core Principles** defined in our [Constitution](.specify/memory/constitution.md):

1. **Spec-Driven Development** ⚠️ NON-NEGOTIABLE
   - Every feature starts with a specification
   - User scenarios with acceptance criteria (Given/When/Then)
   - Functional requirements with measurable success criteria

2. **Test-Driven Development** ⚠️ NON-NEGOTIABLE
   - Write tests first based on specification
   - Red → Green → Refactor cycle strictly enforced
   - User approval before implementation

3. **Evolutionary Architecture**
   - Start with simplest solution
   - Add complexity only when requirements demand it
   - Maintain backward compatibility during evolution

4. **Clean Code & Python Standards**
   - PEP 8 style guidelines
   - Type hints (Python 3.13+)
   - Docstrings for all modules, classes, functions
   - Functions max 20 lines (preferred)

5. **Project Structure & Organization**
   - Consistent directory layout
   - Separation of concerns (models, services, CLI)
   - Documentation alongside code

6. **Simplicity First (YAGNI)**
   - Implement only requested features
   - Avoid premature optimization
   - Defer complexity until needed

7. **Comprehensive Documentation**
   - README, specs, ADRs, PHRs
   - Migration guides between phases
   - Clear code comments

## 📍 Current Phase

### **Phase I: Todo In-Memory Python Console App**

**Status**: 🏗️ In Progress
**Version**: 0.1.0 (Development)

#### Features (Phase I)
- ✅ Constitution v1.0.0 established
- ✅ Spec Generator Subagent (development tool)
- ⏳ Add task
- ⏳ Delete task
- ⏳ Update task
- ⏳ View tasks
- ⏳ Mark task complete

#### Technology Stack
- **Language**: Python 3.13+
- **Package Manager**: [UV](https://github.com/astral-sh/uv) (fast Python package installer)
- **Development Tools**: Claude Code, Spec-Kit Plus
- **Testing**: pytest
- **Code Quality**: ruff (linting), black (formatting)
- **Type Checking**: mypy

#### Constraints (Phase I)
- Data stored in memory only (Python lists/dicts)
- Command-line interface only
- No external dependencies beyond testing tools
- Focus on core CRUD operations

## 🗺️ Evolution Roadmap

```
Phase I   → Phase II    → Phase III  → Phase IV     → Phase V      → Phase VI      → Phase VII
In-Memory → File        → REST API   → Database     → Event-Driven → Distributed   → AI-Powered
Console     Persistence   (FastAPI)   (PostgreSQL)   (Kafka/Redis)  (Kubernetes)    (LLM)
```

### Planned Phases

| Phase | Focus | Key Technologies | Status |
|-------|-------|-----------------|--------|
| **I** | In-Memory Console App | Python, UV, pytest | 🏗️ In Progress |
| **II** | File Persistence | JSON, SQLite | 📋 Planned |
| **III** | REST API | FastAPI, Pydantic | 📋 Planned |
| **IV** | Database Integration | PostgreSQL, SQLAlchemy | 📋 Planned |
| **V** | Event-Driven Architecture | Kafka, Redis | 📋 Planned |
| **VI** | Distributed System | Kubernetes, Docker | 📋 Planned |
| **VII** | AI-Powered Features | LLM Integration, RAG | 📋 Planned |

## 📦 Prerequisites

### Required
- **Python 3.13+** - [Download here](https://www.python.org/downloads/)
- **UV** - Fast Python package installer
  ```bash
  # Install UV (macOS/Linux)
  curl -LsSf https://astral.sh/uv/install.sh | sh

  # Install UV (Windows)
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- **Git** - Version control

### Optional (for development)
- **Claude Code** - AI-assisted development (recommended)
- **VS Code** - Code editor with Python extension

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/codewithurooj/todo-app.git
cd todo-app
```

### 2. Create Virtual Environment with UV
```bash
# Create virtual environment
uv venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
# Install development dependencies
uv pip install -r requirements.txt  # Once created
```

### 4. Verify Installation
```bash
# Run tests (once implemented)
pytest

# Check code quality (once implemented)
ruff check .
black --check .
mypy .
```

## 📁 Project Structure

```
todo-app/
├── .claude/                      # Claude Code commands
│   └── commands/
│       ├── sp.specify.md         # Feature specification command
│       ├── sp.plan.md            # Implementation planning command
│       ├── sp.tasks.md           # Task generation command
│       └── ...
├── .specify/                     # Spec-Kit Plus framework
│   ├── memory/
│   │   └── constitution.md       # Project constitution (v1.0.0)
│   ├── templates/                # Templates for specs, plans, tasks
│   └── scripts/                  # Automation scripts
├── specs/                        # Feature specifications
│   └── [###-feature-name]/       # Per-feature directory
│       ├── spec.md               # Requirements
│       ├── plan.md               # Architecture & design
│       ├── tasks.md              # Implementation tasks
│       └── research.md           # Technical research
├── history/                      # Project history
│   ├── prompts/                  # Prompt History Records (PHRs)
│   │   ├── constitution/         # Constitution-related
│   │   ├── [feature-name]/       # Feature-specific
│   │   └── general/              # General interactions
│   └── adr/                      # Architecture Decision Records
├── src/                          # Source code (to be created)
│   ├── models/                   # Data models
│   ├── services/                 # Business logic
│   ├── cli/                      # Command-line interface
│   └── utils/                    # Utilities
├── tests/                        # Test suite (to be created)
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   └── contract/                 # Contract tests
├── .gitignore                    # Git ignore rules
├── CLAUDE.md                     # Claude Code instructions
├── README.md                     # This file
└── requirements.txt              # Python dependencies (to be created)
```

## 🔄 Development Workflow

This project follows **Spec-Driven Development** with **Test-Driven Development**:

### 1. Specification (`/sp.specify`)
```bash
# Create feature specification
# Defines user scenarios, requirements, success criteria
```
- Document user scenarios with Given/When/Then acceptance criteria
- Define functional requirements (FR-XXX format)
- Establish measurable success criteria
- Identify edge cases

### 2. Planning (`/sp.plan`)
```bash
# Create implementation plan
# Designs architecture, data models, contracts
```
- Research technical approach
- Design data models
- Define API contracts (if applicable)
- Make architectural decisions

### 3. Task Generation (`/sp.tasks`)
```bash
# Generate actionable tasks
# Breaks plan into testable, ordered tasks
```
- Break plan into small, testable tasks
- Order by dependencies
- Mark parallel opportunities
- Map to user stories

### 4. Implementation (`/sp.implement`)
```bash
# Execute tasks
# TDD: Tests → Implementation → Refactor
```
- Write tests first (Red)
- Implement minimum code to pass (Green)
- Refactor for quality
- Validate against spec

### 5. Review & Documentation
- Create Prompt History Records (PHRs)
- Create Architecture Decision Records (ADRs) for significant decisions
- Update documentation
- Commit with conventional commit messages

## 📜 Constitution

The project is governed by our [Constitution](.specify/memory/constitution.md), which defines:

- **Core Principles** (7 principles, 2 NON-NEGOTIABLE)
- **Technology Standards** (Phase I: Python 3.13+, UV, pytest, ruff, black, mypy)
- **Development Workflow** (Specification → Planning → Tasks → Implementation → Review)
- **Quality Gates** (All tests pass, linting/type checking, spec criteria met)
- **Governance** (Amendment process, compliance review, complexity justification)

**Current Version**: 1.0.0
**Ratified**: 2025-12-05
**Last Amended**: 2025-12-05

## 🤖 Development Subagents

This project uses specialized subagents to automate complex development tasks across features and phases.

### Available Subagents

#### 1. Spec Generator Subagent
**Location**: `.claude/subagents/spec-generator.md`
**Purpose**: Automatically generates comprehensive, unambiguous specifications

**Key Capabilities**:
- Exhaustive user scenarios with Given/When/Then acceptance criteria
- Detailed functional requirements (FR-XXX format)
- Measurable success criteria (technology-agnostic)
- Automatic edge case identification
- Quality validation against hackathon requirements
- Maximum 3 clarifications per spec

**Why Critical for This Hackathon**:
The hackathon constraint states: *"You cannot write code manually. You must refine the Spec until Claude Code generates the correct output."*

This subagent ensures specifications are detailed enough that Claude Code can generate perfect implementations without any manual coding.

**Usage**:
```bash
/sp.specify Add task functionality with title and description
```

**What It Generates**:
- Prioritized user stories (P1, P2, P3)
- FR-XXX functional requirements with acceptance criteria
- Measurable success criteria
- Edge cases and error scenarios
- Validation checklist

**Documentation**: See [Subagents README](.claude/subagents/README.md)

## 🤝 Contributing

### Quality Gates (Required Before Merge)
- ✅ All tests pass (100% of written tests)
- ✅ Code passes linting (`ruff check .`)
- ✅ Code passes formatting (`black --check .`)
- ✅ Type checking passes (`mypy .`)
- ✅ Specification acceptance criteria met
- ✅ Documentation updated
- ✅ PHR created and filed

### Commit Standards
Follow [Conventional Commits](https://www.conventionalcommits.org/):
```bash
# Format
<type>(<scope>): <subject>

# Types
feat:     # New feature
fix:      # Bug fix
docs:     # Documentation only
test:     # Adding tests
refactor: # Code change that neither fixes bug nor adds feature
chore:    # Changes to build process or auxiliary tools

# Examples
feat(001-add-task): implement task creation
fix(003-delete): handle empty task list
docs: update README with installation steps
test(002-view): add edge case for empty list
```

## 📚 Documentation

### Key Documents
- [Constitution](.specify/memory/constitution.md) - Project principles and governance
- [CLAUDE.md](CLAUDE.md) - Claude Code agent instructions
- [Specifications](specs/) - Feature specifications
- [ADRs](history/adr/) - Architecture Decision Records
- [PHRs](history/prompts/) - Prompt History Records

### Templates
- [Spec Template](.specify/templates/spec-template.md)
- [Plan Template](.specify/templates/plan-template.md)
- [Tasks Template](.specify/templates/tasks-template.md)
- [ADR Template](.specify/templates/adr-template.md)
- [PHR Template](.specify/templates/phr-template.prompt.md)

## 🔗 Links

- **Repository**: [https://github.com/codewithurooj/todo-app](https://github.com/codewithurooj/todo-app)
- **Issues**: [https://github.com/codewithurooj/todo-app/issues](https://github.com/codewithurooj/todo-app/issues)
- **Discussions**: [https://github.com/codewithurooj/todo-app/discussions](https://github.com/codewithurooj/todo-app/discussions)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Claude Code](https://claude.com/claude-code) - AI-assisted development
- Powered by [Spec-Kit Plus](https://github.com/spec-kit/spec-kit-plus) - Spec-Driven Development framework
- Package management by [UV](https://github.com/astral-sh/uv) - Fast Python package installer

---

**Current Phase**: Phase I - In-Memory Console App
**Last Updated**: 2025-12-05
**Maintainer**: [@codewithurooj](https://github.com/codewithurooj)

*This project demonstrates the evolution of software from simple script to production-ready distributed system. Each phase builds on the previous foundation, showing real-world architectural progression.*
