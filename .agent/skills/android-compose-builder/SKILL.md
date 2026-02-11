---
name: android-compose-builder
description: |
  Toolkit for building production-ready Android Compose UI components and screens.
  Use for complex Android UI requiring state management, navigation, custom components,
  or complete screen implementations. Generates clean, reusable Kotlin/Compose code.
  Adapted from Anthropic's web-artifacts-builder skill for Android development.
---

# Android Compose Builder

Build production-ready Jetpack Compose UI components and screens with modern patterns.

## When This Skill Applies

Activate when:
- Building complex Compose screens
- Creating reusable UI components
- Implementing state management patterns
- Setting up navigation
- Creating design system components

---

## Standard Project Structure

```
app/src/main/kotlin/com/example/app/
├── ui/
│   ├── components/           # Reusable UI components
│   │   ├── buttons/
│   │   ├── cards/
│   │   ├── inputs/
│   │   └── dialogs/
│   ├── screens/              # Screen-level composables
│   │   ├── home/
│   │   ├── detail/
│   │   └── settings/
│   └── theme/                # Theming
│       ├── Theme.kt
│       ├── Color.kt
│       ├── Type.kt
│       └── Shape.kt
├── navigation/               # Navigation setup
│   └── AppNavGraph.kt
├── viewmodel/                # ViewModels
└── data/                     # Data layer
```

---

## Component Patterns

### Basic Component

```kotlin
@Composable
fun PrimaryButton(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    isLoading: Boolean = false
) {
    Button(
        onClick = onClick,
        modifier = modifier.height(48.dp),
        enabled = enabled && !isLoading,
        shape = MaterialTheme.shapes.medium
    ) {
        if (isLoading) {
            CircularProgressIndicator(
                modifier = Modifier.size(20.dp),
                strokeWidth = 2.dp,
                color = MaterialTheme.colorScheme.onPrimary
            )
        } else {
            Text(text = text)
        }
    }
}
```

### Stateful Component

```kotlin
@Composable
fun SearchBar(
    query: String,
    onQueryChange: (String) -> Unit,
    onSearch: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    var isActive by remember { mutableStateOf(false) }
    
    OutlinedTextField(
        value = query,
        onValueChange = onQueryChange,
        modifier = modifier.fillMaxWidth(),
        placeholder = { Text("Search...") },
        leadingIcon = {
            Icon(Icons.Default.Search, contentDescription = null)
        },
        trailingIcon = {
            if (query.isNotEmpty()) {
                IconButton(onClick = { onQueryChange("") }) {
                    Icon(Icons.Default.Clear, contentDescription = "Clear")
                }
            }
        },
        keyboardActions = KeyboardActions(
            onSearch = { onSearch(query) }
        ),
        singleLine = true
    )
}
```

---

## Screen Patterns

### Screen with ViewModel

```kotlin
@Composable
fun HomeScreen(
    viewModel: HomeViewModel = hiltViewModel(),
    onNavigateToDetail: (String) -> Unit
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    
    HomeScreenContent(
        uiState = uiState,
        onRefresh = viewModel::refresh,
        onItemClick = onNavigateToDetail,
        onFavoriteToggle = viewModel::toggleFavorite
    )
}

@Composable
private fun HomeScreenContent(
    uiState: HomeUiState,
    onRefresh: () -> Unit,
    onItemClick: (String) -> Unit,
    onFavoriteToggle: (String) -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(title = { Text("Home") })
        }
    ) { padding ->
        when {
            uiState.isLoading -> {
                LoadingIndicator(Modifier.padding(padding))
            }
            uiState.error != null -> {
                ErrorState(
                    message = uiState.error,
                    onRetry = onRefresh,
                    modifier = Modifier.padding(padding)
                )
            }
            uiState.items.isEmpty() -> {
                EmptyState(
                    message = "No items found",
                    modifier = Modifier.padding(padding)
                )
            }
            else -> {
                ItemList(
                    items = uiState.items,
                    onItemClick = onItemClick,
                    onFavoriteToggle = onFavoriteToggle,
                    modifier = Modifier.padding(padding)
                )
            }
        }
    }
}
```

