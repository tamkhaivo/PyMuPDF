"""Analyze the roofing-permit.pdf to understand its structure."""
import pymupdf
import json

pdf_path = r"c:\Users\tamkh\Documents\PyMuPDF\demo_output\roofing-permit.pdf"
doc = pymupdf.open(pdf_path)

print(f"Pages: {len(doc)}")
print(f"Metadata: {doc.metadata}")
print()

for i, page in enumerate(doc):
    print(f"{'='*70}")
    print(f"PAGE {i}  (size: {page.rect.width:.0f} x {page.rect.height:.0f})")
    print(f"{'='*70}")

    # Check for form widgets (AcroForm fields)
    widgets = list(page.widgets())
    if widgets:
        print(f"\n  FORM WIDGETS ({len(widgets)}):")
        for w in widgets:
            print(f"    field_name={w.field_name!r}  type={w.field_type}  "
                  f"value={w.field_value!r}  rect={w.rect}")
    else:
        print("\n  No AcroForm widgets found.")

    # Get all text with positions
    print(f"\n  TEXT SPANS:")
    text_dict = page.get_text("dict")
    for block in text_dict["blocks"]:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                text = span["text"].strip()
                if text:
                    b = span["bbox"]
                    print(f"    [{b[0]:>6.1f},{b[1]:>6.1f},{b[2]:>6.1f},{b[3]:>6.1f}] "
                          f"sz={span['size']:.1f} font={span['font']:<20s} "
                          f'"{text}"')

    # Get drawings
    drawings = page.get_drawings()
    h_lines = []
    for d in drawings:
        is_dashed = bool(d.get("dashes"))
        for item in d.get("items", []):
            if item[0] == "l":
                p1, p2 = item[1], item[2]
                if abs(p1.y - p2.y) < 2 and abs(p1.x - p2.x) > 30:
                    h_lines.append({
                        "x1": min(p1.x, p2.x), "x2": max(p1.x, p2.x),
                        "y": (p1.y + p2.y) / 2, "dashed": is_dashed,
                    })

    if h_lines:
        print(f"\n  HORIZONTAL LINES ({len(h_lines)}):")
        for hl in sorted(h_lines, key=lambda l: (l["y"], l["x1"])):
            print(f"    x=[{hl['x1']:.0f} → {hl['x2']:.0f}]  y={hl['y']:.0f}  "
                  f"{'dashed' if hl['dashed'] else 'solid'}  "
                  f"len={hl['x2']-hl['x1']:.0f}")

    # Also check for rectangles (form boxes)
    rects = []
    for d in drawings:
        for item in d.get("items", []):
            if item[0] == "re":  # rectangle
                rects.append(item[1])
    if rects:
        print(f"\n  RECTANGLES ({len(rects)}):")
        for r in rects[:20]:
            print(f"    ({r.x0:.0f},{r.y0:.0f}) → ({r.x1:.0f},{r.y1:.0f})  "
                  f"size={r.width:.0f}x{r.height:.0f}")

    print()

doc.close()
