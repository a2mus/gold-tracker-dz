# Android MCP Server Installation

**Date**: 2026-01-23
**Server**: android-mcp
**Repository**: https://github.com/minhalvp/android-mcp-server

## Installation Summary

✅ **Successfully installed** Android MCP Server

### Installation Steps Completed:
1. ✅ Cloned repository to `C:\Users\a2mus\.gemini\antigravity\mcp-servers\android-mcp-server`
2. ✅ Installed Python 3.11 using `uv`
3. ✅ Synced dependencies (24 packages installed)
4. ✅ Added configuration to `mcp_config.json`

## Server Capabilities

The Android MCP server provides control over Android devices through ADB with the following tools:

### 1. **get_screenshot()**
- Takes a screenshot of the connected Android device
- Returns: Image object
- **Use case**: Visual verification, UI testing, bug reporting

### 2. **get_uilayout()**
- Retrieves information about clickable elements in the current UI
- Returns: Formatted string with element details (text, content description, bounds, center coordinates)
- **Use case**: UI automation, accessibility testing, element location

### 3. **execute_adb_command(command: str)**
- Executes any ADB command and returns the output
- Args: ADB command string
- Returns: Command output
- **Use case**: Custom ADB operations, device control, debugging

### 4. **get_packages()**
- Gets all installed packages on the device
- Returns: List of all installed packages as a string
- **Use case**: Package management, app inventory, dependency checking

### 5. **get_package_action_intents(package_name: str)**
- Gets all non-data actions from Activity Resolver Table for a package
- Args: Package name
- Returns: List of action intents
- **Use case**: Understanding app capabilities, intent testing

## Configuration

### Device Selection
The server supports two modes:

1. **Automatic Selection** (Default)
   - No configuration needed
   - Automatically connects to the only connected device
   - Perfect for single device development

2. **Manual Selection** (Multiple Devices)
   - Create `config.yaml` from `config.yaml.example`
   - Specify device serial from `adb devices`
   - Example:
     ```yaml
     device:
       name: "13b22d7f"  # Your device serial
     ```

### Current Configuration
```json
{
  "android-mcp": {
    "command": "uv",
    "args": [
      "--directory",
      "C:\\Users\\a2mus\\.gemini\\antigravity\\mcp-servers\\android-mcp-server",
      "run",
      "server.py"
    ],
    "env": {}
  }
}
```

## Prerequisites

✅ Python 3.x (installed: 3.11.14)
✅ ADB (Android Debug Bridge) - already configured
✅ Android device or emulator
✅ `uv` package manager

## Usage in Workflows

This server is perfect for Android development workflows and can be integrated into:

### Recommended Integrations:

1. **pull-crash-log.md**
   - Use `execute_adb_command()` to pull crash logs
   - Use `get_screenshot()` to capture app state at crash
   - Use `get_uilayout()` to analyze UI state

2. **speckit-implement.md**
   - Use `get_screenshot()` for visual verification
   - Use `get_uilayout()` for UI testing
   - Use `get_packages()` to verify app installation

3. **New workflow: android-ui-test.md**
   - Automated UI testing using `get_uilayout()`
   - Screenshot comparison using `get_screenshot()`
   - Package verification using `get_packages()`

4. **New workflow: android-deploy-verify.md**
   - Verify app installation with `get_packages()`
   - Check app launch with `execute_adb_command()`
   - Capture screenshots for deployment verification

## Testing the Installation

To verify the server is working:

1. Connect your Android device via USB or start emulator
2. Verify device connection:
   ```bash
   adb devices
   ```
3. The MCP server will automatically connect to your device
4. Use MCP tools to interact with the device

## Next Steps

1. ✅ Server installed and configured
2. ⏳ Update workflows to use Android MCP tools
3. ⏳ Create Android-specific workflows
4. ⏳ Test integration with existing workflows

## Notes

- Server uses automatic device selection by default
- For multiple devices, create `config.yaml` with device serial
- All ADB commands are executed through the server
- Screenshots are returned as Image objects
- UI layout information includes clickable elements only
