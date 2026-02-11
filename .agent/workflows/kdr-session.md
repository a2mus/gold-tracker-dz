---
description: Analyze knowledge gaps after AI-assisted code changes or fixes
---

# Knowledge Debt Reduction - Session

Analyze knowledge gaps after another AI agent has provided solutions, implementations, or fixes. This workflow examines the current context to identify concepts you should understand.

> **IMPORTANT**: This agent does NOT generate solutions or write code. It ONLY analyzes what was done and helps you understand it.

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

- After receiving an AI-generated solution you don't fully understand
- After an AI agent has fixed a bug or implemented a feature
- When you want to learn from code that was just written
- Before blindly copy-pasting AI suggestions

## Prerequisites

- Recent AI interaction context (conversation, changed files)
- Memory Bank exists with core files

## Steps

### 1. Capture Current Context

Identify what was just done:
- **Changed Files**: What files were created/modified?
- **Solution Type**: Bug fix? New feature? Refactor?
- **Conversation Context**: What was the request and response?

Ask the user if context is unclear:
```
What would you like me to analyze for knowledge gaps?
A) The last AI-assisted change (I'll detect from context)
B) Specific files: [list files]
C) A concept I want to understand better: [describe]
```

### 2. Load Memory Bank Context

Read for institutional knowledge:
- [[productContext]] - Project goals
- [[systemPatterns]] - Established patterns
- [[decisionLog]] - Historical decisions
- [[activeContext]] - Current focus

This distinguishes **what the PROJECT knows** from **what YOU need to know**.

### 3. Extract Concepts from Solution

Analyze the solution/changes and extract:

```markdown
## Concepts Used in This Solution

### Institutional Knowledge (Documented in Memory Bank)
✓ Already in project documentation:
- [Concept 1]: See [[systemPatterns#[section]|Pattern docs]]
- [Concept 2]: Decision logged in [[decisionLog#[entry]|Decision log]]
- [Pattern]: Defined in [[systemPatterns#[section]|architecture section]]

### Technical Concepts (Your Understanding Required)
? Verify your understanding:
- [Concept A]: Used in lines [X-Y] of [[_code/app/src/main/java/[path]/[file]|[File]]]

- [Concept B]: Core to this solution approach
- [Concept C]: Underlying mechanism

### Framework/Library Usage
- [Framework Feature 1]: [how it's used]
- [Framework Feature 2]: [how it's used]

### Language Features
- [Language Feature 1]: [where used]
- [Language Feature 2]: [where used]
```

### 4. Distinguish Knowledge Layers

Present the distinction clearly:

```markdown
## Knowledge Layer Analysis

### 🏢 Project Knowledge (Memory Bank Has This)
These concepts are documented in your project. You can reference them anytime:

| Concept | Where Documented | Why It's Here |
|---------|------------------|---------------|
| [Pattern] | [[systemPatterns#[section]\|Pattern docs]] | Established project standard |
| [Decision] | [[decisionLog#[entry]\|Decision entry]] | Chosen on [date] because [reason] |

### 👤 Developer Knowledge (Your Understanding)
These concepts are used in the solution. Let's verify your understanding:

1. **[Concept Name]**
   - Used in: [[File]](file:///path/to/[file]):[lines]
   - Purpose: [what it does in this context]
   - Learn more: [[learning/topics/[concept]\|Topic Guide]]
   
2. **[Concept Name]**
   - Used in: [[File]](file:///path/to/[file]):[lines]
   - Purpose: [what it does in this context]
   - Learn more: [[learning/topics/[concept]\|Topic Guide]]
```

### 5. Interactive Knowledge Check

For each concept in "Developer Knowledge":

```
🔍 Knowledge Check: [CONCEPT]

**Context**: This was used in [specific part of solution]
**Purpose**: [why it's needed here]

Code Reference:
```[language]
// [relevant code snippet with annotations]
```

Question: How familiar are you with [CONCEPT]?
A) Very familiar - I could explain it to others
B) Somewhat familiar - I've used it before
C) Heard of it - but need clarification
D) New to me - please explain

[Wait for response]
```

### 6. Process Responses

**Response A (Very Familiar)**:
```
Great! ✓ [CONCEPT] marked as known.
[Move to next concept]
```

