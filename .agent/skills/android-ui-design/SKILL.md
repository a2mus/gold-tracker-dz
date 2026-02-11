---
name: android-ui-design
description: |
  Create distinctive, production-grade Android UI interfaces with high design quality.
  Use this skill when building Jetpack Compose screens, Material Design components,
  custom views, or styling Android applications. Generates creative, polished Kotlin/Compose
  code and UI design that avoids generic aesthetics.
  Adapted from Anthropic's frontend-design skill for Android development.
---

# Android UI Design Skill

Create distinctive, production-grade Android interfaces that avoid generic "AI slop" aesthetics.
Implement real working Kotlin code with exceptional attention to aesthetic details and creative choices.

## When This Skill Applies

Activate when:
- Building Jetpack Compose screens or components
- Creating custom Material Design implementations
- Styling or beautifying Android UI
- Designing dashboards, forms, or complex layouts
- Building custom views or animations

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme:
  - Brutally minimal
  - Material maximalism
  - Retro-futuristic
  - Organic/natural
  - Luxury/refined
  - Playful/toy-like
  - Editorial/magazine
  - Brutalist/raw
  - Art deco/geometric
  - Soft/pastel
  - Industrial/utilitarian
- **Constraints**: Performance, accessibility, RTL support, device compatibility
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute with precision. Bold maximalism and refined minimalism both work - the key is intentionality.

---

## Android Aesthetics Guidelines

### Typography

```kotlin
// Use distinctive typography - NOT system defaults
val AppTypography = Typography(
    displayLarge = TextStyle(
        fontFamily = FontFamily(Font(R.font.distinctive_display)),
        fontWeight = FontWeight.Bold,
        fontSize = 57.sp,
        letterSpacing = (-0.25).sp
    ),
    bodyLarge = TextStyle(
        fontFamily = FontFamily(Font(R.font.refined_body)),
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        letterSpacing = 0.5.sp,
        lineHeight = 24.sp
    )
)
```

**Avoid**: Default Roboto everywhere. Choose distinctive, characterful font choices.
**Prefer**: Pair a distinctive display font with a refined body font.

### Color & Theme

```kotlin
// Create cohesive color schemes - NOT generic Material palettes
private val LightColors = lightColorScheme(
    primary = Color(0xFF1A365D),      // Deep navy
    onPrimary = Color(0xFFF7FAFC),
    secondary = Color(0xFFD97706),    // Warm amber
    surface = Color(0xFFFAFAF9),
    background = Color(0xFFF5F5F4),
    // ... carefully curated palette
)

private val DarkColors = darkColorScheme(
    primary = Color(0xFF90CDF4),      // Soft sky blue
    onPrimary = Color(0xFF1A365D),
    secondary = Color(0xFFFBBF24),    // Golden accent
    surface = Color(0xFF1A1A2E),
    background = Color(0xFF16213E),
    // ... atmospheric dark palette
)
```

**Avoid**: Generic Material palettes (especially purple gradients)
**Prefer**: Dominant colors with sharp accents; cohesive, intentional schemes

### Motion & Animation

```kotlin
// Create high-impact animations
val enterTransition = fadeIn(
    animationSpec = tween(300, easing = EaseOutCubic)
) + slideInVertically(
    initialOffsetY = { it / 4 },
    animationSpec = tween(400, easing = EaseOutQuart)
)

// Micro-interactions that surprise
val scale by animateFloatAsState(
    targetValue = if (pressed) 0.95f else 1f,
    animationSpec = spring(dampingRatio = 0.6f, stiffness = 400f)
)
```

**Prioritize**: One well-orchestrated screen transition over scattered micro-interactions.
**Use**: Staggered reveals, scroll-triggered animations, surprising touch feedback.

### Spatial Composition

```kotlin
// Break the grid intentionally
Box(modifier = Modifier.fillMaxSize()) {
    // Asymmetric layout
    Column(
        modifier = Modifier
            .align(Alignment.CenterStart)
            .offset(x = (-24).dp)  // Intentional bleed
    ) {
        // Content that breaks boundaries
    }
    
    // Overlapping elements
    Box(
        modifier = Modifier
            .align(Alignment.TopEnd)
            .offset(y = 80.dp, x = 16.dp)
            .zIndex(2f)
    ) {
        // Floating accent element
    }
}
```

**Consider**: Unexpected layouts, asymmetry, overlap, diagonal flow, grid-breaking elements.

### Backgrounds & Visual Details

```kotlin
// Create atmosphere and depth
Box(
    modifier = Modifier
        .fillMaxSize()
        .background(
            Brush.radialGradient(
                colors = listOf(
                    Color(0xFF2D3748),
                    Color(0xFF1A202C)
                ),
                center = Offset(0.3f, 0.1f),
                radius = 1000f
            )
        )
        .drawBehind {
            // Noise texture overlay
            // Geometric patterns
            // Layered transparencies
        }
)
```

**Apply**: Gradient meshes, noise textures, geometric patterns, dramatic shadows, grain overlays.

---

## NEVER Use Generic AI Aesthetics

❌ **Avoid**:
- Default Roboto font everywhere
- Purple gradients on white backgrounds  
- Cookie-cutter Material components without customization
- Predictable layouts (centered cards, equal spacing)
- Generic color schemes

✅ **Instead**:
- Make unexpected choices that feel genuinely designed
- Vary between light and dark themes
- Use different fonts, different aesthetics
- Context-specific character

---

## Implementation Pattern

```kotlin
@Composable
fun DistinctiveScreen() {
    // 1. Establish the aesthetic context
    val aestheticDirection = rememberAestheticDirection()
    
    // 2. Apply distinctive theming
    CompositionLocalProvider(
        LocalRippleTheme provides DistinctiveRippleTheme,
        LocalContentColor provides aestheticDirection.contentColor
    ) {
        // 3. Build with intentional composition
        Box(
            modifier = Modifier
                .fillMaxSize()
                .atmosphericBackground(aestheticDirection)
        ) {
            // 4. Every element reinforces the aesthetic
            AnimatedContent(targetState = screenState) { state ->
                when (state) {
                    // Screens with distinctive transitions
                }
            }
        }
    }
}
```

---

## Complexity Matching

**IMPORTANT**: Match implementation complexity to the aesthetic vision:

| Vision | Implementation |
|--------|----------------|
| Maximalist | Elaborate code, extensive animations, rich effects |
| Minimalist | Restraint, precision, careful spacing/typography |
| Refined | Subtle details, polish, attention to micro-interactions |

Elegance comes from executing the vision well.

---

## Remember

Claude is capable of extraordinary creative work. Don't hold back.
Show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

## Keywords

jetpack compose, material design, android ui, kotlin, animation, theming, custom components, mobile design, screens, composables
