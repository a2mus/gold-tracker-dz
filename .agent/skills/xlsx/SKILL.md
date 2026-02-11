---
name: xlsx
description: |
  Comprehensive spreadsheet creation, editing, and analysis with support for formulas,
  formatting, data analysis, and visualization. Use when working with spreadsheets
  (.xlsx, .xlsm, .csv, .tsv) for creating, reading, modifying, or analyzing data.
---

# Excel/Spreadsheet Processing Guide

## Requirements for Outputs

### Zero Formula Errors
Every Excel file MUST be delivered with ZERO formula errors:
- #REF!
- #DIV/0!
- #VALUE!
- #N/A
- #NAME?

### Preserve Existing Templates
When modifying files:
- Match existing format, style, and conventions
- Never impose standardized formatting on files with established patterns

---

## Quick Start

### Reading Files

```python
import pandas as pd

# Read Excel file
df = pd.read_excel("data.xlsx")

# Read specific sheet
df = pd.read_excel("data.xlsx", sheet_name="Sheet2")

# Read CSV
df = pd.read_csv("data.csv")

# Preview data
print(df.head())
print(df.info())
```

### Writing Files

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob"],
    "Value": [100, 200]
})

# Write to Excel
df.to_excel("output.xlsx", index=False)

# Write to CSV
df.to_csv("output.csv", index=False)
```

---

## Working with openpyxl

### Creating Formatted Spreadsheets

```python
from openpyxl import Workbook
from openpyxl.styles import Font, Fill, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active
ws.title = "Data"

# Headers with formatting
headers = ["Name", "Value", "Date"]
for col, header in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col, value=header)
    cell.font = Font(bold=True)
    cell.fill = PatternFill(start_color="4472C4", fill_type="solid")
    cell.font = Font(bold=True, color="FFFFFF")

# Add data
data = [
    ["Alice", 100, "2024-01-15"],
    ["Bob", 200, "2024-01-16"],
]
for row_idx, row_data in enumerate(data, 2):
    for col_idx, value in enumerate(row_data, 1):
        ws.cell(row=row_idx, column=col_idx, value=value)

# Auto-fit column widths
for col in range(1, len(headers) + 1):
    ws.column_dimensions[get_column_letter(col)].width = 15

wb.save("formatted.xlsx")
```

### Working with Formulas

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active

# Add data
ws["A1"] = "Item"
ws["B1"] = "Price"
ws["C1"] = "Quantity"
ws["D1"] = "Total"

ws["A2"] = "Widget"
ws["B2"] = 10.50
ws["C2"] = 5
ws["D2"] = "=B2*C2"  # Formula

ws["A3"] = "Gadget"
ws["B3"] = 25.00
ws["C3"] = 3
ws["D3"] = "=B3*C3"

# Sum formula
ws["D4"] = "=SUM(D2:D3)"

wb.save("with_formulas.xlsx")
```

### Reading and Preserving Formulas

```python
from openpyxl import load_workbook

# Load with formulas (not calculated values)
wb = load_workbook("input.xlsx")
ws = wb.active

# Modify while preserving formulas
ws["A1"] = "New Value"

# WARNING: Using data_only=True replaces formulas with values permanently
# Only use when you need calculated values and won't save

wb.save("output.xlsx")
```

---

## Data Analysis with Pandas

### Basic Analysis

```python
import pandas as pd

df = pd.read_excel("data.xlsx")

# Summary statistics
print(df.describe())

# Group by analysis
summary = df.groupby("Category").agg({
    "Value": ["sum", "mean", "count"]
})

# Pivot table
pivot = pd.pivot_table(
    df,
    values="Value",
    index="Category",
    columns="Month",
    aggfunc="sum"
)

# Export results
summary.to_excel("analysis.xlsx")
```

### Data Cleaning

```python
import pandas as pd

df = pd.read_excel("data.xlsx")

# Handle missing values
df = df.dropna()  # Remove rows with missing values
df = df.fillna(0)  # Fill missing with 0

# Remove duplicates
df = df.drop_duplicates()

# Convert types
df["Date"] = pd.to_datetime(df["Date"])
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

df.to_excel("cleaned.xlsx", index=False)
```

---

## Financial Model Color Standards

When creating financial models (unless specified otherwise):

| Color | RGB | Use |
|-------|-----|-----|
| Blue text | 0,0,255 | Hardcoded inputs |
| Black text | 0,0,0 | Formulas and calculations |
| Green text | 0,128,0 | Links from other worksheets |
| Red text | 255,0,0 | External links |
| Yellow background | 255,255,0 | Input cells |

---

## Common Operations

### Merge Multiple Files

```python
import pandas as pd
import glob

files = glob.glob("data/*.xlsx")
dfs = [pd.read_excel(f) for f in files]
combined = pd.concat(dfs, ignore_index=True)
combined.to_excel("combined.xlsx", index=False)
```

### Filter and Export

```python
import pandas as pd

df = pd.read_excel("data.xlsx")
filtered = df[df["Value"] > 100]
filtered.to_excel("filtered.xlsx", index=False)
```

### Add Charts

```python
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference

wb = Workbook()
ws = wb.active

# Add data
data = [
    ["Category", "Value"],
    ["A", 10],
    ["B", 20],
    ["C", 15],
]
for row in data:
    ws.append(row)

# Create chart
chart = BarChart()
chart.title = "Sample Chart"
data_ref = Reference(ws, min_col=2, min_row=1, max_row=4)
cats_ref = Reference(ws, min_col=1, min_row=2, max_row=4)
chart.add_data(data_ref, titles_from_data=True)
chart.set_categories(cats_ref)

ws.add_chart(chart, "D2")
wb.save("with_chart.xlsx")
```

---

## Dependencies

| Library | Install | Purpose |
|---------|---------|---------|
| pandas | `pip install pandas` | Data analysis |
| openpyxl | `pip install openpyxl` | Excel manipulation |
| xlrd | `pip install xlrd` | Read old .xls files |

---

## Best Practices

- **pandas**: Best for data analysis and bulk operations
- **openpyxl**: Best for complex formatting and Excel-specific features
- Cell indices are 1-based in openpyxl (row=1, column=1 = A1)
- For large files: Use `read_only=True` or `write_only=True`

---

## Keywords

xlsx, excel, spreadsheet, pandas, openpyxl, csv, data analysis, formulas, charts