**Response B (Somewhat Familiar)**:
```markdown
### Targeted Refresher: [CONCEPT]

**Quick Definition**: [2-3 sentences]

**In This Solution** (lines [X-Y]):
```[language]
[code snippet with inline annotations]
```
This implements [concept] by [mechanism].

**Memory Bank Connection**:
This aligns with [[systemPatterns#[section]|this pattern]] because [reason].

**Official Documentation** (using context7 or firecrawl):
**Option A: Context7 MCP** (if available - RECOMMENDED):
  Use `mcp_context7_query-docs` to fetch relevant official documentation for this concept.
  Present key excerpts that clarify the usage in this specific context.

**Option B: Firecrawl MCP** (if available):
  Use `mcp_firecrawl_firecrawl_search` to find official documentation and tutorials.
  Use `mcp_firecrawl_firecrawl_scrape` to extract detailed content from documentation pages.

**Confidence Check**: Does this clarify the usage? (Y/N)
```

**Response C or D (Needs Learning)**:
```markdown
### Learning Required: [CONCEPT]

**Foundation Explanation**:
[3-4 sentences with clear definition]

**Why It Matters Here**:
[Connect to the specific solution and project goals]

**In Your Code** (lines [X-Y]):
```[language]
[code snippet]
// ← [annotation explaining this line]
// ← [annotation explaining this line]
```

**Architecture Context**:
From [[systemPatterns#[section]|Pattern docs]]: This follows [pattern] because [reason].

**SpecKit Connection** (if applicable):
This addresses requirement from [[specs/[feature]/spec|Feature Spec]].

🎯 **Added to [[register/index|Knowledge Debt Register]]** - Priority: [HIGH/MEDIUM/LOW]
```

### 7. Update Session File

Create `knowledge-debt/sessions/[YYYY-MM-DD]_[feature-name].md`:

```markdown
# Knowledge Debt Session

**Date**: [TIMESTAMP]
**Mode**: Post-AI-Fix Analysis
**Trigger**: [What prompted this analysis]
**Memory Bank**: [[productContext]] | [[systemPatterns]] | [[decisionLog]] | [[activeContext]]

## Solution Analyzed

**Files Changed**:
- `[file1.kt]`: [[_code/path/to/[file1.kt]|[File 1]]] - [brief description]
- `[file2.kt]`: [[_code/path/to/[file2.kt]|[File 2]]] - [brief description]


**Solution Type**: [Bug fix / Feature / Refactor]

## Institutional Knowledge Used

| Concept | Memory Bank Reference |
|---------|----------------------|
| [Pattern] | [[systemPatterns#[section]\|Pattern docs]] |
| [Decision] | [[decisionLog#[entry]\|Decision entry]] |

## Concepts Assessed

| Concept | Rating | Action Taken | Topic |
|---------|--------|--------------|-------|
| [name] | A/B/C/D | [refresher/learning/known] | [[learning/topics/[name]\|Learn]] |

## New Debt Items

- **[Concept]** - Priority: [HIGH/MEDIUM/LOW]
  - Used in: [[_code/app/src/main/java/[path]/[file1]|[File1]]], [[_code/app/src/main/java/[path]/[file2]|[File2]]]

  - Added to [[register/index|Register]]
  - Topic: [[learning/topics/[concept]|Start Learning]]

## Memory Bank Update Suggestions

Consider adding to [[decisionLog]]:
```
[DATE]: [Decision description]
Decision: [What was chosen]
Rationale: [Why - what you learned]
```

Consider adding to [[systemPatterns]]:
```
[Pattern description if new pattern was used]
```
```

### 8. Update Knowledge Debt Register

Add new items to `knowledge-debt/register/index.md` under appropriate priority:

```markdown
### [CONCEPT NAME]
- **Identified**: [date]
- **Context**: [feature/fix that triggered this]
- **Category**: [Architectural/Framework/Domain/Language]
- **Used In**: [file references from this session]
- **Memory Bank Refs**: [[systemPatterns#[section]|Pattern]] | [[decisionLog#[entry]|Decision]]
- **Learning Topic**: [[learning/topics/[concept_name]|Start Learning]]
- **Why Important**: [impact on understanding this solution]
- **Est. Learning Time**: [realistic estimate]
- **Status**: [ ] Not started
```

### 9. Curate Context-Aware Resources

