"""Quick verification of filled roofing permit."""
import pymupdf

doc = pymupdf.open(r"c:\Users\tamkh\Documents\PyMuPDF\demo_output\roofing-permit-filled.pdf")
filled = 0
empty = 0
for page in doc:
    for w in page.widgets():
        if w.field_value and w.field_value not in ("", "Off"):
            filled += 1
            print(f"  [P{page.number}] {w.field_name:<45} = {w.field_value}")
        else:
            empty += 1
print(f"\nFilled: {filled}  |  Empty: {empty}")
doc.close()
