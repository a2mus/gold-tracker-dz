---
name: skill-creator
description: |
  Guide for creating effective skills that extend Antigravity's capabilities with
  specialized knowledge, workflows, or tool integrations. Use when users want to
  create a new skill or update an existing skill.
---

# Skill Creator

Create effective skills that extend agent capabilities with specialized knowledge and workflows.

## About Skills

Skills are modular, self-contained packages that extend capabilities by providing
specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for
specific domains or tasks—they transform a general-purpose agent into a specialized one
equipped with procedural knowledge.

### What Skills Provide

1. **Specialized workflows** - Multi-step procedures for specific domains
2. **Tool integrations** - Instructions for working with specific file formats or APIs
3. **Domain expertise** - Company-specific knowledge, schemas, business logic
4. **Bundled resources** - Scripts, references, and assets for complex and repetitive tasks

---

## Core Principles

### Concise is Key

The context window is a public good. Skills share the context window with everything else:
system prompt, conversation history, other skills' metadata, and the actual user request.

**Default assumption: The agent is already very smart.** Only add context it doesn't already have.

### Set Appropriate Degrees of Freedom

| Scenario | Approach |
|----------|----------|
| Creative tasks | Leave room for interpretation |
| Precise tasks | Provide exact specifications |
| Workflow tasks | Define clear steps with flexibility in execution |

---

## Skill Anatomy

A skill is a folder with the following structure:

```
skill-name/
├── SKILL.md           # Required: Instructions and metadata
├── scripts/           # Optional: Helper scripts
├── examples/          # Optional: Reference implementations
└── resources/         # Optional: Assets, templates, data
```

### SKILL.md Format

```markdown
---
name: my-skill-name
description: |
  A clear description of what this skill does and when to use it.
  This should be detailed enough to help route requests correctly.
---

# Skill Title

[Main instructions for using the skill]

## When This Skill Applies

[Clear triggers for activation]

## Workflow

[Step-by-step process]

## Reference

[Resources and documentation]

## Keywords

[comma, separated, keywords, for, matching]
```

---

## Skill Creation Process

### Step 1: Understand with Concrete Examples

Before creating the skill, gather concrete examples:
- What tasks should this skill handle?
- What does the ideal output look like?
- What are common failure modes?

### Step 2: Plan the Contents

Determine what the skill needs:
- **Instructions**: Core workflow and guidelines
- **Scripts**: Automation helpers (if needed)
- **Examples**: Reference implementations (if complex)
- **Resources**: Templates, data files (if needed)

### Step 3: Write the SKILL.md

#### Frontmatter (Required)

```yaml
---
name: skill-name          # Lowercase, hyphens for spaces
description: |
  Multi-line description of what the skill does
  and when it should be activated.
---
```

Only include `name` and `description` in frontmatter.

#### Body

Write clear, concise instructions that include:
1. **When to activate** - Clear triggers
2. **Core workflow** - Step-by-step process
3. **Examples** - Concrete usage patterns
4. **Resources** - Links to bundled files

### Step 4: Progressive Disclosure

Use this design principle:
- **SKILL.md**: Essential instructions only
- **Reference files**: Detailed documentation (load when needed)
- **Scripts**: Complex operations (use as black boxes)

### Step 5: Test and Iterate

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how to improve instructions
4. Update and test again

---

## Best Practices

### Good Skill Characteristics

✅ **Concise**: Only essential information in SKILL.md
✅ **Clear triggers**: When to activate is obvious
✅ **Actionable**: Instructions can be followed immediately
✅ **Complete**: All needed resources are included
✅ **Maintainable**: Easy to update as requirements change

### Common Mistakes

❌ **Too verbose**: Every possible scenario covered
❌ **Too vague**: No clear workflow
❌ **Missing context**: References files that don't exist
❌ **Over-engineered**: Complex when simple would work

---

## Example: Minimal Skill

```markdown
---
name: code-review
description: |
  Review code for quality, security, and best practices.
  Use when asked to review code, find bugs, or improve code quality.
---

# Code Review

## Process

1. Understand the code's purpose
2. Check for bugs and edge cases
3. Evaluate code quality and readability
4. Identify security concerns
5. Suggest improvements

## Focus Areas

- Error handling
- Input validation
- Performance implications
- Code organization
- Naming conventions

## Output Format

Provide review as:
- 🐛 **Bugs**: Issues that will cause problems
- ⚠️ **Warnings**: Potential issues
- 💡 **Suggestions**: Improvements
- ✅ **Strengths**: What's done well
```

---

## Keywords

skill creation, custom skills, agent skills, workflow automation, domain expertise
