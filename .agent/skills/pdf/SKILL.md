---
name: pdf
description: |
  Comprehensive PDF manipulation toolkit for extracting text and tables, creating
  new PDFs, merging/splitting documents, and handling forms. Use when working with
  PDF documents for processing, generation, or analysis.
---

# PDF Processing Guide

## Overview

Essential PDF processing operations using Python libraries and command-line tools.

---

## Quick Start

```python
from pypdf import PdfReader, PdfWriter

# Read a PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = ""
for page in reader.pages:
    text += page.extract_text()
```

---

## Common Operations

### Merge PDFs

```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

### Split PDF

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

### Extract Tables

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                print(row)
```

---

## Creating PDFs

### Using ReportLab

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("output.pdf", pagesize=letter)
c.drawString(100, 750, "Hello, World!")
c.save()
```

### From HTML

```bash
wkhtmltopdf input.html output.pdf
```

### From Markdown

```bash
pandoc input.md -o output.pdf
```

---

## PDF Manipulation

### Rotate Pages

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.rotate(90)  # Rotate 90 degrees clockwise
    writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

### Add Watermark

```python
from pypdf import PdfReader, PdfWriter

watermark = PdfReader("watermark.pdf").pages[0]
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

### Extract Images

```bash
# Using pdfimages (poppler-utils)
pdfimages -j input.pdf output_prefix
# Extracts as output_prefix-000.jpg, output_prefix-001.jpg, etc.
```

### Password Protection

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

writer.encrypt("userpassword", "ownerpassword")

with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

---

## Command Line Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `pdftk` | Merge, split, rotate | `pdftk *.pdf cat output merged.pdf` |
| `qpdf` | Merge, encrypt | `qpdf --empty --pages *.pdf -- output.pdf` |
| `pdftotext` | Extract text | `pdftotext input.pdf output.txt` |
| `pdfimages` | Extract images | `pdfimages -j input.pdf prefix` |

---

## Quick Reference

| Task | Best Tool | Command/Code |
|------|-----------|--------------|
| Merge PDFs | pypdf | `writer.add_page(page)` |
| Split PDFs | pypdf | One page per file |
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Create PDFs | reportlab | Canvas or Platypus |
| Command line merge | qpdf | `qpdf --empty --pages ...` |
| OCR scanned PDFs | pytesseract | Convert to image first |

---

## Dependencies

| Library | Install | Purpose |
|---------|---------|---------|
| pypdf | `pip install pypdf` | Read, write, merge PDFs |
| pdfplumber | `pip install pdfplumber` | Extract text and tables |
| reportlab | `pip install reportlab` | Create PDFs |
| poppler-utils | `apt install poppler-utils` | CLI tools |
| qpdf | `apt install qpdf` | PDF manipulation |

---

## Keywords

pdf, document processing, text extraction, table extraction, merge, split, reportlab, pypdf, pdfplumber
