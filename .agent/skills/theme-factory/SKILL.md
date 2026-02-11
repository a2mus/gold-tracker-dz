---
name: theme-factory
description: |
  Toolkit for creating and applying themes to Android applications and artifacts.
  Provides pre-set themes with color palettes and typography that can be applied
  to Jetpack Compose apps, documents, presentations, and other artifacts.
  Adapted from Anthropic's theme-factory skill for Android development.
---

# Theme Factory Skill

Create and apply professional themes with curated color palettes and font pairings.
Each theme includes colors optimized for Material 3 and complementary typography.

## When This Skill Applies

Activate when:
- Creating new Android app themes
- Applying consistent styling across screens
- Generating color schemes for Material 3
- Styling documents or presentations
- Discussing visual identity for applications

---

## Available Themes

### 1. Ocean Depths
Professional and calming maritime theme

```kotlin
val oceanDepthsLight = lightColorScheme(
    primary = Color(0xFF1565C0),
    onPrimary = Color.White,
    secondary = Color(0xFF00ACC1),
    tertiary = Color(0xFF26A69A),
    background = Color(0xFFF5F9FC),
    surface = Color.White
)

val oceanDepthsDark = darkColorScheme(
    primary = Color(0xFF64B5F6),
    onPrimary = Color(0xFF0D47A1),
    secondary = Color(0xFF4DD0E1),
    tertiary = Color(0xFF80CBC4),
    background = Color(0xFF0D1B2A),
    surface = Color(0xFF1B2838)
)
```
**Typography**: Poppins (headings) + Inter (body)

---

### 2. Sunset Boulevard
Warm and vibrant sunset colors

```kotlin
val sunsetLight = lightColorScheme(
    primary = Color(0xFFE65100),
    onPrimary = Color.White,
    secondary = Color(0xFFFF8F00),
    tertiary = Color(0xFFFFC107),
    background = Color(0xFFFFFBF5),
    surface = Color.White
)
```
**Typography**: Montserrat (headings) + Lora (body)

---

### 3. Forest Canopy
Natural and grounded earth tones

```kotlin
val forestLight = lightColorScheme(
    primary = Color(0xFF2E7D32),
    secondary = Color(0xFF558B2F),
    tertiary = Color(0xFF8D6E63),
    background = Color(0xFFF5F7F5),
    surface = Color.White
)
```
**Typography**: Merriweather (headings) + Source Sans Pro (body)

---

### 4. Modern Minimalist
Clean and contemporary grayscale

```kotlin
val minimalistLight = lightColorScheme(
    primary = Color(0xFF212121),
    secondary = Color(0xFF616161),
    tertiary = Color(0xFF9E9E9E),
    background = Color(0xFFFAFAFA),
    surface = Color.White
)
```
**Typography**: Roboto Mono (headings) + Roboto (body)

---

### 5. Golden Hour
Rich and warm autumnal palette

```kotlin
val goldenHourLight = lightColorScheme(
    primary = Color(0xFFD4A574),
    secondary = Color(0xFFC4956A),
    tertiary = Color(0xFF8B6B4E),
    background = Color(0xFFFDF8F3),
    surface = Color.White
)
```
**Typography**: Playfair Display (headings) + Libre Baskerville (body)

---

### 6. Arctic Frost
Cool and crisp winter-inspired theme

```kotlin
val arcticFrostLight = lightColorScheme(
    primary = Color(0xFF546E7A),
    secondary = Color(0xFF78909C),
    tertiary = Color(0xFF90A4AE),
    background = Color(0xFFF5F7FA),
    surface = Color.White
)
```
**Typography**: Nunito (headings) + Open Sans (body)

---

### 7. Desert Rose
Soft and sophisticated dusty tones

```kotlin
val desertRoseLight = lightColorScheme(
    primary = Color(0xFFB76E79),
    secondary = Color(0xFFD4A5A5),
    tertiary = Color(0xFFE8C4C4),
    background = Color(0xFFFDF5F5),
    surface = Color.White
)
```
**Typography**: Cormorant Garamond (headings) + Raleway (body)

---

### 8. Tech Innovation
Bold and modern tech aesthetic

```kotlin
val techInnovationLight = lightColorScheme(
    primary = Color(0xFF6200EE),
    secondary = Color(0xFF03DAC5),
    tertiary = Color(0xFFFF0266),
    background = Color(0xFFF5F5F7),
    surface = Color.White
)
```
**Typography**: Space Grotesk (headings) + DM Sans (body)

---

### 9. Botanical Garden
Fresh and organic garden colors

```kotlin
val botanicalLight = lightColorScheme(
    primary = Color(0xFF4CAF50),
    secondary = Color(0xFF81C784),
    tertiary = Color(0xFFA5D6A7),
    background = Color(0xFFF1F8E9),
    surface = Color.White
)
```
**Typography**: Josefin Sans (headings) + Cabin (body)

---

### 10. Midnight Galaxy
Dramatic and cosmic deep tones

```kotlin
val galaxyDark = darkColorScheme(
    primary = Color(0xFF7C4DFF),
    secondary = Color(0xFFB388FF),
    tertiary = Color(0xFFFF80AB),
    background = Color(0xFF0A0A1A),
    surface = Color(0xFF1A1A2E)
)
```
**Typography**: Orbitron (headings) + Exo 2 (body)

---

## Usage Instructions

### Applying a Theme

1. **Choose a theme** from the list above
2. **Copy the color scheme** to your `Theme.kt`
3. **Add the typography** using Google Fonts dependency:

```kotlin
// build.gradle.kts
implementation("androidx.compose.ui:ui-text-google-fonts:1.x.x")

// Type.kt
val provider = GoogleFont.Provider(
    providerAuthority = "com.google.android.gms.fonts",
    providerPackage = "com.google.android.gms",
    certificates = R.array.com_google_android_gms_fonts_certs
)

val headingFont = GoogleFont("Poppins")
val bodyFont = GoogleFont("Inter")

val AppTypography = Typography(
    displayLarge = TextStyle(
        fontFamily = FontFamily(Font(headingFont, provider)),
        fontWeight = FontWeight.Bold,
        fontSize = 57.sp
    ),
    bodyLarge = TextStyle(
        fontFamily = FontFamily(Font(bodyFont, provider)),
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp
    )
)
```

4. **Apply in your app**:

```kotlin
@Composable
fun AppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = if (darkTheme) themeDarkColors else themeLightColors,
        typography = AppTypography,
        content = content
    )
}
```

---

## Create Custom Theme

When existing themes don't fit, create a custom theme:

1. **Define the mood**: What emotion should the app convey?
2. **Choose primary color**: The most prominent color
3. **Select complementary colors**: Secondary and tertiary
4. **Pick typography**: Heading + body font pairing
5. **Create both light and dark variants**
6. **Test with actual components**

### Custom Theme Template

```kotlin
val customThemeName = "Your Theme Name"

val customLight = lightColorScheme(
    primary = Color(0xFF______),
    onPrimary = Color(0xFF______),
    primaryContainer = Color(0xFF______),
    onPrimaryContainer = Color(0xFF______),
    secondary = Color(0xFF______),
    // ... complete the scheme
)

val customDark = darkColorScheme(
    // ... dark variant
)
```

---

## Keywords

material 3, color scheme, typography, theming, design system, color palette, fonts, visual identity, android theme
