---
name: pptx
description: |
  Presentation creation, editing, and analysis. Use when working with presentations
  (.pptx files) for creating, modifying content, working with layouts, or adding
  speaker notes.
---

# PPTX Creation, Editing, and Analysis

## Overview

Work with .pptx files for creating, editing, or analyzing presentations. A .pptx file
is essentially a ZIP archive containing XML files that can be read or edited.

---

## Workflow Decision Tree

```
Task type?
├─ Reading/Analyzing → Use text extraction (markitdown)
├─ Creating new → Use python-pptx or html2pptx
└─ Editing existing
    ├─ Text changes → python-pptx
    └─ Layout/Design → HTML to PPTX workflow
```

---

## Reading and Analyzing

### Text Extraction

```bash
python -m markitdown path-to-file.pptx
```

### Raw XML Access

For accessing speaker notes, animations, or complex formatting:

```bash
# Unzip the pptx
unzip presentation.pptx -d presentation_extracted/

# Key files:
# - ppt/slides/slide1.xml (slide content)
# - ppt/notesSlides/notesSlide1.xml (speaker notes)
# - ppt/slideMasters/ (master layouts)
```

---

## Creating Presentations

### Using python-pptx

```python
from pptx import Presentation
from pptx.util import Inches, Pt

# Create presentation
prs = Presentation()

# Add title slide
title_slide_layout = prs.slide_layouts[0]
slide = prs.slides.add_slide(title_slide_layout)
title = slide.shapes.title
subtitle = slide.placeholders[1]

title.text = "Presentation Title"
subtitle.text = "Subtitle text"

# Add content slide
bullet_slide_layout = prs.slide_layouts[1]
slide = prs.slides.add_slide(bullet_slide_layout)
shapes = slide.shapes

title_shape = shapes.title
body_shape = shapes.placeholders[1]

title_shape.text = "Slide Title"
tf = body_shape.text_frame
tf.text = "First bullet point"

p = tf.add_paragraph()
p.text = "Second bullet point"
p.level = 1

# Save
prs.save("output.pptx")
```

### Adding Images

```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

# Add image
slide.shapes.add_picture(
    "image.png",
    left=Inches(1),
    top=Inches(1),
    width=Inches(5)
)

prs.save("output.pptx")
```

### Adding Tables

```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[6])

# Add table
table = slide.shapes.add_table(
    rows=3, cols=3,
    left=Inches(1), top=Inches(2),
    width=Inches(8), height=Inches(2)
).table

# Fill cells
table.cell(0, 0).text = "Header 1"
table.cell(0, 1).text = "Header 2"
table.cell(0, 2).text = "Header 3"

prs.save("output.pptx")
```

---

## Editing Presentations

### Modify Existing Slides

```python
from pptx import Presentation

prs = Presentation("existing.pptx")

for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame:
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    if "placeholder" in run.text:
                        run.text = run.text.replace("placeholder", "value")

prs.save("modified.pptx")
```

### Add Speaker Notes

```python
from pptx import Presentation

prs = Presentation("presentation.pptx")

for slide in prs.slides:
    notes_slide = slide.notes_slide
    notes_slide.notes_text_frame.text = "Speaker notes for this slide"

prs.save("with_notes.pptx")
```

---

## Converting to Images

For visual analysis:

```bash
# Step 1: Convert to PDF
soffice --headless --convert-to pdf presentation.pptx

# Step 2: Convert PDF pages to JPEG
pdftoppm -jpeg -r 150 presentation.pdf slide
# Creates slide-1.jpg, slide-2.jpg, etc.
```

---

## Slide Layouts

Standard layouts in default template:

| Index | Layout Name | Use Case |
|-------|-------------|----------|
| 0 | Title Slide | Opening slides |
| 1 | Title and Content | Standard content |
| 2 | Section Header | Section breaks |
| 3 | Two Content | Side-by-side |
| 4 | Comparison | Before/after |
| 5 | Title Only | Custom layout base |
| 6 | Blank | Full custom |

---

## Dependencies

| Tool | Install | Purpose |
|------|---------|---------|
| python-pptx | `pip install python-pptx` | Create/edit presentations |
| markitdown | `pip install markitdown[pptx]` | Text extraction |
| LibreOffice | `apt install libreoffice` | PDF conversion |
| Poppler | `apt install poppler-utils` | PDF to image |

---

## Code Style Guidelines

When generating code for PPTX operations:
- Write concise code
- Avoid verbose variable names
- Avoid unnecessary print statements

---

## Keywords

pptx, powerpoint, presentation, slides, python-pptx, speaker notes, slide layouts
