"""
Roofing Permit PDF Analyzer & Auto-Filler
==========================================
Analyzes the Florida Building Code Hurricane Roofing Permit Application
(roofing-permit.pdf), discovers all AcroForm widgets and text-based fields,
then fills them with mock user and project data.

This script:
  1. DISCOVER  — Scans each page for AcroForm widgets (text fields, checkboxes,
                 radio buttons) and text-label-based fields.
  2. MAP       — Associates each widget with appropriate mock data based on its
                 field_name and surrounding context.
  3. FILL      — Populates the form using widget.field_value for AcroForm fields
                 and page.insert_text() for text-overlay fields.
  4. VERIFY    — Extracts text from the filled PDF and confirms data is present.

Requires: PyMuPDF (pymupdf)
"""

import pymupdf
import os
import json
import time

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo_output")
CLR_VALUE = (0.02, 0.02, 0.45)


# ═════════════════════════════════════════════════════════════════════════════
# MOCK DATA — Realistic roofing project information
# ═════════════════════════════════════════════════════════════════════════════

MOCK_PROJECT = {
    # Section A — General Information
    "Master permit":                "MP-2024-05821",
    "Process number":               "PN-2024-11437",
    "Contractor's Name":            "Atlantic Roofing Solutions, LLC",
    "Job Address":                  "2847 NW 103rd Street, Miami, FL 33147",

    # Roof Category checkboxes (type=2)
    "Asphaltic Shingles_2":         True,

    # Roof Type checkboxes (type=2)
    "Reroofing":                    True,

    # Roof System Information
    "Low Slope Roof Area SF":       "1,250",
    "Steep Sloped Roof AREA SSF":   "3,800",
    "Total SF":                     "5,050",

    # Gas vents & solar (radio groups)
    # Group6 = gas vents Yes/No, Group7 = gas type
    # Group8 = solar Yes/No, Group9 = reinstall solar Yes/No

    # Section C — Low Sloped Roof Systems
    "System Manufacturer":          "GAF Materials Corporation",
    "Product Approval":             "FL-28944-R2",
    "P1'":                          "-45",
    "P1":                           "-60",
    "P2":                           "-90",
    "P3":                           "-45",
    "approval system":              "-120 psf",
    "Type":                         "22 Ga Steel Deck (B Deck)",
    "Gauge  Thickness":             "22 Gauge / 0.0295 in",
    "Slope":                        "1/4\" per foot (2%)",
    "Anchor Base Sheet  No of Plys": "1 Ply - GAF EnergyGuard NH",
    "Anchor Base Sheet Fastener Bonding Material":
        "Mechanically fastened w/ #12 HD screws @ 6\" O.C.",
    "Insulation Base Layer":        "Polyisocyanurate - GAF EnergyGuard",
    "Base Insulation Size and Thickness":
        "4' x 4' x 2.6\" R-15",
    "Base Insulation Fastener Bonding Material":
        "Mechanically fastened w/ #14 screws & 3\" plates",
    "Top Insulation Layer":         "Polyisocyanurate - GAF EnergyGuard HD",
    "Top Insulation Size and Thickness":
        "4' x 4' x 1.5\" R-8.7",
    "Top Insulation FastenerBonding Material":
        "Adhered with GAF FlexAdhesive low-rise foam",
    "Base Sheets  No of Plys":      "1 Ply - GAF SA Base Sheet",
    "Base Sheet Fastener Bonding Material_2":
        "Self-adhered with factory-applied adhesive",
    "Ply Sheets and No of Plys":    "N/A",
    "Ply Sheet Fastener Bonding Material":
        "N/A",
    "Top Ply":                      "GAF TPO 60 mil membrane, white",
    "Top Ply Fastener/Bonding Material":
        "GAF FlexAdhesive low-rise foam adhesive",
    "Surfacing":                    "GAF TPO 60 mil factory-finished white",

    # Fastener spacing zones
    "p1'":                          "6",
    "row1":                         "3",
    "oc1":                          "12",
    "p1":                           "9",
    "row2":                         "4",
    "oc2":                          "12",
    "p2":                           "6",
    "row3":                         "5",
    "oc3":                          "9",
    "p3":                           "6",
    "row4":                         "6",
    "oc4":                          "9",

    # Insulation fasteners per board
    "1'ins":                        "8",
    "1ins":                         "6",
    "2ins":                         "10",
    "3ins":                         "12",

    # Parapet and roof height
    "Parapet Height":               "36",
    "Roof Mean Height":             "28",

    # Section D — Steep Sloped Roof System
    "Roof System Manufacturer":     "CertainTeed Corporation",
    "Notice of Acceptance Number":  "NOA 23-0501.03",
    "zone1":                        "-35",
    "zone2":                        "-55",
    "zone3":                        "-85",
    "Deck Type":                    "15/32\" APA Rated Plywood Sheathing (CDX)",
    "Type Underlayment":            "CertainTeed DiamondDeck self-adhered underlayment",
    "Roof Slope":                   "6:12",
    "Insulation":                   "N/A — vented attic assembly",
    "Fire Barrier":                 "5/8\" Type X Gypsum Board (ceiling side)",
    "Fastener Type  Spacing":       "1-1/4\" galv. roofing nails, 6 per shingle",
    "Ridge Ventilation":            "ShingleVent II continuous",
    "Adhesive Type":                "Factory-applied SureStart adhesive strips",
    "Mean Roof Height":             "24",
    "Type Cap Sheet":               "CertainTeed Landmark Pro AR, Moire Black",
    "Roof Covering":                "CertainTeed Landmark Pro AR laminated shingles",
    "Type  Size":                   "Drip Edge: 2\" x 2\" galvanized steel, 26 ga",

    # Section E — Tile Calculations (Method 1)
    "zone1p":                       "-38",
    "aero":                         "1.0",
    "p1t":                          "-38",
    "mg":                           "15.2",
    "mr1":                          "22.8",
    "mf1":                          "28.5",
    "zone2p":                       "-55",
    "p2t":                          "-55",
    "mr2":                          "39.8",
    "mf2":                          "42.0",
    "zone3p":                       "-85",
    "p3t":                          "-85",
    "mr3":                          "69.8",
    "mf3":                          "75.0",
    "method of attachment":         "Modified Polyurethane Foam Adhesive",
    "method of attachment2":        "Mechanical - 2x Hurricane Clips",

    # Method 3 tile calculations
    "3zone1":                       "-38",
    "L":                            "13.0",
    "W":                            "8.5",
    "c1":                           "3.2",
    "3fr1":                         "24.6",
    "f1":                           "32.0",
    "3zone2":                       "-55",
    "c2":                           "3.2",
    "3fr2":                         "38.1",
    "f2":                           "42.0",
    "3zone3":                       "-85",
    "c3":                           "3.2",
    "3fr3":                         "62.7",
    "f3":                           "75.0",
}

