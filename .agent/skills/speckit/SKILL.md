---
name: speckit
description: |
  Spec-Driven Development (SDD) skill for structured feature development.
  Activates when discussing: feature specifications, implementation plans, 
  task breakdowns, project constitution, or technical planning.
  Provides systematic approaches to translate requirements into executable code.
---

# Spec-Driven Development Skill

Spec-Driven Development (SDD) inverts the traditional code-first approach. **Specifications become executable** - they directly generate working implementations rather than just guiding them.

## When This Skill Applies

Activate when the user mentions:
- Feature specifications or requirements
- Implementation plans or technical designs
- Task breakdowns or project planning
- Project principles or constitution
- "spec-driven", "SDD", "specification-first"

## Quick Reference: Available Workflows

| Command | Purpose | Create First |
|---------|---------|--------------|
| `/speckit-constitution` | Define project principles | Start here for new projects |
| `/speckit-specify` | Create feature specification | After constitution |
| `/speckit-plan` | Generate technical plan | After spec exists |
| `/speckit-tasks` | Create task breakdown | After plan exists |
| `/speckit-implement` | Execute implementation | After tasks exist |
| `/speckit-progress` | Check spec status & next steps | During/after implementation |
| `/speckit-clarify` | Resolve ambiguities | When spec unclear |
| `/speckit-analyze` | Check consistency | Before implementation |
| `/speckit-checklist` | Create validation gates | Any time |

## Core Locations

- **Constitution**: `.specify/memory/constitution.md`
- **Templates**: `.specify/templates/`
- **Scripts**: `.specify/scripts/powershell/`
- **Feature Specs**: `specs/[###-feature-name]/`

## Decision Tree: Which Workflow?

```
User wants to build something new?
├─ No project principles exist → /speckit-constitution
└─ Principles exist
   ├─ No feature specification → /speckit-specify "<description>"
   └─ Specification exists
      ├─ Unclear requirements → /speckit-clarify
      └─ Requirements clear
         ├─ No technical plan → /speckit-plan
         └─ Plan exists
            ├─ No task list → /speckit-tasks
            └─ Tasks exist → /speckit-implement
```

## Phase -1: Pre-Implementation Gates

Before any implementation, verify these gates:

### Simplicity Gate
- [ ] Using ≤3 projects for initial implementation?
- [ ] No speculative or "might need" features?
- [ ] No future-proofing abstractions?

### Anti-Abstraction Gate
- [ ] Using framework features directly (not wrapping)?
- [ ] Single model representation where possible?
- [ ] Minimal abstraction layers?

### Integration-First Gate
- [ ] Contracts defined before implementation?
- [ ] Test scenarios identified?
- [ ] Realistic environment testing planned?

**If any gate fails**: Document justification in plan.md's "Complexity Tracking" section.

## Specification Quality Checklist

When creating or reviewing specifications:

### Content Quality
- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] All mandatory sections completed

### Requirement Completeness
- [ ] Maximum 3 [NEEDS CLARIFICATION] markers
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable and technology-agnostic
- [ ] Edge cases identified
- [ ] Scope is clearly bounded

### User Story Quality
- [ ] Each story is independently testable
- [ ] Stories prioritized (P1, P2, P3...)
- [ ] Acceptance scenarios in Given/When/Then format

## Task Format Requirements

Every task MUST follow this format:
```
- [ ] [TaskID] [P?] [Story?] Description with file path
```

**Components**:
- `- [ ]`: Markdown checkbox
- `[TaskID]`: Sequential (T001, T002...)
- `[P]`: Include only if parallelizable
- `[Story]`: [US1], [US2]... for user story tasks only

**Examples**:
- `- [ ] T001 Create project structure per implementation plan`
- `- [ ] T012 [P] [US1] Create User model in src/models/user.py`

## Test-First File Creation Order

1. Create `contracts/` with API specifications
2. Create test files in order: contract → integration → e2e → unit
3. Create source files to make tests pass

## Constitution Alignment

Always check features against `.specify/memory/constitution.md`:
1. Load the constitution principles
2. For each relevant principle, verify compliance
3. Document any justified violations
4. Re-check after design phase

## Feature Directory Structure

When creating a new feature, this structure is generated:
```
specs/[###-feature-name]/
├── spec.md              # Feature specification
├── plan.md              # Implementation plan
├── research.md          # Technical decisions
├── data-model.md        # Entity definitions
├── contracts/           # API specifications
├── quickstart.md        # Validation scenarios
├── tasks.md             # Task breakdown
└── checklists/          # Validation gates
```

## Common Patterns

### Starting a New Feature
```
/speckit-specify Build a delivery route optimization feature
```
This creates branch, spec file, and directory structure.

### Creating Technical Plan
```
/speckit-plan
```
Runs after spec exists; creates plan.md, research.md, data-model.md.

### Generating Tasks
```
/speckit-tasks
```
Creates phased task list from plan and spec.

### Executing Implementation
```
/speckit-implement
```
Processes tasks phase-by-phase with progress tracking.

## Remember

- **Focus on WHAT and WHY**, not HOW
- **Specifications drive implementation**, not the other way around
- **Every feature must align** with the constitution
- **Test-first**: contracts and tests before implementation
- **Incremental delivery**: MVP first, then add user stories