For HIGH priority items, create/update `knowledge-debt/learning/topics/[concept].md`:

Focus resources on YOUR context:
- Find examples similar to YOUR tech stack
- Link to sections relevant to YOUR architecture
- Reference YOUR Memory Bank alongside external docs
- **Use Context7 MCP** (if available - RECOMMENDED) to fetch official documentation:
  - Use `mcp_context7_resolve-library-id` to find the exact library
  - Use `mcp_context7_query-docs` to get targeted documentation
  - Include relevant code examples from official docs
- **Use Firecrawl MCP** (if available) for additional resources:
  - Use `mcp_firecrawl_firecrawl_search` to find tutorials and guides
  - Use `mcp_firecrawl_firecrawl_scrape` to extract content from learning resources
- **Use Obsidian MCP** (if available) to find related notes:
  - Use `mcp_obsidian_search_vault_smart` to search for similar concepts in vault
  - Cross-reference with past learning sessions and project notes

```markdown
# Learning: [CONCEPT]

**Project Context**: 
Used in [[_code/app/src/main/java/[path]/[file]|[File]]] following pattern from `systemPatterns.md#[section]`.
**Register Entry**: [[register/index#[Concept Name]|View in Register]]

## Your Use Case

You encountered this while: [description of solution/fix]

The code does this:
```[language]
[annotated code from the solution]
```

## Focused Learning Path

### 1. Quick Understanding (10-15 min)
📖 [Resource]: [URL]
- Read sections: [specific]
- **Then**: Re-read [[systemPatterns#[section]|pattern docs]] with new understanding

**Official Documentation** (via context7):
[Relevant excerpts from official docs fetched via MCP]

### 2. Hands-On Practice (30 min)
🛠️ [Resource]: [URL]
- Focus on: [aspects matching your usage]
- **Then**: Look at your code again with fresh eyes

### 3. Reference
📚 [Docs]: [URL]
- Bookmark: [sections]
- Use when: [scenarios in your project]

## Project References

- **Pattern docs**: [[systemPatterns#[related section]|Architecture]]
- **Decision context**: [[decisionLog#[related entry]|Why this approach]]
- **Related topics**: [[learning/topics/[related_topic]|Related Concept]]

## Validation

After learning:
- [ ] Can explain why the solution uses [concept]?
- [ ] Could modify this code if requirements changed?
- [ ] Understand the [[systemPatterns|Memory Bank pattern documentation]]?

---
← Back to [[register/index|Knowledge Debt Register]]
```

### 9.5 Sync to Obsidian (Optional)

If Obsidian MCP server is available:
- Use `mcp_obsidian_create_vault_file` to save session analysis to Obsidian vault
- Use `mcp_obsidian_search_vault_smart` to find related project documentation
- Create bidirectional links between session notes and related project documentation
- Tag with relevant categories for easy retrieval (e.g., #learning, #knowledge-debt, #[technology])
- Enable cross-referencing with other learning sessions and project patterns

### 10. Report Summary

```markdown
## Session Complete

**Solution Analyzed**: [brief description]
**Concepts Extracted**: [count]
**Already Known**: [count] ✓
**Refreshed**: [count] 📝
**New Learning**: [count] 📚

### Immediate Learning Priority

**[Concept]** - Est. [X] min
- Why: Critical to understanding this solution
- Resources: [[learning/topics/[concept]|Start Learning]]

### Quick Links

- [[register/index|📋 Knowledge Debt Register]]
- [[sessions/[date]_[feature]|📝 This Session]]
- [[learning/topics/[topic]|📚 Priority Topic]]

### Memory Bank Contributions

If you feel confident after learning:
- Add insight to [[decisionLog]]
- Update [[systemPatterns]] if pattern isn't documented

### Memory Bank Context

- [[productContext|Project Context]] | [[systemPatterns|Patterns]] | [[decisionLog|Decisions]]
```

## Integration with Other Workflows

This workflow is designed to run AFTER:
- `/speckit-implement` - After implementation is complete
- Any bug fix or feature implementation by an AI agent
- Code review where AI suggested changes

## Notes

- Keep session files focused on one solution/change
- Reference Memory Bank to avoid "re-learning" documented concepts
- Suggest Memory Bank updates when you gain confidence
- Focus on understanding YOUR code, not abstract theory