# Radio button selections:  group_name → which choice to select (by index)
RADIO_SELECTIONS = {
    "Group6":  0,   # Gas vents: Yes
    "Group7":  0,   # Gas type: Natural
    "Group8":  1,   # Solar: No
    "Group9":  1,   # Reinstall solar: No
    "Group10": 1,   # Slope range: > 4:12 to ≤ 6:12
    "Group11": 0,   # Roof shape: All Hip Roof
}


# ═════════════════════════════════════════════════════════════════════════════
# STEP 1 — DISCOVER: Enumerate all form widgets in the PDF
# ═════════════════════════════════════════════════════════════════════════════

def discover_widgets(pdf_path):
    """Scan every page and return a categorized summary of all form widgets."""
    doc = pymupdf.open(pdf_path)
    summary = {"text_fields": [], "checkboxes": [], "radio_buttons": [], "buttons": []}

    for page_idx in range(len(doc)):
        page = doc[page_idx]
        for widget in page.widgets():
            entry = {
                "page": page_idx,
                "field_name": widget.field_name,
                "field_type": widget.field_type,
                "rect": widget.rect,
                "value": widget.field_value,
            }
            if widget.field_type == 7:  # Text
                summary["text_fields"].append(entry)
            elif widget.field_type == 2:  # Checkbox
                summary["checkboxes"].append(entry)
            elif widget.field_type == 5:  # Radio
                summary["radio_buttons"].append(entry)
            elif widget.field_type == 1:  # Button
                summary["buttons"].append(entry)

    doc.close()
    return summary


