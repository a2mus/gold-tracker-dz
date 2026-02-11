---
description: Execute the implementation plan created by /plan-with-opus
---

# Execute with Gemini (The Builder)

> **Role**: Gemini 3.0 Flash/Pro serves as the **Builder** - responsible for Execution, Coding, Frontend styling, and scaffolding.
> 
> **Strength**: Almost unlimited rate limits and extremely fast execution. Perfect for heavy lifting.

This workflow executes the implementation plan created by the `/plan-with-opus` workflow (The Architect).

## The Architect-Builder Strategy

This workflow follows the "Architect-Builder" model:
- **Opus (Architect)**: Created the detailed plan with bifurcated Backend/Frontend tasks
- **Gemini (Builder)**: Reads the high-level architecture and writes the boilerplate/implementation code instantly

## Purpose
- Read and understand the implementation plan from Opus
- Execute Backend tasks (B1, B2...) systematically
- Execute Frontend tasks (F1, F2...) with design skill
- Write production-grade, well-documented code
- Update progress as work is completed
- Verify the implementation works correctly

## Special Modes

### King Mode (For Backend/Logic)
When executing Backend tasks or complex logic:
- Zero fluff, no philosophical lectures, output first
- Focus on clean, efficient implementation

### UltraThink Mode (For Complex Tasks)
When a task is marked with "Use UltraThink mode":
- Suspend zero-fluff rule
- Max depth analyze through psychological AND technical lens
- Prioritize performance over speed
- Consider edge cases (memory overhead, race conditions)

### Frontend Design Skill (For UI/UX)
When executing Frontend tasks:
- Avoid generic "AI slop" designs (standard Bootstrap/Tailwind looks)
- Follow established UI patterns in `memory-bank/systemPatterns.md`
- Use project's established component library
- Implement smooth animations and micro-interactions

## Prerequisites
- Implementation plan exists at `memory-bank/implementation-plan.md`
- Plan has been reviewed and approved by the user
- Backend (B) and Frontend (F) tasks are clearly defined

## Steps

### 1. Load the Implementation Plan
// turbo
```bash
cat memory-bank/implementation-plan.md
```

Read and understand the full architecture from Opus before proceeding.

### 2. Verify Prerequisites
- Check that all dependencies mentioned in the plan are available
- Ensure the workspace is in a clean state
- Confirm no conflicting changes are in progress
- Review `memory-bank/systemPatterns.md` for coding patterns to follow

### 3. Execute Backend Tasks (B1, B2, B3...)

Execute Backend tasks in order using **King Mode** principles:

#### 3.1 Announce Current Backend Step
"Executing Backend Step BX: [Step Name]"

#### 3.2 Implement the Backend Step
- Create/modify/delete files as specified by Opus
- Follow the project's established patterns from `memory-bank/systemPatterns.md`
- Write clean, well-documented code
- Handle edge cases as documented in the plan
- If marked "UltraThink", analyze deeply before implementing

#### 3.3 Verify the Backend Step
// turbo
After each significant change, verify no syntax errors:
```bash
./gradlew assembleDebug --dry-run 2>&1 | head -50
```

#### 3.4 Update Progress
Mark the completed step in `memory-bank/implementation-plan.md`:
- Change `- [ ]` to `- [x]` for completed items

### 4. Execute Frontend Tasks (F1, F2, F3...)

Execute Frontend tasks in order using **Frontend Design Skill** principles:

#### 4.1 Announce Current Frontend Step
"Executing Frontend Step FX: [Step Name]"

#### 4.2 Implement the Frontend Step
- Follow the aesthetic direction specified in the plan
- Use project's established UI components
- Implement animations and micro-interactions
- Avoid generic designs - follow project's design language
- Handle edge cases as documented in the plan

#### 4.3 Verify the Frontend Step
// turbo
After each significant change, verify no syntax errors:
```bash
./gradlew assembleDebug --dry-run 2>&1 | head -50
```

#### 4.4 Update Progress
Mark the completed step in `memory-bank/implementation-plan.md`:
- Change `- [ ]` to `- [x]` for completed items

### 5. Build Verification
// turbo
After completing all steps, verify the project compiles:
```bash
./gradlew assembleDebug 2>&1 | tail -100
```

### 6. Run Lint/Tests (if applicable)
// turbo
```bash
./gradlew lintDebug 2>&1 | tail -50
```

### 6.5 Automated Testing (Optional - using TestSprite MCP)

If TestSprite MCP server is available and testing is required:
- Use `mcp_TestSprite_testsprite_bootstrap` to initialize testing environment
- Use `mcp_TestSprite_testsprite_generate_frontend_test_plan` for UI components
- Use `mcp_TestSprite_testsprite_generate_backend_test_plan` for backend logic
- Use `mcp_TestSprite_testsprite_generate_code_and_execute` to run automated tests
- Review test results and fix any failures before proceeding

### 7. Update Memory Bank

Update the following files after successful implementation:

#### 7.1 Update `memory-bank/progress.md`
Add completed tasks to the progress log.

#### 7.2 Update `memory-bank/activeContext.md`
Document what was implemented and the current state.

#### 7.3 Update `memory-bank/decisionLog.md` (if applicable)
Log any architectural decisions made during implementation.

### 8. Final Report
Provide a summary to the user:
- What was implemented (Backend + Frontend tasks completed)
- Any deviations from the original plan
- Issues encountered and how they were resolved
- Suggestions for next steps or improvements

## Error Handling

### If Build Fails
1. Analyze the error message
2. Fix the specific issue
3. Re-run build verification
4. Continue with remaining steps

### If Complex Bug Encountered
1. Document the issue clearly
2. **Switch back to Opus** for debugging
3. Opus excels at "one-shot debugging" and finding root causes
4. Resume execution after fix is identified

### If Plan is Incomplete
1. Note what's missing
2. Ask user for clarification
3. Optionally run `/plan-with-opus` again to update the plan

### If Step Conflicts with Existing Code
1. Document the conflict
2. Propose resolution options
3. Get user approval before proceeding

## Output Checklist
- [ ] All Backend tasks (B1-Bn) completed
- [ ] All Frontend tasks (F1-Fn) completed  
- [ ] Project compiles without errors
- [ ] No new lint warnings introduced
- [ ] Memory bank updated with progress
- [ ] User notified of completion

## Notes
- Follow the Opus plan strictly unless you encounter issues
- Document any deviations from the plan
- For complex bugs, switch back to Opus for debugging
- Keep commits atomic and well-described (if using git)
- Test functionality on device when UI changes are involved (use `/verify_ui`)
- Use King Mode for backend: zero fluff, output first
- Use Frontend Design Skill for UI: avoid generic aesthetics
