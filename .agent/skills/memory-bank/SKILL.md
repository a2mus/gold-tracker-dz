---
name: memory-bank
description: |
  Persistent context management system for maintaining project knowledge across sessions.
  Activates when: starting new conversations, making architectural decisions, completing tasks,
  learning patterns, or when user says "UMB" or "Update Memory Bank".
  Provides continuity by tracking progress, decisions, and system patterns.
---

# Memory Bank

Maintain persistent project context across AI sessions through structured markdown files in your project root.

## When This Skill Applies

- **Session Start**: Check for existing `memory-bank/` directory
- **Architectural Decisions**: Log significant technical choices
- **Task Completion**: Update progress tracking
- **Pattern Learning**: Document coding/architectural patterns
- **Manual Trigger**: User says "UMB" or "Update Memory Bank"

---

## Core File Structure

| File | Purpose | Update Frequency |
|------|---------|-----------------|
| `projectbrief.md` | Overall scope, goals, requirements, constraints | Rare - project setup |
| `productContext.md` | UX considerations, target users, problems solved | When product focus shifts |
| `systemPatterns.md` | Architecture decisions, design patterns, technical choices | New patterns discovered |
| `techContext.md` | Technology stack, dependencies, frameworks, constraints | Dependencies change |
| `activeContext.md` | Current focus, recent changes, next steps, active decisions | **Frequently** |
| `progress.md` | Completed features, current tasks, unresolved issues | Task state changes |

---

## Directory Organization

### Standard Structure
```
project-root/
├── memory-bank/
│   ├── projectbrief.md      # Project scope and goals
│   ├── productContext.md    # UX and user focus
│   ├── systemPatterns.md    # Architecture & patterns
│   ├── techContext.md       # Tech stack & deps
│   ├── activeContext.md     # Current work state
│   └── progress.md          # Task tracking
```

### Modular Structure (Larger Projects)
```
memory-bank/
├── general.md               # Cross-cutting concerns
├── frontend/
│   ├── patterns.md
│   └── context.md
├── backend/
│   ├── patterns.md
│   └── context.md
└── activeContext.md         # Always at root level
```

---

## Initialization Workflow

### If memory-bank/ Exists
1. Read all core files in order: projectbrief → productContext → techContext → systemPatterns → activeContext → progress
2. Check for `specs/` directory for SDD integration
3. Set status: `[MEMORY BANK: ACTIVE]`

### If No memory-bank/
1. Ask: "No Memory Bank found. Initialize one for project context?"
2. If declined: Set `[MEMORY BANK: INACTIVE]`, proceed
3. If agreed: Create directory and core files from templates
4. Look for existing docs (README, CLAUDE.md) to populate initial context

---

## Status Prefix

Begin responses with `[MEMORY BANK: ACTIVE]` or `[MEMORY BANK: INACTIVE]`.

---

## Update Protocol

Use timestamp format: `[YYYY-MM-DD HH:MM:SS]`

| Event | Update Action |
|-------|---------------|
| Session starts | Read all files, update activeContext with session start |
| Architecture decision | Add to systemPatterns.md with rationale |
| Task completed | Move item in progress.md, update activeContext |
| Tech stack change | Update techContext.md with dependencies |
| Pattern identified | Document in systemPatterns.md with example |
| Focus shift | Update activeContext.md current focus section |

---

## Specs Integration

When `specs/` directory exists, treat as authoritative source:

```
specs/
└── NNN-feature-name/
    ├── spec.md        # Feature specification
    ├── plan.md        # Technical plan
    ├── tasks.md       # Task breakdown
    ├── data-model.md  # Data entities
    └── research.md    # Technical findings
```

Cross-reference specs/tasks.md with memory-bank/progress.md for alignment.

---

## Learning Support

When solving coding/architecture requests:
1. Identify pattern/paradigm (MVC, Repository, DI, etc.)
2. State: "I used [NAME] pattern."
3. Explain: purpose and fit
4. Document in systemPatterns.md

---

## Manual Update (UMB)

When user says "UMB" or "Update Memory Bank":
1. Respond: `[MEMORY BANK: UPDATING]`
2. Review session for: decisions, clarifications, context changes
3. Update all affected files
4. Confirm: "Memory Bank synchronized"

---

## File Templates

### projectbrief.md
```markdown
# Project Brief

## Overview
[One-paragraph project description]

## Goals
- Primary:
- Secondary:

## Requirements
- Must have:
- Nice to have:

## Constraints
- Technical:
- Business:
```

### productContext.md
```markdown
# Product Context

## Target Users
[Who uses this product]

## Problems Solved
[What pain points addressed]

## UX Considerations
- Key flows:
- Critical screens:
```

### techContext.md
```markdown
# Technical Context

## Stack
- Language:
- Framework:
- Build:

## Dependencies
[Key libraries and versions]

## Constraints
- API limits:
- Platform requirements:
```

### systemPatterns.md
```markdown
# System Patterns

## Architecture
[Overall architecture pattern]

## Design Patterns
| Pattern | Where Used | Rationale |
|---------|------------|-----------|

## Coding Standards
- Naming:
- Structure:
```

### activeContext.md
```markdown
# Active Context

## Current Focus
[What we're working on right now]

## Recent Changes
- [YYYY-MM-DD] Change description

## Next Steps
1. 
2. 

## Open Questions
- 
```

### progress.md
```markdown
# Progress

## Completed
- [x] Feature/task

## In Progress
- [ ] Current work

## Blocked
- Issue and blocker

## Next Up
- Prioritized backlog
```

---

## Best Practices

✅ **Be specific**: "Use 2-space indentation" not "Format properly"
✅ **Update activeContext.md frequently**: It's your working memory
✅ **Let structure evolve**: Don't over-engineer initially
✅ **Keep files focused**: One domain per file
✅ **Use standard markdown**: AI discovers .md files recursively

---

## Keywords

memory bank, context persistence, session continuity, project documentation, decision tracking, progress tracking, pattern documentation, agentic coding
