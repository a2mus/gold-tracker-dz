---
description: Pull crash logs from connected Android device to project directory
---

# Pull Crash Log

> [!CAUTION]
> **This workflow is ANALYSIS ONLY. It does NOT execute fixes or modify any source code.**

This workflow pulls the crash log from the connected Android device, analyzes it, and generates a structured bug description that can be fed into the `/speckit-specify` workflow.

## Prerequisites
- Android device connected via USB or emulator running
- USB debugging enabled on device
- ADB available in PATH or Android SDK installed

## Steps

### 1. Check Device Connection

**Option A: Android MCP** (if available):
```
Use `mcp_android-mcp_execute_adb_shell_command` with command "devices"
```

**Option B: Direct ADB** (fallback):
// turbo
```powershell
adb devices
```

If no devices are listed, inform the user and stop.

### 2. Pull Crash Log

**Option A: Android MCP** (if available):
```
Use `mcp_android-mcp_execute_adb_shell_command` with command:
"cat /sdcard/Android/data/com.dzlivreur.app/files/crash_logs/crash.log"
Save output to crash.log
```

**Option B: Direct ADB** (fallback):
For Windows (default):
```powershell
adb shell cat /sdcard/Android/data/com.dzlivreur.app/files/crash_logs/crash.log > crash.log 2>&1
```

Alternative for emulators (specify device):
```powershell
adb -s emulator-5554 shell cat /sdcard/Android/data/com.dzlivreur.app/files/crash_logs/crash.log > crash.log 2>&1
```

### 3. View and Analyze Crash Log

// turbo
Read the `crash.log` file from the project root:
```powershell
Get-Content .\crash.log
```

If the file is empty or contains an error message like "No such file", inform the user that no crash log exists.

### 4. Parse Crash Information

From the crash log, extract:
- **Timestamp**: When the crash occurred
- **Exception Type**: The Java/Kotlin exception class (e.g., `SecurityException`, `NullPointerException`)
- **Exception Message**: The error message
- **Root Cause**: The first non-library stack frame (from `com.dzlivreur.app.*`)
- **Affected Component**: The screen/class where the crash originated
- **Stack Trace Summary**: Key frames showing the crash path

### 5. Investigate Related Code

Based on the crash location:
1. Find the affected source file(s)
2. Identify the specific function/composable
3. Note any relevant patterns (permissions, state, navigation)

**Optional: Research with Context7** (if available):
- If crash involves framework/library code, use `mcp_context7_query-docs` to:
  - Research the exception type in official documentation
  - Find best practices for handling similar errors
  - Understand framework-specific error patterns

**Optional: Check Firebase** (if Firebase-related crash):
- Use `mcp_firebase-mcp-server_firebase_get_environment` to check Firebase configuration
- Verify Firebase Security Rules if permission-related
- Check Firebase project status

**DO NOT modify any code. Only read and analyze.**

### 6. Generate Bug Description

Create a structured bug description in the following format that can be used with `/speckit-specify`:

```markdown
## Bug Report: [Short Description]

### Summary
[One-sentence description of what's happening]

### Environment
- **Device**: [Device/Emulator info from adb devices]
- **Crash Timestamp**: [From crash log]
- **App Version**: [If available]

### Steps to Reproduce
1. [Step 1 - e.g., "Navigate to the All Clients Map screen"]
2. [Step 2 - e.g., "Wait for map to load"]
3. [Observed: App crashes]

### Expected Behavior
[What should happen instead]

### Actual Behavior
[What actually happens - the crash]

### Technical Analysis

#### Exception
- **Type**: [Exception class]
- **Message**: [Error message]

#### Stack Trace (Key Frames)
```
[Relevant stack frames, especially from com.dzlivreur.app.*]
```

#### Affected Files
- `[file1.kt]` - [brief description of relevance]
- `[file2.kt]` - [brief description of relevance]

#### Root Cause Analysis
[Explanation of why the crash is happening based on code analysis]

### Suggested Fix Approach
[High-level description of what needs to change - NO CODE]

### Related Patterns
- [Any similar issues in the codebase]
- [Relevant architectural patterns that apply]
```

### 7. Present Report (END OF WORKFLOW)

Present the bug description to the user and **STOP**.

> [!IMPORTANT]
> **STOP HERE.** This workflow ends after presenting the bug report.
> Do NOT proceed to fix or implement any changes without user approval.

### 8. Save to Obsidian (Optional)

If Obsidian MCP server is available, offer to save the crash analysis:
- Use `mcp_obsidian_create_vault_file` to create a new note in the vault
- Link the crash report to related project notes using Obsidian internal links
- Tag with relevant categories (e.g., #crash, #android, #firebase)
- Use `mcp_obsidian_search_vault_smart` to find similar crash patterns in vault history
- This enables better knowledge management and pattern recognition across crashes

## Next Steps (User Must Invoke Separately)

After reviewing the bug report:
- `/speckit-specify` - Create a formal bug fix specification from the report
- `/speckit-plan` - Create technical implementation plan for the fix

## Notes
- The `crash.log` file will be saved in the project root
- If no crash has occurred since the app was installed, the log file won't exist
- Add `crash.log` to `.gitignore` to avoid committing it
- Multiple crashes may be logged in the same file (separated by `====` lines)
