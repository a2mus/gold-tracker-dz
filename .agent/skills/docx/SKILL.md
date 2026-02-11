---
name: docx
description: |
  Comprehensive document creation, editing, and analysis with support for tracked
  changes, comments, formatting preservation, and text extraction. Use when working
  with professional documents (.docx files) for creating, modifying, or analyzing content.
---

# DOCX Creation, Editing, and Analysis

## Overview

Work with .docx files for creating, editing, or analyzing content. A .docx file is
essentially a ZIP archive containing XML files that can be read or edited directly.

---

## Workflow Decision Tree

```
Task type?
├─ Reading/Analyzing → Use text extraction (pandoc)
├─ Creating new → Use python-docx or pandoc
└─ Editing existing
    ├─ Simple changes → Basic OOXML editing
    └─ Tracked changes needed → Redlining workflow
```

---

## Reading and Analyzing

### Text Extraction

Convert document to markdown using pandoc:

```bash
pandoc -f docx -t markdown document.docx -o document.md
```

### Raw XML Access

For accessing comments, tracked changes, or complex formatting:

```bash
# Unzip the docx
unzip document.docx -d document_extracted/

# Key files:
# - word/document.xml (main content)
# - word/comments.xml (comments)
# - word/styles.xml (styles)
```

---

## Creating Documents

### Using python-docx

```python
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Create document
doc = Document()

# Add heading
doc.add_heading('Document Title', 0)

# Add paragraph
para = doc.add_paragraph('This is a paragraph.')
para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

# Add formatted text
run = para.add_run(' Bold text.')
run.bold = True

# Add table
table = doc.add_table(rows=2, cols=2)
table.cell(0, 0).text = 'Header 1'
table.cell(0, 1).text = 'Header 2'

# Save
doc.save('output.docx')
```

### Using pandoc (from markdown)

```bash
pandoc input.md -o output.docx
```

---

## Editing Documents

### Basic Editing with python-docx

```python
from docx import Document

doc = Document('existing.docx')

# Find and replace text
for para in doc.paragraphs:
    if 'old text' in para.text:
        para.text = para.text.replace('old text', 'new text')

doc.save('modified.docx')
```

### Preserving Formatting

When editing, preserve original formatting:

```python
from docx import Document

doc = Document('template.docx')

# Access runs to preserve formatting
for para in doc.paragraphs:
    for run in para.runs:
        if 'placeholder' in run.text:
            run.text = run.text.replace('placeholder', 'actual value')
            # Formatting is preserved

doc.save('filled.docx')
```

---

## Converting to Images

For visual analysis, convert documents to images:

```bash
# Step 1: Convert to PDF
soffice --headless --convert-to pdf document.docx

# Step 2: Convert PDF pages to JPEG
pdftoppm -jpeg -r 150 document.pdf page
# Creates page-1.jpg, page-2.jpg, etc.
```

Options:
- `-r 150`: Resolution (DPI)
- `-f N`: First page
- `-l N`: Last page

---

## Dependencies

Required tools:

| Tool | Install | Purpose |
|------|---------|---------|
| pandoc | `apt install pandoc` | Text extraction, conversion |
| python-docx | `pip install python-docx` | Python document manipulation |
| LibreOffice | `apt install libreoffice` | PDF conversion |
| Poppler | `apt install poppler-utils` | PDF to image conversion |

---

## Code Style Guidelines

When generating code for DOCX operations:
- Write concise code
- Avoid verbose variable names
- Avoid unnecessary print statements

---

## Keywords

docx, word document, document creation, document editing, text extraction, pandoc, python-docx
