---
description: Interactive quiz to verify learning progress and update Knowledge Debt status
---

# Knowledge Debt Reduction - Update Progress

Verify your learning progress through interactive quizzes, update item statuses, and contribute insights back to the Memory Bank.

> **PURPOSE**: Close the learning loop by validating your understanding and tracking your growth.

## Obsidian Link Syntax Guidelines

All generated markdown files MUST use **Obsidian internal link syntax** for navigability:

| Link Type | Syntax | Example |
|-----------|--------|---------|
| Note link | `[[Note name]]` | `[[systemPatterns]]` |
| With extension | `[[Note name.md]]` | `[[productContext.md]]` |
| To heading | `[[Note#Heading]]` | `[[systemPatterns#Repository Pattern]]` |
| Nested heading | `[[Note#H1#H2]]` | `[[decisionLog#Decisions#Firebase Choice]]` |
| Display alias | `[[Note\|Display Text]]` | `[[firebase_android\|Firebase Learning Topic]]` |
| Heading + alias | `[[Note#Heading\|Alias]]` | `[[systemPatterns#MVVM\|MVVM Pattern docs]]` |

**Rules for Internal Links:**
1. Use relative note names (no full paths) - Obsidian resolves them
2. For cross-folder links, include folder: `[[learning/topics/concept_name]]`
3. Use `|` for human-readable display text when the note name is technical
4. Always link to Memory Bank files when referencing patterns/decisions
5. **Link to source code**: `[[_code/app/src/main/java/path/File.kt|File.kt]]` (Junction `_code` points to project root)

## When to Use

- After completing a learning session from [[learning/topics/|topic guides]]
- When you feel ready to validate your understanding of a concept
- Periodically (weekly) to review your progress
- Before starting a new feature that uses concepts you've been learning

## Prerequisites

- Knowledge Debt Register exists at [[register/index|Knowledge Debt Register]]
- At least one item in the register with status `[ ]` or `[/]`
- Memory Bank exists with core files: [[productContext]] | [[systemPatterns]] | [[decisionLog]]

## Steps

### 1. Load Current Register State

Read [[register/index|Knowledge Debt Register]] and extract:
- Items with status `[ ] Not started`
- Items with status `[/] In progress`

Present summary:
```
📊 KNOWLEDGE DEBT PROGRESS CHECK

Current Register Status:
┌─────────────────────────────────────────────────────────┐
│ In Progress [/]: X items                                │
│ Not Started [ ]: Y items                                │
│ Completed   [x]: Z items                                │
└─────────────────────────────────────────────────────────┘

Which items would you like to verify today?
A) All "In Progress" items
B) Specific item: [list numbered items]
C) Quick check on a "Not Started" item I've been studying
D) Full review of everything
```

### 2. Interactive Verification Quiz

For each selected item, run a progressive verification:

#### Level 1: Conceptual Understanding
```
🧠 CONCEPT CHECK: [CONCEPT NAME]

Category: [Architectural/Framework/Domain/Language]
Used in: [[_code/app/src/main/java/[path]/[file1]|[File1]]], [[_code/app/src/main/java/[path]/[file2]|[File2]]]

Est. learning time was: [X] min

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Q1: In your own words, what is [CONCEPT] and why is it used?

[Wait for user response]
```

Evaluate response:
- **Strong answer**: Contains key terminology, explains purpose, mentions context
- **Partial answer**: Missing some aspects, may need gentle prompting
- **Weak answer**: Fundamentally incomplete, suggest more learning

#### Level 2: Project Context
```
🔗 CONTEXT CHECK: [CONCEPT NAME]

In YOUR project, this concept appears in:
- `[file1.kt]`: [[_code/app/src/main/java/[path]/[file1.kt]|Usage in File 1]]
- `[file2.kt]`: [[_code/app/src/main/java/[path]/[file2.kt]|Usage in File 2]]


Q2: Why does your project use [CONCEPT] in these places?
    What problem does it solve?

[Wait for user response]
```

#### Level 3: Practical Application
```
🛠️ APPLICATION CHECK: [CONCEPT NAME]

Scenario: [Describe a realistic modification request]

Q3: How would you approach this change?
    What would you modify and why?

[Wait for user response]
```

### 3. Score and Provide Feedback

After each concept assessment:

```markdown
## Assessment Result: [CONCEPT NAME]

| Check | Score | Notes |
|-------|-------|-------|
| Conceptual | ⭐⭐⭐ / ⭐⭐⭐ | [brief feedback] |
| Context    | ⭐⭐☆ / ⭐⭐⭐ | [brief feedback] |
| Application| ⭐⭐⭐ / ⭐⭐⭐ | [brief feedback] |

**Overall**: [PASSED ✅ / NEEDS REVIEW 📝 / CONTINUE LEARNING 📚]
```

**Passing Criteria**:
- PASSED: At least 2/3 checks scored 2+ stars
- NEEDS REVIEW: Mixed results, some gaps remain
- CONTINUE LEARNING: Fundamental gaps, recommend more study time

### 4. Update Register Status

Based on assessment results:

**For PASSED items**:
```markdown
### [CONCEPT NAME]
- **Identified**: [original date]
- **Completed**: [TODAY's DATE]
- **Category**: [unchanged]
- **Status**: [x] Completed ✅
- **Verification Notes**: Passed quiz on [date]. User demonstrated [brief summary].
```

**For NEEDS REVIEW items**:
```markdown
### [CONCEPT NAME]
- **Status**: [/] In progress
- **Last Reviewed**: [TODAY's DATE]
- **Gaps Identified**: [specific areas to focus on]
- **Next Review**: [suggested date]
```

