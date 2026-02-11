---
description: Analyze project knowledge debt independently using Memory Bank and SpecKit context
---

# Knowledge Debt Reduction - Analyze

Perform an independent knowledge debt audit. This workflow analyzes your project's Memory Bank and SpecKit artifacts to identify architectural patterns, decisions, and concepts that may represent knowledge gaps.

> **IMPORTANT**: This agent does NOT generate solutions or write code. It ONLY identifies knowledge gaps and helps you understand what you should learn.

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

- Periodically (weekly/monthly) to audit your understanding of the project
- When onboarding to a new codebase
- After significant architectural changes
- When you feel you've been copy-pasting AI solutions without understanding

## Prerequisites

- Memory Bank must exist with core files
- SpecKit features (optional but recommended)

## Steps

### 1. Load Memory Bank Context

Read and analyze these files:
- [[productContext]] - Project goals and domain
- [[systemPatterns]] - Architectural patterns in use
- [[decisionLog]] - Historical decisions and rationale
- [[activeContext]] - Current focus areas

Extract:
- **Domain concepts**: What business logic does this project implement?
- **Patterns**: What architectural/coding patterns are established?
- **Technologies**: What frameworks, libraries, tools are used?
- **Decisions**: What choices were made and why?

### 2. Enrich with Official Documentation (using context7 or firecrawl)

**Option A: Context7 MCP** (if available - RECOMMENDED):
For each technology/framework identified:
- Use `mcp_context7_resolve-library-id` to find the library
- Use `mcp_context7_query-docs` to fetch relevant documentation
- Cross-reference project usage with official best practices
- Identify gaps between project implementation and recommended patterns
- This helps distinguish between "project-specific patterns" and "standard framework usage"

**Option B: Firecrawl MCP** (if available):
For technologies without Context7 coverage:
- Use `mcp_firecrawl_firecrawl_search` to search for official documentation
- Use `mcp_firecrawl_firecrawl_scrape` to extract content from documentation pages
- Gather best practices and usage patterns

**Option C: Manual Research** (fallback):
- Use standard web search and documentation reading

### 3. Scan SpecKit Artifacts

If `specs/` folder exists, scan for:
- `spec.md` files - Feature requirements and acceptance criteria
- `plan.md` files - Technical implementation approaches
- `research.md` files - Technical decisions and alternatives considered

Extract:
- **Features implemented**: What has been built?
- **Technical approaches**: How were problems solved?
- **Rationale**: Why were certain approaches chosen?

### 4. Build Knowledge Map

Create a structured list of concepts organized by category:

```markdown
## Knowledge Map

### Architectural Patterns
- [ ] MVVM Architecture (ViewModels + Compose)
- [ ] Repository Pattern (Firebase abstraction)
- [ ] State Management (StateFlow + collectAsState)

### Framework Features
- [ ] Jetpack Compose (@Composable, Modifiers)
- [ ] Jetpack Navigation (NavController, destinations)
- [ ] Material 3 (Theming, Components)

### External Services
- [ ] Firebase Firestore (CRUD, queries, listeners)
- [ ] Firebase Auth (Authentication flow)
- [ ] Google Maps API (MapView, markers)

### Language Features
- [ ] Kotlin Coroutines (suspend, Flow, scope)
- [ ] Sealed Classes (state representation)
- [ ] Data Classes (immutable models)

### Domain Knowledge
- [ ] [Project-specific business logic]
```

### 5. Interactive Knowledge Assessment

For each concept category, run an interactive assessment:

```
🔍 KNOWLEDGE CHECK: [CATEGORY NAME]

I found these concepts used in your project:

1. [Concept 1] - Used in: [file/component references]
2. [Concept 2] - Used in: [file/component references]
3. [Concept 3] - Used in: [file/component references]

For each concept, rate your understanding:
A) Very familiar - I could explain it to others
B) Somewhat familiar - I've used it but have gaps
C) Heard of it - Need clarification
D) New to me - Please explain

Enter your ratings (e.g., "1A, 2B, 3D"):
```

### 6. Process Responses

**For A (Very Familiar)**:
- Mark as known
- Move to next concept

**For B (Somewhat Familiar)**:
```markdown
### Quick Refresher: [CONCEPT]

**Definition**: [2-3 sentence explanation]

**In Your Codebase**:
See `[file path]` where this is used:
- [[_code/path/to/[file path]|[file path]]] (click to open in IDE)


**Memory Bank Reference**:
See [[systemPatterns#[section]|Pattern documentation]]

**Connection to Project Goals**:
From [[productContext]]: [how this serves project goals]
```

**For C or D (Needs Learning)**:
```markdown
### Learning Required: [CONCEPT]

**Priority**: [HIGH/MEDIUM/LOW based on usage frequency]

**Definition**: [Full explanation, 3-4 sentences]

**Why This Matters in YOUR Project**:
[Connect to specific project features and goals]

**Where It's Used**:
- `[file1.kt]`: [[_code/app/src/main/java/[path]/[file1.kt]|[file1.kt]]]
- `[file2.kt]`: [[_code/app/src/main/java/[path]/[file2.kt]|[file2.kt]]]


**Architecture Connection**:
See [[systemPatterns#[section]|Architecture docs]] for related pattern

**Decision Context**:
See [[decisionLog#[decision]|Decision rationale]] for why this approach was chosen

🎯 **Added to [[register/index|Knowledge Debt Register]]**
```

