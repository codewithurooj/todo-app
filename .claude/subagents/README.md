# Subagents Directory

This directory contains specialized subagent configurations that enhance Claude Code's capabilities for the Todo App Evolution Project.

## Available Subagents

### 1. Spec Generator Subagent
**File**: `spec-generator.md`
**Purpose**: Automates creation of comprehensive, unambiguous specifications
**Activation**: `/sp.specify <feature description>`

**Key Capabilities**:
- Generates exhaustive user scenarios with Given/When/Then acceptance criteria
- Creates detailed functional requirements (FR-XXX format)
- Defines measurable success criteria
- Identifies edge cases automatically
- Validates spec quality against hackathon requirements
- Ensures specifications are detailed enough for code generation without manual intervention

**Use When**:
- Starting a new feature for any hackathon phase
- Need to document requirements before implementation
- Want to ensure Claude Code has all information to generate correct code

**Example Usage**:
```
/sp.specify Create a feature to add tasks with title and description
```

## Coming Soon

### 2. MCP Tool Builder Subagent (Phase III)
**Purpose**: Generate MCP server tool specifications and implementations
**Status**: Planned for Phase III

### 3. Kubernetes Deployment Subagent (Phase IV)
**Purpose**: Create deployment specifications for K8s/Helm
**Status**: Planned for Phase IV

### 4. Cloud-Native Blueprint Subagent (Bonus +200 pts)
**Purpose**: Generate infrastructure-as-code specifications
**Status**: Planned for bonus points

### 5. Event-Driven Architecture Subagent (Phase V)
**Purpose**: Design Kafka/Dapr event-driven architectures
**Status**: Planned for Phase V

### 6. Testing & Validation Subagent (All Phases)
**Purpose**: Generate comprehensive test suites from specs
**Status**: Planned for cross-phase support

## How to Use Subagents

### Method 1: Slash Commands
The subagents integrate with existing Spec-Kit Plus commands:
```bash
/sp.specify <feature>      # Activates Spec Generator
/sp.plan                   # Uses spec to generate plan
/sp.tasks                  # Breaks plan into testable tasks
/sp.implement              # Executes tasks with TDD
```

### Method 2: Direct Reference
Reference subagent guides in your prompts:
```
@.claude/subagents/spec-generator.md help me create a spec for user authentication
```

### Method 3: Context Awareness
Subagents are automatically aware of:
- Constitution principles
- Project phase (I, II, III, IV, or V)
- Technology stack constraints
- Hackathon requirements

## Subagent Development Guidelines

When creating new subagents:

1. **Clear Purpose**: Define exactly when and why to use this subagent
2. **Activation Patterns**: Specify how the subagent gets triggered
3. **Quality Checklist**: Include validation criteria
4. **Examples**: Show good vs bad outputs
5. **Phase-Specific**: Adapt behavior based on hackathon phase
6. **Constitution Compliance**: Align with project principles

## Integration with Spec-Kit Plus

All subagents follow Spec-Kit Plus workflow:
```
Specify → Plan → Tasks → Implement → Review
   ↓        ↓       ↓        ↓          ↓
 spec.md  plan.md tasks.md  code      PHR/ADR
```

## Version History

- **v1.0.0** (2025-12-06): Initial setup with Spec Generator Subagent

---

**Note**: This is a living directory. Subagents will be added as we progress through hackathon phases.