**For CONTINUE LEARNING items**:
```markdown
### [CONCEPT NAME]
- **Status**: [/] In progress (or [ ] if was not started)
- **Last Attempted**: [TODAY's DATE]
- **Recommended Focus**: [specific learning suggestion]
- **Resources**: [[learning/topics/[concept]|Continue Learning]]
```

### 5. Capture Insights for Memory Bank

For PASSED items, prompt for Memory Bank contribution:

```
📝 MEMORY BANK CONTRIBUTION

You've mastered [CONCEPT]! Consider contributing to the project's institutional knowledge.

Would you like to add insights to the Memory Bank?
A) Add to [[systemPatterns]] - Document how this pattern is used
B) Add to [[decisionLog]] - Record why this approach was chosen
C) Update [[productContext]] - Clarify architectural context
D) Skip - No contribution needed now
```

If user selects A, B, or C:

```
Please share your insight in 2-3 sentences.
Focus on: What would help future-you (or another developer) understand this faster?

[Wait for user response]
```

Then append to the selected Memory Bank file:
```markdown
[YYYY-MM-DD HH:MM:SS] - Knowledge Debt Resolution: [CONCEPT]
[User's insight, formatted appropriately for the target file]
```

### 6. Update Progress Session File

Create `knowledge-debt/sessions/[YYYY-MM-DD]_progress.md`:

```markdown
# Knowledge Debt Progress Session

**Date**: [TIMESTAMP]
**Mode**: Progress Verification
**Items Reviewed**: [count]
**Register**: [[register/index|View Register]]
**Memory Bank**: [[productContext]] | [[systemPatterns]] | [[decisionLog]]

## Assessment Results

| Concept | Previous Status | Quiz Result | New Status | Topic |
|---------|-----------------|-------------|------------|-------|
| [name]  | [/] In progress | PASSED ✅   | [x] Completed | [[learning/topics/[name]\|Topic]] |
| [name]  | [ ] Not started | NEEDS REVIEW | [/] In progress | [[learning/topics/[name]\|Topic]] |

## Concepts Completed This Session

### [CONCEPT NAME]
- **Learning Duration**: [estimated total time spent]
- **Key Insight**: [brief summary of what was learned]
- **Memory Bank Contribution**: Added to [[systemPatterns#[section]|Patterns]] / [[decisionLog#[entry]|Decisions]]
- **Topic Archive**: [[learning/topics/[concept]|Learning Materials]]

## Ongoing Items

### [CONCEPT NAME]
- **Current Gaps**: [what still needs work]
- **Focus Areas**: [specific recommendations]
- **Next Review Target**: [date]
- **Continue Learning**: [[learning/topics/[concept]|Resources]]

## Register Statistics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Completed | X | Y | +Z |
| In Progress | X | Y | change |
| Not Started | X | Y | change |
| Total Debt | X | Y | -Z |

---
← Back to [[register/index|Knowledge Debt Register]]
```

### 7. Update Register Dashboard

Update the dashboard section in [[register/index|Knowledge Debt Register]]:

```markdown
## Dashboard

**Last Updated**: [TIMESTAMP]

| Priority | Count | Trend | Notes |
|----------|-------|-------|-------|
| HIGH     | X     | ↓     | [Y completed this week] |
| MEDIUM   | Y     | →     | |
| LOW      | Z     | →     | |

### Recent Completions
- [DATE]: [[learning/topics/[concept]|[CONCEPT]]] - Verified and completed
- [DATE]: [[learning/topics/[concept]|[CONCEPT]]] - Verified and completed

### Upcoming Reviews
- [DATE]: [[learning/topics/[concept]|[CONCEPT]]] - Scheduled verification
```

### 8. Report Summary

```markdown
## Progress Update Complete

### Session Stats
- **Items Reviewed**: [count]
- **Passed**: [count] ✅
- **Needs Review**: [count] 📝
- **Continue Learning**: [count] 📚

### Knowledge Debt Reduction
- **Starting Debt**: [X items]
- **Current Debt**: [Y items]
- **Session Reduction**: -[Z items] 🎉

### Memory Bank Contributions
- Added [X] insights to [[systemPatterns|project patterns]] and [[decisionLog|decisions]]

### Next Steps
1. [[learning/topics/[concept]|[Next high-priority item to study]]]
   - Est. time: [X] min
   - Priority: HIGH

2. **Scheduled Reviews**
   - [Date]: [[learning/topics/[concept]|[Concept review]]]

### Quick Links

- [[register/index|📋 Knowledge Debt Register]]
- [[sessions/[date]_progress|📝 This Session]]
- [[productContext|Project Context]] | [[systemPatterns|Patterns]] | [[decisionLog|Decisions]]
```

## Quick Commands

During the workflow, users can use these shortcuts:
- `skip` - Skip current question, mark for later
- `hint` - Get a hint for the current question
- `resources` - Show learning resources for current concept
- `context` - Show project context for current concept

## Integration Notes

- This workflow completes the KDR cycle: Identify → Learn → **Verify → Update**
- Run after `/kdr-analyze` or `/kdr-session` has identified gaps
- Insights contributed to Memory Bank improve future AI assistance
- Track trends over time to measure learning velocity

## Best Practices

1. **Be honest** - The quiz is for your benefit, not to "pass"
2. **Take notes** - If you struggle, note what specifically was unclear
3. **Contribute back** - Memory Bank contributions help future sessions
4. **Regular cadence** - Weekly progress checks prevent debt accumulation
5. **Celebrate wins** - Completed items represent real growth! 🎉
