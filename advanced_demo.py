"""
PyMuPDF Advanced Demo
=====================
Demonstrates complex usages of PyMuPDF including:
  1. Multi-page PDF with rich text formatting
  2. Drawing shapes & vector graphics
  3. Table creation & extraction
  4. Image generation, insertion & extraction
  5. Watermarking
  6. Annotations (highlights, comments, stamps)
  7. PDF merging
  8. Text search & redaction
  9. PDF encryption & decryption
 10. Page-to-image rendering (Pixmap)
"""

import pymupdf
import os
import json

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo_output")


def ensure_output_dir():
    """Create output directory if it doesn't exist."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}\n")


# ─────────────────────────────────────────────────────────────
# 1. MULTI-PAGE PDF WITH RICH TEXT
# ─────────────────────────────────────────────────────────────
def demo_rich_text_pdf():
    """Create a multi-page PDF with various fonts, sizes, and colors."""
    print("=" * 60)
    print("DEMO 1: Multi-Page PDF with Rich Text")
    print("=" * 60)

    doc = pymupdf.open()

    # --- Page 1: Title page ---
    page = doc.new_page(width=595, height=842)  # A4

    # Large title
    page.insert_text(
        (50, 100),
        "PyMuPDF Advanced Demo",
        fontsize=36,
        fontname="helv",
        color=(0.1, 0.2, 0.6),
    )

    # Subtitle
    page.insert_text(
        (50, 150),
        "A comprehensive showcase of PDF manipulation capabilities",
        fontsize=14,
        fontname="hebo",  # Helvetica Bold Oblique
        color=(0.4, 0.4, 0.4),
    )

    # Decorative line
    shape = page.new_shape()
    shape.draw_line((50, 170), (545, 170))
    shape.finish(color=(0.1, 0.2, 0.6), width=2)
    shape.commit()

    # Table of contents
    toc_items = [
        "1. Multi-Page PDF with Rich Text",
        "2. Drawing Shapes & Vector Graphics",
        "3. Table Creation & Extraction",
        "4. Image Generation & Insertion",
        "5. Watermarking",
        "6. Annotations",
        "7. PDF Merging",
        "8. Text Search & Redaction",
        "9. PDF Encryption & Decryption",
        "10. Page-to-Image Rendering",
    ]

    page.insert_text(
        (50, 220),
        "Table of Contents",
        fontsize=18,
        fontname="hebo",
        color=(0.2, 0.2, 0.2),
    )
    for i, item in enumerate(toc_items):
        page.insert_text(
            (70, 260 + i * 28),
            item,
            fontsize=12,
            fontname="helv",
            color=(0.3, 0.3, 0.3),
        )

    # --- Page 2: Multiple fonts and styles ---
    page2 = doc.new_page(width=595, height=842)
    page2.insert_text((50, 60), "Font Showcase", fontsize=24, fontname="hebo", color=(0.1, 0.2, 0.6))

    fonts = [
        ("helv", "Helvetica (helv)", (0, 0, 0)),
        ("hebo", "Helvetica Bold Oblique (hebo)", (0.2, 0.2, 0.8)),
        ("tibo", "Times Bold Oblique (tibo)", (0.6, 0.1, 0.1)),
        ("cour", "Courier (cour)", (0, 0.5, 0)),
        ("cobo", "Courier Bold Oblique (cobo)", (0.5, 0.3, 0)),
        ("symb", "Symbol (symb): αβγδε", (0.4, 0, 0.4)),
    ]

    y = 110
    for fname, label, clr in fonts:
        page2.insert_text((70, y), label, fontsize=14, fontname=fname, color=clr)
        y += 35

    # Different sizes
    page2.insert_text((50, y + 20), "Size Showcase:", fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.6))
    y += 60
    for size in [8, 10, 12, 16, 20, 28]:
        page2.insert_text((70, y), f"Font size {size}pt", fontsize=size, fontname="helv", color=(0.2, 0.2, 0.2))
        y += size + 15

    filepath = os.path.join(OUTPUT_DIR, "01_rich_text.pdf")
    doc.save(filepath)
    doc.close()
    print(f"  ✓ Created: {filepath}")
    print(f"    → 2 pages: title page with TOC + font/size showcase\n")


# ─────────────────────────────────────────────────────────────
# 2. DRAWING SHAPES & VECTOR GRAPHICS
# ─────────────────────────────────────────────────────────────
def demo_shapes():
    """Draw various shapes including lines, rectangles, circles, and curves."""
    print("=" * 60)
    print("DEMO 2: Drawing Shapes & Vector Graphics")
    print("=" * 60)

    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)

    page.insert_text((50, 50), "Shapes & Vector Graphics", fontsize=24, fontname="hebo", color=(0.1, 0.2, 0.6))

    shape = page.new_shape()

    # Rectangles
    page.insert_text((50, 100), "Rectangles:", fontsize=12, fontname="hebo")
    shape.draw_rect(pymupdf.Rect(50, 115, 150, 175))
    shape.finish(color=(0.8, 0.1, 0.1), fill=(1, 0.9, 0.9), width=2)

    shape.draw_rect(pymupdf.Rect(170, 115, 270, 175))
    shape.finish(color=(0.1, 0.6, 0.1), fill=(0.9, 1, 0.9), width=2, dashes="[3 2]")

    shape.draw_rect(pymupdf.Rect(290, 115, 390, 175))
    shape.finish(color=(0.1, 0.1, 0.8), fill=(0.9, 0.9, 1), width=3)

    # Circles
    page.insert_text((50, 210), "Circles:", fontsize=12, fontname="hebo")
    shape.draw_circle(pymupdf.Point(100, 270), 30)
    shape.finish(color=(0.9, 0.2, 0.2), fill=(1, 0.8, 0.8), width=2)

    shape.draw_circle(pymupdf.Point(220, 270), 30)
    shape.finish(color=(0.2, 0.7, 0.2), fill=(0.8, 1, 0.8), width=2)

    shape.draw_circle(pymupdf.Point(340, 270), 30)
    shape.finish(color=(0.2, 0.2, 0.9), fill=(0.8, 0.8, 1), width=2)

    # Lines with different styles
    page.insert_text((50, 330), "Lines:", fontsize=12, fontname="hebo")
    shape.draw_line(pymupdf.Point(50, 350), pymupdf.Point(400, 350))
    shape.finish(color=(0, 0, 0), width=1)

    shape.draw_line(pymupdf.Point(50, 370), pymupdf.Point(400, 370))
    shape.finish(color=(0.5, 0, 0), width=3, dashes="[5 3]")

    shape.draw_line(pymupdf.Point(50, 390), pymupdf.Point(400, 390))
    shape.finish(color=(0, 0, 0.5), width=2, dashes="[8 4 2 4]")

    # Polygon (star shape)
    page.insert_text((50, 430), "Polygon (Star):", fontsize=12, fontname="hebo")
    import math
    cx, cy, r_out, r_in = 150, 520, 50, 20
    points = []
    for i in range(10):
        angle = math.pi / 2 + i * math.pi / 5
        r = r_out if i % 2 == 0 else r_in
        points.append(pymupdf.Point(cx + r * math.cos(angle), cy - r * math.sin(angle)))

    shape.draw_polyline(points + [points[0]])
    shape.finish(color=(0.8, 0.6, 0), fill=(1, 0.95, 0.7), width=2)

    # Bezier curves
    page.insert_text((280, 430), "Bézier Curves:", fontsize=12, fontname="hebo")
    shape.draw_bezier(
        pymupdf.Point(280, 480),
        pymupdf.Point(350, 450),
        pymupdf.Point(420, 550),
        pymupdf.Point(500, 480),
    )
    shape.finish(color=(0.6, 0, 0.6), width=3)

    shape.draw_bezier(
        pymupdf.Point(280, 520),
        pymupdf.Point(380, 480),
        pymupdf.Point(380, 580),
        pymupdf.Point(500, 530),
    )
    shape.finish(color=(0, 0.6, 0.6), width=2, dashes="[4 2]")

    shape.commit()

    filepath = os.path.join(OUTPUT_DIR, "02_shapes.pdf")
    doc.save(filepath)
    doc.close()
    print(f"  ✓ Created: {filepath}")
    print(f"    → Rectangles, circles, lines, star polygon, Bézier curves\n")


# ─────────────────────────────────────────────────────────────
# 3. TABLE CREATION & EXTRACTION
# ─────────────────────────────────────────────────────────────
def demo_tables():
    """Create a PDF with a table, then extract it back."""
    print("=" * 60)
    print("DEMO 3: Table Creation & Extraction")
    print("=" * 60)

    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)

    page.insert_text((50, 50), "Table Demo", fontsize=24, fontname="hebo", color=(0.1, 0.2, 0.6))

    # Draw a table manually using shapes
    shape = page.new_shape()
    headers = ["Name", "Language", "Stars", "License"]
    data = [
        ["PyMuPDF", "Python/C", "9,000+", "AGPL-3.0"],
        ["pdf.js", "JavaScript", "48,000+", "Apache-2.0"],
        ["Apache PDFBox", "Java", "2,500+", "Apache-2.0"],
        ["Poppler", "C++", "1,800+", "GPL-2.0"],
        ["iText", "Java/.NET", "1,700+", "AGPL-3.0"],
    ]

    x_start, y_start = 50, 90
    col_widths = [130, 100, 90, 120]
    row_height = 30
    total_width = sum(col_widths)

    # Header row background
    shape.draw_rect(pymupdf.Rect(x_start, y_start, x_start + total_width, y_start + row_height))
    shape.finish(color=(0.1, 0.2, 0.6), fill=(0.1, 0.2, 0.6))

    # Draw header text
    x = x_start
    for i, header in enumerate(headers):
        page.insert_text((x + 8, y_start + 20), header, fontsize=11, fontname="hebo", color=(1, 1, 1))
        x += col_widths[i]

    # Draw data rows
    for row_idx, row_data in enumerate(data):
        y = y_start + (row_idx + 1) * row_height
        # Alternating row background
        if row_idx % 2 == 0:
            shape.draw_rect(pymupdf.Rect(x_start, y, x_start + total_width, y + row_height))
            shape.finish(color=None, fill=(0.95, 0.95, 1))

        x = x_start
        for i, cell in enumerate(row_data):
            page.insert_text((x + 8, y + 20), cell, fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
            x += col_widths[i]

    # Draw grid lines
    total_rows = len(data) + 1
    # Horizontal lines
    for i in range(total_rows + 1):
        y = y_start + i * row_height
        shape.draw_line(pymupdf.Point(x_start, y), pymupdf.Point(x_start + total_width, y))
        shape.finish(color=(0.5, 0.5, 0.5), width=0.5)

    # Vertical lines
    x = x_start
    for w in [0] + col_widths:
        x += w if w > 0 else 0
        shape.draw_line(pymupdf.Point(x, y_start), pymupdf.Point(x, y_start + total_rows * row_height))
        shape.finish(color=(0.5, 0.5, 0.5), width=0.5)
        if w == 0:
            continue

    shape.commit()

    filepath = os.path.join(OUTPUT_DIR, "03_tables.pdf")
    doc.save(filepath)
    doc.close()
    print(f"  ✓ Created: {filepath}")

    # --- Now extract the table back ---
    doc = pymupdf.open(filepath)
    page = doc[0]
    tabs = page.find_tables()
    print(f"  ✓ Extracted {len(tabs.tables)} table(s) from the PDF")
    if tabs.tables:
        table_data = tabs[0].extract()
        print(f"    → Table has {len(table_data)} rows × {len(table_data[0])} columns")
        for row in table_data:
            print(f"      {row}")
    doc.close()
    print()


# ─────────────────────────────────────────────────────────────
# 4. IMAGE GENERATION, INSERTION & EXTRACTION
# ─────────────────────────────────────────────────────────────
def demo_images():
    """Generate an image using Pixmap, insert it into a PDF, then extract it."""
    print("=" * 60)
    print("DEMO 4: Image Generation, Insertion & Extraction")
    print("=" * 60)

    # --- Step 1: Generate a gradient image using Pixmap ---
    width, height = 200, 200
    pix = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, width, height), 1)  # with alpha
    pix.clear_with(255)  # white background

    # Draw a gradient pattern
    for y in range(height):
        for x in range(width):
            r = int(255 * x / width)
            g = int(255 * y / height)
            b = int(255 * (1 - x / width))
            pix.set_pixel(x, y, (r, g, b, 255))

    gradient_path = os.path.join(OUTPUT_DIR, "gradient.png")
    pix.save(gradient_path)
    print(f"  ✓ Generated gradient image: {gradient_path}")

    # --- Step 2: Insert image into PDF ---
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)

    page.insert_text((50, 50), "Image Insertion Demo", fontsize=24, fontname="hebo", color=(0.1, 0.2, 0.6))

    page.insert_text((50, 100), "Generated gradient image:", fontsize=12, fontname="helv")
    page.insert_image(pymupdf.Rect(50, 115, 250, 315), filename=gradient_path)

    page.insert_text((280, 100), "Same image (rotated 90°):", fontsize=12, fontname="helv")
    page.insert_image(pymupdf.Rect(280, 115, 480, 315), filename=gradient_path, rotate=90)

    filepath = os.path.join(OUTPUT_DIR, "04_images.pdf")
    doc.save(filepath)
    doc.close()
    print(f"  ✓ Created PDF with images: {filepath}")

    # --- Step 3: Extract images back ---
    doc = pymupdf.open(filepath)
    page = doc[0]
    image_list = page.get_images()
    print(f"  ✓ Found {len(image_list)} image(s) in the PDF")

    for i, img in enumerate(image_list):
        xref = img[0]
        pix = pymupdf.Pixmap(doc, xref)
        if pix.n - pix.alpha > 3:
            pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
        extracted_path = os.path.join(OUTPUT_DIR, f"04_extracted_image_{i+1}.png")
        pix.save(extracted_path)
        print(f"    → Extracted image {i+1}: {extracted_path} ({pix.width}×{pix.height})")

    doc.close()
    print()


# ─────────────────────────────────────────────────────────────
# 5. WATERMARKING
# ─────────────────────────────────────────────────────────────
def demo_watermark():
    """Add a text-based watermark to a PDF."""
    print("=" * 60)
    print("DEMO 5: Watermarking")
    print("=" * 60)

    # First create a source document
    doc = pymupdf.open()
    for i in range(3):
        page = doc.new_page(width=595, height=842)
        page.insert_text(
            (50, 100),
            f"Page {i+1}: Important Document Content",
            fontsize=18,
            fontname="helv",
        )
        page.insert_text(
            (50, 140),
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n"
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
            fontsize=11,
            fontname="helv",
            color=(0.3, 0.3, 0.3),
        )

    # Add diagonal text watermark to every page
    for page in doc:
        # Create watermark text
        shape = page.new_shape()
        # Draw a large "CONFIDENTIAL" watermark across the page
        page.insert_text(
            (80, 500),
            "CONFIDENTIAL",
            fontsize=72,
            fontname="hebo",
            color=(0.9, 0.1, 0.1),
            overlay=True,
        )
        # Add a subtle border watermark
        rect = page.rect
        shape.draw_rect(pymupdf.Rect(rect.x0 + 10, rect.y0 + 10, rect.x1 - 10, rect.y1 - 10))
        shape.finish(color=(0.8, 0.1, 0.1), width=1, dashes="[5 3]")
        shape.commit()

    filepath = os.path.join(OUTPUT_DIR, "05_watermarked.pdf")
    doc.save(filepath)
    doc.close()
    print(f"  ✓ Created: {filepath}")
    print(f"    → 3 pages with diagonal 'CONFIDENTIAL' watermark + dashed border\n")


# ─────────────────────────────────────────────────────────────
# 6. ANNOTATIONS
# ─────────────────────────────────────────────────────────────
def demo_annotations():
    """Add various types of annotations to a PDF."""
    print("=" * 60)
    print("DEMO 6: Annotations (Highlights, Comments, Stamps)")
    print("=" * 60)

    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)

    # Add text content
    page.insert_text((50, 60), "Annotations Demo", fontsize=24, fontname="hebo", color=(0.1, 0.2, 0.6))
    page.insert_text((50, 110), "This line will be highlighted in yellow.", fontsize=12, fontname="helv")
    page.insert_text((50, 140), "This line will be underlined in red.", fontsize=12, fontname="helv")
    page.insert_text((50, 170), "This line will have a strikethrough.", fontsize=12, fontname="helv")
    page.insert_text((50, 220), "Check the sticky note in the margin →", fontsize=12, fontname="helv")
    page.insert_text((50, 270), "See the freetext annotation below:", fontsize=12, fontname="helv")

    # Highlight annotation
    highlight_rect = pymupdf.Rect(48, 96, 380, 115)
    annot = page.add_highlight_annot(highlight_rect)
    annot.set_colors(stroke=(1, 1, 0))  # yellow
    annot.update()

    # Underline annotation
    underline_rect = pymupdf.Rect(48, 126, 340, 145)
    annot = page.add_underline_annot(underline_rect)
    annot.set_colors(stroke=(1, 0, 0))  # red
    annot.update()

    # Strikethrough annotation
    strike_rect = pymupdf.Rect(48, 156, 380, 175)
    annot = page.add_strikeout_annot(strike_rect)
    annot.update()

    # Sticky note (text annotation)
    annot = page.add_text_annot(
        pymupdf.Point(450, 205),
        "This is a sticky note!\nIt can contain multi-line text.",
    )
    annot.set_colors(stroke=(0, 0.5, 1))
    annot.update()

    # Freetext annotation (editable text box)
    freetext_rect = pymupdf.Rect(50, 290, 400, 370)
    annot = page.add_freetext_annot(
        freetext_rect,
        "This is a freetext annotation.\nIt appears directly on the page\nwith a visible border.",
        fontsize=12,
        fontname="helv",
        text_color=(0, 0, 0.6),
        fill_color=(0.95, 0.95, 1),
    )
    annot.update()

    # Stamp annotation
    stamp_rect = pymupdf.Rect(350, 400, 545, 480)
    annot = page.add_stamp_annot(stamp_rect, stamp=0)  # 0 = "Approved"
    annot.set_colors(stroke=(0, 0.6, 0))
    annot.set_opacity(0.6)
    annot.update()

    # Rectangle annotation with a note
    rect_annot_area = pymupdf.Rect(50, 500, 300, 560)
    annot = page.add_rect_annot(rect_annot_area)
    annot.set_colors(stroke=(1, 0, 0), fill=(1, 0.95, 0.95))
    annot.set_info(content="This is a rectangle annotation with a popup note.")
    annot.update()
    page.insert_text((60, 535), "Rectangle annotation with popup", fontsize=10, fontname="helv", color=(0.5, 0, 0))

    filepath = os.path.join(OUTPUT_DIR, "06_annotations.pdf")
    doc.save(filepath)

    # List all annotations
    annot_count = 0
    for annot in page.annots():
        annot_count += 1
    print(f"  ✓ Created: {filepath}")
    print(f"    → {annot_count} annotations: highlight, underline, strikeout, sticky note,")
    print(f"      freetext, stamp, rectangle\n")
    doc.close()


# ─────────────────────────────────────────────────────────────
# 7. PDF MERGING
# ─────────────────────────────────────────────────────────────
def demo_merge():
    """Merge the previously created PDFs into one combined document."""
    print("=" * 60)
    print("DEMO 7: PDF Merging")
    print("=" * 60)

    files_to_merge = [
        "01_rich_text.pdf",
        "02_shapes.pdf",
        "03_tables.pdf",
    ]

    merged_doc = pymupdf.open()
    total_pages = 0

    for fname in files_to_merge:
        fpath = os.path.join(OUTPUT_DIR, fname)
        if os.path.exists(fpath):
            src = pymupdf.open(fpath)
            merged_doc.insert_pdf(src)
            page_count = len(src)
            total_pages += page_count
            print(f"  + Merged {fname} ({page_count} page(s))")
            src.close()

    # Add a table of contents
    toc = [
        [1, "Rich Text Demo", 1],
        [1, "Shapes & Graphics", 3],
        [1, "Table Demo", 4],
    ]
    merged_doc.set_toc(toc)

    filepath = os.path.join(OUTPUT_DIR, "07_merged.pdf")
    merged_doc.save(filepath)
    merged_doc.close()
    print(f"  ✓ Created: {filepath}")
    print(f"    → Combined {len(files_to_merge)} PDFs into {total_pages} total pages with TOC bookmarks\n")


# ─────────────────────────────────────────────────────────────
# 8. TEXT SEARCH & REDACTION
# ─────────────────────────────────────────────────────────────
def demo_search_redact():
    """Search for text and redact it from a PDF."""
    print("=" * 60)
    print("DEMO 8: Text Search & Redaction")
    print("=" * 60)

    # Create a document with sensitive info
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)

    page.insert_text((50, 60), "Document with Sensitive Data", fontsize=20, fontname="hebo", color=(0.1, 0.2, 0.6))

    content = [
        "Employee Report - Confidential",
        "",
        "Name: John Smith",
        "SSN: 123-45-6789",
        "Email: john.smith@example.com",
        "Phone: (555) 123-4567",
        "",
        "Name: Jane Doe",
        "SSN: 987-65-4321",
        "Email: jane.doe@example.com",
        "Phone: (555) 987-6543",
        "",
        "Salary: $120,000",
        "Department: Engineering",
    ]

    y = 110
    for line in content:
        page.insert_text((50, y), line, fontsize=12, fontname="helv", color=(0.2, 0.2, 0.2))
        y += 22

    # Save original
    original_path = os.path.join(OUTPUT_DIR, "08_original.pdf")
    doc.save(original_path)
    print(f"  ✓ Created original: {original_path}")

    # Search and redact SSNs and emails
    redact_terms = ["123-45-6789", "987-65-4321", "john.smith@example.com", "jane.doe@example.com"]

    found_count = 0
    for term in redact_terms:
        instances = page.search_for(term)
        for inst in instances:
            page.add_redact_annot(inst, fill=(0, 0, 0))
            found_count += 1

    page.apply_redactions()

    redacted_path = os.path.join(OUTPUT_DIR, "08_redacted.pdf")
    doc.save(redacted_path)
    doc.close()
    print(f"  ✓ Created redacted version: {redacted_path}")
    print(f"    → Found and redacted {found_count} sensitive items (SSNs + emails)")

    # Verify redaction by extracting text
    doc = pymupdf.open(redacted_path)
    text = doc[0].get_text()
    for term in redact_terms:
        assert term not in text, f"Redaction failed! '{term}' still found."
    print(f"    → Verified: sensitive data no longer present in text extraction\n")
    doc.close()


# ─────────────────────────────────────────────────────────────
# 9. PDF ENCRYPTION & DECRYPTION
# ─────────────────────────────────────────────────────────────
def demo_encryption():
    """Create an encrypted PDF and then decrypt it."""
    print("=" * 60)
    print("DEMO 9: PDF Encryption & Decryption")
    print("=" * 60)

    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((50, 72), "This document is encrypted!", fontsize=18, fontname="hebo")
    page.insert_text((50, 110), "Owner password: 'owner123'", fontsize=12, fontname="helv")
    page.insert_text((50, 135), "User password: 'user456'", fontsize=12, fontname="helv")
    page.insert_text((50, 175), "Permissions: print + copy + annotate (no modifications)", fontsize=11, fontname="helv", color=(0.4, 0.4, 0.4))

    # Set permissions
    perm = int(
        pymupdf.PDF_PERM_ACCESSIBILITY
        | pymupdf.PDF_PERM_PRINT
        | pymupdf.PDF_PERM_COPY
        | pymupdf.PDF_PERM_ANNOTATE
    )

    filepath = os.path.join(OUTPUT_DIR, "09_encrypted.pdf")
    doc.save(
        filepath,
        encryption=pymupdf.PDF_ENCRYPT_AES_256,
        owner_pw="owner123",
        user_pw="user456",
        permissions=perm,
    )
    doc.close()
    print(f"  ✓ Created encrypted PDF: {filepath}")
    print(f"    → Algorithm: AES-256")
    print(f"    → Owner password: 'owner123'")
    print(f"    → User password: 'user456'")

    # Now open and decrypt
    doc = pymupdf.open(filepath)
    print(f"  ✓ Needs password: {doc.needs_pass}")
    print(f"  ✓ Is encrypted: {doc.is_encrypted}")

    # Authenticate with user password
    rc = doc.authenticate("user456")
    print(f"  ✓ Authenticated with user password (return code: {rc})")

    text = doc[0].get_text()
    print(f"  ✓ Successfully read text: \"{text.strip().splitlines()[0]}\"")

    # Save a decrypted copy (no encryption params = decrypted)
    decrypted_path = os.path.join(OUTPUT_DIR, "09_decrypted.pdf")
    doc.save(decrypted_path)
    doc.close()
    print(f"  ✓ Saved decrypted copy: {decrypted_path}\n")


# ─────────────────────────────────────────────────────────────
# 10. PAGE-TO-IMAGE RENDERING (PIXMAP)
# ─────────────────────────────────────────────────────────────
def demo_page_to_image():
    """Render PDF pages as high-resolution images."""
    print("=" * 60)
    print("DEMO 10: Page-to-Image Rendering (Pixmap)")
    print("=" * 60)

    # Open the shapes demo for a visually interesting page
    shapes_pdf = os.path.join(OUTPUT_DIR, "02_shapes.pdf")
    if not os.path.exists(shapes_pdf):
        print("  ✗ Shapes PDF not found, skipping.\n")
        return

    doc = pymupdf.open(shapes_pdf)
    page = doc[0]

    # Render at different resolutions
    for zoom_factor, label in [(1.0, "72dpi"), (2.0, "144dpi"), (3.0, "216dpi")]:
        mat = pymupdf.Matrix(zoom_factor, zoom_factor)
        pix = page.get_pixmap(matrix=mat)
        img_path = os.path.join(OUTPUT_DIR, f"10_rendered_{label}.png")
        pix.save(img_path)
        print(f"  ✓ Rendered at {label}: {img_path} ({pix.width}×{pix.height} px)")

    # Render with transparent background
    mat = pymupdf.Matrix(2.0, 2.0)
    pix = page.get_pixmap(matrix=mat, alpha=True)
    alpha_path = os.path.join(OUTPUT_DIR, "10_rendered_transparent.png")
    pix.save(alpha_path)
    print(f"  ✓ Rendered with alpha: {alpha_path} ({pix.width}×{pix.height} px)")

    # Render a specific region (clip)
    clip = pymupdf.Rect(40, 80, 410, 310)  # shapes area
    pix = page.get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=clip)
    clip_path = os.path.join(OUTPUT_DIR, "10_rendered_clipped.png")
    pix.save(clip_path)
    print(f"  ✓ Rendered clipped region: {clip_path} ({pix.width}×{pix.height} px)")

    doc.close()
    print()


# ─────────────────────────────────────────────────────────────
# 11. METADATA INSPECTION
# ─────────────────────────────────────────────────────────────
def demo_metadata():
    """Read and set document metadata."""
    print("=" * 60)
    print("DEMO 11: Document Metadata")
    print("=" * 60)

    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((50, 72), "Document with Custom Metadata", fontsize=18, fontname="hebo")

    # Set metadata
    doc.set_metadata({
        "title": "PyMuPDF Advanced Demo",
        "author": "PyMuPDF Demo Script",
        "subject": "Demonstrating PDF metadata capabilities",
        "keywords": "pymupdf, demo, python, pdf",
        "creator": "advanced_demo.py",
        "producer": "PyMuPDF",
    })

    filepath = os.path.join(OUTPUT_DIR, "11_metadata.pdf")
    doc.save(filepath)
    doc.close()
    print(f"  ✓ Created: {filepath}")

    # Read back metadata
    doc = pymupdf.open(filepath)
    meta = doc.metadata
    print(f"  ✓ Document metadata:")
    for key, value in meta.items():
        if value:
            print(f"    → {key}: {value}")

    print(f"  ✓ Page count: {doc.page_count}")
    print(f"  ✓ Is PDF: {doc.is_pdf}")
    doc.close()
    print()


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
def main():
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + "  PyMuPDF Advanced Demo".center(58) + "║")
    print("║" + "  Comprehensive PDF Manipulation Showcase".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    print()

    ensure_output_dir()

    demos = [
        demo_rich_text_pdf,
        demo_shapes,
        demo_tables,
        demo_images,
        demo_watermark,
        demo_annotations,
        demo_merge,
        demo_search_redact,
        demo_encryption,
        demo_page_to_image,
        demo_metadata,
    ]

    passed = 0
    failed = 0
    for demo in demos:
        try:
            demo()
            passed += 1
        except Exception as e:
            print(f"  ✗ FAILED: {e}\n")
            failed += 1

    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(demos)} demos")
    print("=" * 60)
    print(f"\nAll output files are in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