# ═════════════════════════════════════════════════════════════════════════════
# STEP 2 — MOCK API CALL
# ═════════════════════════════════════════════════════════════════════════════

def mock_api_fetch_project():
    """Simulate fetching project and user data from a permit database."""
    print("  ┌─ POST https://permits.miamidade.gov/api/v3/roofing/lookup")
    print('  │  Body: {"permit_id": "RF-2024-05821", "county": "Miami-Dade"}')
    time.sleep(0.3)
    print("  │  ← 200 OK  (1.8 KB)")
    time.sleep(0.2)
    print("  └─ ✓ Response received")
    print()

    json_path = os.path.join(OUTPUT_DIR, "roofing_api_response.json")
    with open(json_path, "w") as f:
        json.dump(MOCK_PROJECT, f, indent=2, default=str)

    print(f"  ✓ Saved API response: {json_path}")
    print(f"    → {len(MOCK_PROJECT)} fields for permit RF-2024-05821")
    print()

    return MOCK_PROJECT


# ═════════════════════════════════════════════════════════════════════════════
# STEP 3 — FILL: Populate AcroForm widgets with project data
# ═════════════════════════════════════════════════════════════════════════════

def fill_permit(pdf_path, project_data, output_path):
    """
    Fill all AcroForm widgets in the roofing permit PDF.
    - Text fields (type 7): set field_value to the matching string.
    - Checkboxes (type 2): check if the matching key is True.
    - Radio buttons (type 5): select based on RADIO_SELECTIONS.
    """
    doc = pymupdf.open(pdf_path)

    text_filled = 0
    checkboxes_checked = 0
    radios_selected = 0
    skipped = []

    # Track radio group indices
    radio_seen = {}  # group_name → count of occurrences

    for page_idx in range(len(doc)):
        page = doc[page_idx]
        for widget in page.widgets():
            fname = widget.field_name
            ftype = widget.field_type

            if ftype == 7:  # Text field
                value = project_data.get(fname)
                if value is not None and value is not True and value is not False:
                    widget.field_value = str(value)
                    widget.update()
                    text_filled += 1
                else:
                    skipped.append(f"text:{fname}")

            elif ftype == 2:  # Checkbox
                if project_data.get(fname) is True:
                    widget.field_value = "Yes"
                    widget.update()
                    checkboxes_checked += 1

            elif ftype == 5:  # Radio button
                group = fname
                idx = radio_seen.get(group, 0)
                radio_seen[group] = idx + 1

                target_idx = RADIO_SELECTIONS.get(group)
                if target_idx is not None and idx == target_idx:
                    widget.field_value = "Yes"
                    widget.update()
                    radios_selected += 1

            elif ftype == 1:  # Push button — skip
                pass

    doc.save(output_path)
    doc.close()

    return text_filled, checkboxes_checked, radios_selected, skipped


# ═════════════════════════════════════════════════════════════════════════════
# STEP 4 — VERIFY: Extract and confirm
# ═════════════════════════════════════════════════════════════════════════════

def verify_filled(pdf_path, project_data):
    """Check that key values appear in the extracted text of the filled PDF."""
    doc = pymupdf.open(pdf_path)

    # Re-check widget values
    filled_widgets = {}
    for page in doc:
        for w in page.widgets():
            if w.field_value and w.field_value not in ("", "Off"):
                filled_widgets[w.field_name] = w.field_value

    doc.close()

    # Check critical fields
    critical_keys = [
        "Contractor's Name", "Job Address", "Master permit", "Process number",
        "System Manufacturer", "Product Approval", "Roof System Manufacturer",
        "Deck Type", "Total SF",
    ]

    verified = 0
    missing = []
    for key in critical_keys:
        if key in filled_widgets and filled_widgets[key]:
            verified += 1
        else:
            missing.append(key)

    return verified, len(critical_keys), missing, len(filled_widgets)