### 7. Update Knowledge Debt Register

Create/update `knowledge-debt/register/index.md`:

```markdown
# Knowledge Debt Register

**Last Updated**: [TIMESTAMP]
**Developer**: [if known]

## Dashboard

| Priority | Count | Trend |
|----------|-------|-------|
| HIGH     | X     | ↑↓→   |
| MEDIUM   | Y     | ↑↓→   |
| LOW      | Z     | ↑↓→   |

## Active High-Priority Items

### [CONCEPT NAME]
- **Identified**: [date]
- **Category**: [Architectural/Framework/Domain/etc.]
- **Used In**: [[_code/app/src/main/java/[path]/[file1]|[file1]]], [[_code/app/src/main/java/[path]/[file2]|[file2]]]
- **Memory Bank Refs**: [[systemPatterns#[section]|Pattern]] | [[decisionLog#[entry]|Decision]]
- **Learning Topic**: [[learning/topics/[concept_name]|Topic Guide]]
- **Why Critical**: [impact on understanding]
- **Est. Learning Time**: [realistic estimate]
- **Status**: [ ] Not started / [/] In progress / [x] Completed

## Learning Resources

See [[learning/topics/[concept]|Learning Topic]] for curated resources.
```

### 8. Create Session File

Save detailed analysis to `knowledge-debt/sessions/[YYYY-MM-DD]_analyze.md`:

```markdown
# Knowledge Debt Analysis Session

**Date**: [TIMESTAMP]
**Mode**: Independent Analysis
**Memory Bank State**: [[productContext]] | [[systemPatterns]] | [[decisionLog]] | [[activeContext]]
**SpecKit Features**: [list features scanned]

## Concepts Assessed

| Concept | Category | Rating | Action | Topic Link |
|---------|----------|--------|--------|------------|
| [name]  | [cat]    | A/B/C/D| [action taken] | [[learning/topics/[name]\|Learn]] |

## New Debt Items Added

Items added to [[register/index|Knowledge Debt Register]]:
- [[learning/topics/[concept1]|Concept 1]]
- [[learning/topics/[concept2]|Concept 2]]

## Patterns Detected

[Any recurring themes or foundational gaps identified]
See [[systemPatterns]] for documented project patterns.

## Recommended Focus

This week: [[learning/topics/[priority_topic]|[Topic Name]]] - Est. [X] min
```

### 9. Curate Learning Resources

For each HIGH priority gap, create/update topic file in `knowledge-debt/learning/topics/[concept].md`:

```markdown
# Learning: [CONCEPT NAME]

**Context**: Used in [project feature] following [[systemPatterns#[pattern]|this pattern]]
**Register Entry**: [[register/index#[Concept Name]|View in Register]]

## Quick Understanding (15 min)

📖 **Article**: [Title]
- URL: [link]
- Read sections: [specific parts]
- Skip: [irrelevant parts for your stack]
- **Connection**: After reading, review [[systemPatterns#[section]|Memory Bank pattern]]

## Hands-On Practice (30-45 min)

🛠️ **Tutorial**: [Title]
- URL: [link]
- Focus on: [specific techniques you use]
- Build: [what you'll create]

## Reference Documentation

📚 **Official Docs**: [Title]
- URL: [link]
- Bookmark: [specific sections]
- Use when: [scenarios in your project]

## Project References

- **Pattern docs**: [[systemPatterns#[related section]|Architecture]]
- **Decision context**: [[decisionLog#[related entry]|Why this approach]]
- **Related topics**: [[learning/topics/[related_topic]|Related Concept]]

## Self-Validation

After learning, you should be able to:
- [ ] Explain why [[systemPatterns#[pattern]|this pattern]] is used over alternatives
- [ ] Implement a similar feature independently
- [ ] Understand the decision in [[decisionLog#[entry]|decision log]]

---
← Back to [[register/index|Knowledge Debt Register]]
```

### 10. Sync to Obsidian (Optional)

If Obsidian MCP server is available:
- Use `mcp_obsidian` tools to create/update notes in the vault
- Create bidirectional links between knowledge debt topics and project notes
- Tag learning topics with relevant categories (e.g., #learning, #android, #architecture)
- This enables better knowledge management and cross-referencing across the vault

### 11. Report Summary

Output final summary:

```markdown
## Analysis Complete

**Concepts Scanned**: [count]
**Already Known**: [count] ✓
**Needs Refresher**: [count] 📝
**New Learning Required**: [count] 📚

### Top Priority This Week

1. **[Concept]** - Est. [X] min
   - Why: [brief reason]
   - Resources: [[learning/topics/[concept]|Start Learning]]

### Quick Links

- [[register/index|📋 Knowledge Debt Register]]
- [[sessions/[date]_analyze|📝 This Session]]
- [[learning/topics/[topic1]|📚 Topic 1]] | [[learning/topics/[topic2]|📚 Topic 2]]

### Memory Bank Context

- [[productContext|Project Context]] | [[systemPatterns|Patterns]] | [[decisionLog|Decisions]]
```

## Notes

- Run this workflow periodically (suggest: weekly)
- Focus on HIGH priority items first
- Track progress in the register
- Update Memory Bank when you gain insights from learning