### UI State Pattern

```kotlin
data class HomeUiState(
    val items: List<Item> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null,
    val isRefreshing: Boolean = false
)

@HiltViewModel
class HomeViewModel @Inject constructor(
    private val repository: ItemRepository
) : ViewModel() {
    
    private val _uiState = MutableStateFlow(HomeUiState())
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()
    
    init {
        loadItems()
    }
    
    fun refresh() {
        _uiState.update { it.copy(isRefreshing = true) }
        loadItems()
    }
    
    private fun loadItems() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            
            repository.getItems()
                .onSuccess { items ->
                    _uiState.update { 
                        it.copy(items = items, isLoading = false, isRefreshing = false) 
                    }
                }
                .onFailure { e ->
                    _uiState.update { 
                        it.copy(error = e.message, isLoading = false, isRefreshing = false) 
                    }
                }
        }
    }
    
    fun toggleFavorite(itemId: String) {
        viewModelScope.launch {
            repository.toggleFavorite(itemId)
        }
    }
}
```

---

## Navigation Setup

```kotlin
@Composable
fun AppNavGraph(
    navController: NavHostController = rememberNavController()
) {
    NavHost(
        navController = navController,
        startDestination = Route.Home
    ) {
        composable<Route.Home> {
            HomeScreen(
                onNavigateToDetail = { id ->
                    navController.navigate(Route.Detail(id))
                }
            )
        }
        
        composable<Route.Detail> { backStackEntry ->
            val route: Route.Detail = backStackEntry.toRoute()
            DetailScreen(
                itemId = route.id,
                onNavigateBack = { navController.popBackStack() }
            )
        }
    }
}

@Serializable
sealed class Route {
    @Serializable
    data object Home : Route()
    
    @Serializable
    data class Detail(val id: String) : Route()
}
```

---

## Common Components Library

### Loading Indicator

```kotlin
@Composable
fun LoadingIndicator(
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        CircularProgressIndicator()
    }
}
```

### Error State

```kotlin
@Composable
fun ErrorState(
    message: String,
    onRetry: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Icon(
            imageVector = Icons.Default.Warning,
            contentDescription = null,
            modifier = Modifier.size(48.dp),
            tint = MaterialTheme.colorScheme.error
        )
        Spacer(modifier = Modifier.height(16.dp))
        Text(
            text = message,
            style = MaterialTheme.typography.bodyLarge,
            textAlign = TextAlign.Center
        )
        Spacer(modifier = Modifier.height(16.dp))
        Button(onClick = onRetry) {
            Text("Retry")
        }
    }
}
```

### Empty State

```kotlin
@Composable
fun EmptyState(
    message: String,
    modifier: Modifier = Modifier,
    icon: ImageVector = Icons.Default.Inbox
) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            modifier = Modifier.size(64.dp),
            tint = MaterialTheme.colorScheme.outline
        )
        Spacer(modifier = Modifier.height(16.dp))
        Text(
            text = message,
            style = MaterialTheme.typography.bodyLarge,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}
```

---

## Design Guidelines

### AVOID "AI Slop"

❌ Don't use:
- Excessive centered layouts
- Purple gradients everywhere
- Uniform rounded corners on everything
- Default Material components without customization

✅ Do use:
- Intentional asymmetry
- Contextual color choices
- Varied corner radii
- Custom component implementations

---

## Best Practices

1. **Separate stateful and stateless composables**
2. **Use preview annotations for all components**
3. **Extract reusable components early**
4. **Use semantic modifiers (clickable, selectable)**
5. **Handle all UI states (loading, error, empty, success)**
6. **Use collectAsStateWithLifecycle for flows**

---

## Keywords

jetpack compose, android ui, components, screens, viewmodel, navigation, state management, mvvm, material design
