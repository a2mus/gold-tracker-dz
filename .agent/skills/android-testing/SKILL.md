---
name: android-testing
description: |
  Toolkit for testing Android applications using instrumented tests, UI Automator,
  Espresso, and ADB commands. Supports verifying UI functionality, debugging behavior,
  capturing screenshots, and reading device logs.
  Adapted from Anthropic's webapp-testing skill for Android development.
---

# Android Application Testing

Test Android applications using instrumented tests, ADB, and UI automation frameworks.

## When This Skill Applies

Activate when:
- Testing Android UI functionality
- Debugging app behavior on device/emulator
- Capturing screenshots for verification
- Reading device logs (logcat)
- Writing instrumented or UI tests

---

## Decision Tree: Choosing Your Approach

```
User task → What type of testing?
    ├─ Unit tests (no Android dependencies)
    │   └─ Write JUnit tests in src/test/
    │
    ├─ Integration tests (with Android APIs)
    │   └─ Write instrumented tests in src/androidTest/
    │
    ├─ UI testing
    │   ├─ Single screen/component → Use Compose Testing
    │   ├─ User flows → Use Espresso or UI Automator
    │   └─ Screenshot verification → Use Screenshot Testing
    │
    └─ Manual verification
        ├─ Check device logs → adb logcat
        ├─ Take screenshot → adb screencap
        └─ Record screen → adb screenrecord
```

---

## ADB Commands for Debugging

### Device Connection

```bash
# List connected devices
adb devices

# Connect to wireless debugging
adb pair <ip>:<port>
adb connect <ip>:<port>
```

### Logs and Debugging

```bash
# View logs filtered by tag
adb logcat -s "MyAppTag"

# View logs filtered by package
adb logcat --pid=$(adb shell pidof -s com.example.myapp)

# Clear existing logs
adb logcat -c

# Export logs to file
adb logcat -d > logs.txt

# View crash logs
adb logcat "*:E" | grep -i "fatal\|crash\|exception"
```

### Screenshots and Recording

```bash
# Capture screenshot
adb shell screencap /sdcard/screenshot.png
adb pull /sdcard/screenshot.png ./screenshot.png

# Record screen (max 3 minutes)
adb shell screenrecord /sdcard/recording.mp4
adb pull /sdcard/recording.mp4 ./recording.mp4

# Record with size limit
adb shell screenrecord --size 720x1280 /sdcard/recording.mp4
```

### App Management

```bash
# Install app
adb install -r app-debug.apk

# Uninstall app
adb uninstall com.example.myapp

# Clear app data
adb shell pm clear com.example.myapp

# Force stop app
adb shell am force-stop com.example.myapp

# Start activity
adb shell am start -n com.example.myapp/.MainActivity
```

---

## Compose UI Testing

### Setup

```kotlin
// build.gradle.kts (app module)
androidTestImplementation("androidx.compose.ui:ui-test-junit4:1.x.x")
debugImplementation("androidx.compose.ui:ui-test-manifest:1.x.x")
```

### Basic Test Pattern

```kotlin
@RunWith(AndroidJUnit4::class)
class MyScreenTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun myScreen_displaysCorrectContent() {
        composeTestRule.setContent {
            MyTheme {
                MyScreen()
            }
        }

        // Find elements
        composeTestRule.onNodeWithText("Welcome")
            .assertIsDisplayed()

        // Interact with elements
        composeTestRule.onNodeWithContentDescription("Submit")
            .performClick()

        // Verify results
        composeTestRule.onNodeWithText("Success")
            .assertExists()
    }
}
```

### Common Matchers

```kotlin
// By text
onNodeWithText("Hello")
onNodeWithText("Hello", substring = true)
onNodeWithText("Hello", ignoreCase = true)

// By content description (accessibility)
onNodeWithContentDescription("Close button")

// By test tag
onNodeWithTag("my_button")

// By semantic role
onNode(hasRole(Role.Button))

// Multiple nodes
onAllNodesWithTag("list_item")
```

### Common Actions

```kotlin
// Click
performClick()

// Text input
performTextInput("Hello")
performTextClearance()
performTextReplacement("New text")

// Scroll
performScrollTo()
performScrollToIndex(5)

// Gestures
performTouchInput {
    swipeUp()
    swipeLeft()
    longClick()
}
```

### Common Assertions

```kotlin
assertIsDisplayed()
assertIsNotDisplayed()
assertExists()
assertDoesNotExist()
assertIsEnabled()
assertIsNotEnabled()
assertIsSelected()
assertTextEquals("Expected")
assertTextContains("partial")
```

---

## Espresso Testing

### Basic Pattern

```kotlin
@RunWith(AndroidJUnit4::class)
class MainActivityTest {

    @get:Rule
    val activityRule = ActivityScenarioRule(MainActivity::class.java)

    @Test
    fun clickButton_showsMessage() {
        // Find and click button
        onView(withId(R.id.myButton))
            .perform(click())

        // Verify result
        onView(withText("Hello!"))
            .check(matches(isDisplayed()))
    }
}
```

---

## Screenshot Testing

### Setup with Roborazzi

```kotlin
// build.gradle.kts
testImplementation("io.github.takahirom.roborazzi:roborazzi:1.x.x")
```

### Capture Screenshots

```kotlin
@RunWith(RobolectricTestRunner::class)
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class ScreenshotTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun myScreen_matchesSnapshot() {
        composeTestRule.setContent {
            MyTheme {
                MyScreen()
            }
        }

        composeTestRule.onRoot()
            .captureRoboImage("screenshots/my_screen.png")
    }
}
```

---

## Best Practices

### Test Organization

```
src/
├── test/                          # Unit tests (JVM)
│   └── kotlin/
│       └── com/example/
│           └── MyViewModelTest.kt
│
└── androidTest/                   # Instrumented tests (device)
    └── kotlin/
        └── com/example/
            ├── ui/                # UI tests
            │   └── MyScreenTest.kt
            └── integration/       # Integration tests
                └── DatabaseTest.kt
```

### Tips

- Use `testTag` modifier for reliable element selection
- Wait for async operations with `waitUntil { }`
- Use `printToLog()` to debug test trees
- Keep tests focused and independent
- Use test fixtures for common setup

---

## Keywords

android testing, compose testing, espresso, ui automator, adb, instrumented tests, screenshot testing, logcat, debugging
