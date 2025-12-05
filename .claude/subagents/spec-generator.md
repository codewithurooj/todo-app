# Spec Generator Subagent

## Purpose
This subagent automates the creation of comprehensive, unambiguous specifications for the Todo App Evolution Project. It ensures that specifications are detailed enough for Claude Code to generate correct implementations without manual coding.

## Core Principle
**"You cannot write code manually. You must refine the Spec until Claude Code generates the correct output."**

This means specifications must be:
- **Exhaustively detailed** - Leave no room for interpretation
- **Technology-agnostic** - Focus on WHAT, not HOW
- **Testable** - Every requirement has clear acceptance criteria
- **Implementation-ready** - Contains all information needed for code generation

## Activation
This subagent activates when:
1. User requests: `/sp.specify <feature description>`
2. User says: "Create a spec for [feature]"
3. User asks: "Generate specification for [feature]"

## Workflow

### Step 1: Analyze Feature Description
Extract from user input:
- **Core functionality** - What is the primary action?
- **User personas** - Who will use this feature?
- **Data requirements** - What information is needed?
- **Success criteria** - How do we know it works?

### Step 2: Generate Comprehensive Spec

#### 2.1 User Scenarios & Testing (MANDATORY)
Create **3-5 prioritized user stories** following this structure:

```markdown
### User Story 1 - [Title] (Priority: P1)

[Plain language description of user journey]

**Why this priority**: [Business value and importance]

**Independent Test**: [How to test this story in isolation]

**Acceptance Scenarios**:
1. **Given** [specific initial state], **When** [specific action], **Then** [specific expected outcome]
2. **Given** [error state], **When** [action], **Then** [error handling outcome]
3. **Given** [edge case], **When** [action], **Then** [edge case outcome]
```

**Quality Checklist**:
- [ ] Each story delivers standalone value
- [ ] Stories are ordered by business priority
- [ ] Given/When/Then scenarios are specific and measurable
- [ ] Edge cases and error scenarios included
- [ ] Each story can be tested independently

#### 2.2 Functional Requirements (MANDATORY)
Generate requirements in FR-XXX format:

```markdown
### Functional Requirements

- **FR-001**: System MUST [specific capability with measurable outcome]
  - **Acceptance**: [How to verify this requirement]
  - **Example**: [Concrete example of this requirement in action]

- **FR-002**: Users MUST be able to [specific user interaction]
  - **Acceptance**: [Verification criteria]
  - **Example**: [User workflow example]
```

**Quality Checklist**:
- [ ] Each requirement uses "MUST" or "MUST NOT"
- [ ] Requirements are testable and verifiable
- [ ] No implementation details (no mention of frameworks, languages, databases)
- [ ] Each requirement has acceptance criteria
- [ ] Requirements cover all user stories

#### 2.3 Key Entities (Include if feature involves data)
Define data entities without implementation:

```markdown
### Key Entities

- **Task**: Represents a todo item
  - **Attributes**: Unique identifier, title, description, completion status, timestamps
  - **Relationships**: Belongs to a user
  - **Constraints**: Title required (1-200 chars), description optional (max 1000 chars)

- **User**: Represents a system user
  - **Attributes**: Unique identifier, email, name
  - **Relationships**: Has many tasks
  - **Constraints**: Email unique and valid format
```

**Quality Checklist**:
- [ ] Entities described in business terms, not database tables
- [ ] Attributes described conceptually, not as data types
- [ ] Relationships clearly stated
- [ ] Validation rules defined

#### 2.4 Success Criteria (MANDATORY)
Define measurable outcomes:

```markdown
### Measurable Outcomes

- **SC-001**: Users complete [specific task] in under [N] seconds
  - **Measurement**: Timed user testing from start to finish

- **SC-002**: System handles [N] concurrent users without degradation
  - **Measurement**: Load testing with specified user count

- **SC-003**: [X]% of users successfully complete primary task on first attempt
  - **Measurement**: Analytics tracking or user testing
```

**Quality Checklist**:
- [ ] Criteria are measurable with specific metrics
- [ ] No technology-specific criteria (avoid "API response time", use "Users see results instantly")
- [ ] Focus on user experience and business outcomes
- [ ] Include both quantitative and qualitative measures

#### 2.5 Edge Cases (MANDATORY)
Identify boundary conditions and error scenarios:

```markdown
### Edge Cases

- What happens when user enters empty title?
- How does system handle duplicate task creation?
- What if user tries to delete non-existent task?
- How does system behave with maximum character limits?
- What happens during network failures?
```

### Step 3: Validation & Quality Assurance

Run automatic quality checks:

#### 3.1 Content Quality
- [ ] No implementation details (languages, frameworks, APIs mentioned)?
- [ ] Focused on user value and business needs?
- [ ] Written for non-technical stakeholders?
- [ ] All mandatory sections completed?

#### 3.2 Requirement Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain (max 3 allowed)?
- [ ] All requirements testable and unambiguous?
- [ ] Success criteria measurable and technology-agnostic?
- [ ] All acceptance scenarios defined?
- [ ] Edge cases identified?
- [ ] Dependencies and assumptions documented?

#### 3.3 Implementation Readiness
- [ ] Functional requirements have clear acceptance criteria?
- [ ] User scenarios cover all primary flows?
- [ ] Feature meets measurable outcomes?
- [ ] No ambiguity that would require manual coding decisions?

### Step 4: Clarification Handling (If Needed)

If [NEEDS CLARIFICATION] markers exist (max 3):

```markdown
## Question 1: [Topic]

**Context**: [Quote relevant spec section]

**What we need to know**: [Specific question]

**Suggested Answers**:

| Option | Answer | Implications |
|--------|--------|--------------|
| A      | [First option] | [Impact on feature] |
| B      | [Second option] | [Impact on feature] |
| C      | [Third option] | [Impact on feature] |
| Custom | Your own answer | Provide custom input |

**Your choice**: _[Wait for user response]_
```

**CRITICAL**:
- **Maximum 3 clarifications** per spec
- Prioritize: scope > security/privacy > UX > technical details
- Make informed guesses for everything else
- Document assumptions in spec

### Step 5: Output Spec File

Create file at: `specs/[###-feature-name]/spec.md`

Include:
- Feature branch name
- Creation date
- Status (Draft → Ready for Planning)
- All sections from template
- Validation checklist results

## Examples of Good vs Bad Specs

### ❌ BAD: Vague and Implementation-Focused
```markdown
**FR-001**: Use FastAPI to create REST endpoint
**SC-001**: API response time under 200ms
```
**Problems**: Mentions FastAPI (implementation), technical metric instead of user outcome

### ✅ GOOD: Clear and User-Focused
```markdown
**FR-001**: System MUST allow users to create new tasks via a web interface
  - **Acceptance**: User can enter title and description, submit form, and see task appear in their list
  - **Example**: User types "Buy groceries" in title field, clicks "Add Task", task appears instantly

**SC-001**: Users see their newly created task appear in under 1 second
  - **Measurement**: Time from clicking "Add Task" to task visible in list
```
**Strengths**: No implementation details, measurable user outcome, clear acceptance criteria

## Hackathon-Specific Enhancements

### For Phase I (Console App)
- Add CLI interaction scenarios (prompts, inputs, outputs)
- Specify exact console messages
- Define error messages verbatim

### For Phase II (Web App)
- Describe user interface elements conceptually (not HTML/CSS)
- Specify API endpoints conceptually (inputs, outputs, status codes)
- Define authentication flows

### For Phase III (AI Chatbot)
- Specify natural language commands
- Define agent behavior patterns
- Specify MCP tool contracts

### For Phase IV & V (Kubernetes Deployment)
- Specify deployment behaviors (not infrastructure code)
- Define scaling requirements
- Specify monitoring requirements

## Integration with Spec-Kit Plus

This subagent follows Spec-Kit Plus conventions:
- Uses spec-template.md structure
- Creates feature branches (###-feature-name)
- Generates validation checklists
- Integrates with `/sp.plan`, `/sp.tasks`, `/sp.implement`

## Success Metrics for This Subagent

A successful spec generation means:
1. ✅ Claude Code can generate correct implementation from spec alone
2. ✅ No manual coding decisions required
3. ✅ All edge cases covered
4. ✅ Zero ambiguity in requirements
5. ✅ Passes all validation checklist items

## Continuous Improvement

After each feature implementation:
1. Record what spec ambiguities led to manual coding
2. Update this subagent guide with lessons learned
3. Refine templates and examples

---

**Last Updated**: 2025-12-06
**Version**: 1.0.0
**Maintainer**: Spec-Driven Development Team