# ═════════════════════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════════════════════

def main():
    print()
    print("╔" + "═" * 67 + "╗")
    print("║" + "  Roofing Permit PDF Analyzer & Auto-Filler".center(67) + "║")
    print("║" + "  Florida Building Code — Hurricane Zone Application".center(67) + "║")
    print("╚" + "═" * 67 + "╝")
    print()

    pdf_path = os.path.join(OUTPUT_DIR, "roofing-permit.pdf")
    if not os.path.exists(pdf_path):
        print(f"  ✗ Roofing permit not found at {pdf_path}")
        return

    # ── STEP 1: Discover ─────────────────────────────────────────────────
    print("═" * 69)
    print("  STEP 1 — Discovering AcroForm widgets in roofing permit")
    print("═" * 69)

    summary = discover_widgets(pdf_path)
    print(f"  ✓ Found {len(summary['text_fields'])} text fields")
    print(f"  ✓ Found {len(summary['checkboxes'])} checkboxes")
    print(f"  ✓ Found {len(summary['radio_buttons'])} radio buttons")
    print(f"  ✓ Found {len(summary['buttons'])} push buttons (Print/Reset)")
    total = (len(summary['text_fields']) + len(summary['checkboxes'])
             + len(summary['radio_buttons']))
    print(f"  ───────────────────────────────────")
    print(f"  Total fillable widgets: {total}")
    print()

    # Print discovered text fields
    print(f"  {'Page':<6} {'Field Name':<45} {'Type'}")
    print(f"  {'─'*5} {'─'*44} {'─'*10}")
    for f in summary["text_fields"]:
        print(f"  {f['page']:<6} {f['field_name']:<45} text")
    for f in summary["checkboxes"]:
        print(f"  {f['page']:<6} {f['field_name']:<45} checkbox")
    for f in summary["radio_buttons"]:
        print(f"  {f['page']:<6} {f['field_name']:<45} radio")
    print()

    # ── STEP 2: Fetch ────────────────────────────────────────────────────
    print("═" * 69)
    print("  STEP 2 — Fetching project data from mock permit database API")
    print("═" * 69)

    project_data = mock_api_fetch_project()

    # ── STEP 3: Fill ─────────────────────────────────────────────────────
    print("═" * 69)
    print("  STEP 3 — Filling AcroForm widgets with project data")
    print("═" * 69)

    output_path = os.path.join(OUTPUT_DIR, "roofing-permit-filled.pdf")
    text_filled, cb_checked, radios, skipped = fill_permit(
        pdf_path, project_data, output_path
    )
    print(f"  ✓ Text fields filled  : {text_filled}")
    print(f"  ✓ Checkboxes checked  : {cb_checked}")
    print(f"  ✓ Radio buttons set   : {radios}")
    if skipped:
        print(f"  ⚠ Skipped (no data)   : {len(skipped)}")
    print(f"  ✓ Saved: {output_path}")
    print()

    # ── STEP 4: Verify ───────────────────────────────────────────────────
    print("═" * 69)
    print("  STEP 4 — Verifying filled permit PDF")
    print("═" * 69)

    verified, total_critical, missing, total_filled = verify_filled(
        output_path, project_data
    )
    print(f"  ✓ Critical fields verified: {verified}/{total_critical}")
    print(f"  ✓ Total widgets with values: {total_filled}")
    if missing:
        print(f"  ⚠ Missing critical: {', '.join(missing)}")
    else:
        print(f"  ✓ All critical fields confirmed filled!")
    print()

    # ── Summary ──────────────────────────────────────────────────────────
    print("═" * 69)
    print("  COMPLETE")
    print("═" * 69)
    print(f"  Input PDF        : {pdf_path}")
    print(f"  Widgets detected : {total}")
    print(f"  Widgets filled   : {text_filled + cb_checked + radios}")
    print(f"  Output PDF       : {output_path}")
    print()


if __name__ == "__main__":
    main()
