"""
PDF Form Fill Workflow
======================
A complete document automation pipeline demonstrating:

  Phase 1 — Generate a complex, multi-page blank PDF form with 30+ personal
            information fields organized into professional sections.
  Phase 2 — Mock an API call to a database that returns a JSON payload
            containing all the personal information to fill out.
  Phase 3 — Fill the blank PDF form with the fetched data and verify.

Requires: PyMuPDF (pymupdf)
"""

import pymupdf
import os
import json
import time
import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo_output")


# ═════════════════════════════════════════════════════════════════════════════
# CONSTANTS — Layout & Style
# ═════════════════════════════════════════════════════════════════════════════
PAGE_W, PAGE_H = 612, 792  # US Letter
MARGIN_L, MARGIN_R, MARGIN_T, MARGIN_B = 50, 50, 50, 50
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R

# Color palette
CLR_PRIMARY = (0.11, 0.22, 0.55)      # deep navy
CLR_SECONDARY = (0.30, 0.30, 0.30)    # dark grey
CLR_ACCENT = (0.85, 0.12, 0.12)       # red accent
CLR_LINE = (0.60, 0.60, 0.60)         # field underline
CLR_BG_HEADER = (0.92, 0.94, 0.98)    # light blue-grey
CLR_LABEL = (0.20, 0.20, 0.20)
CLR_VALUE = (0.05, 0.05, 0.50)        # blue-black for filled values


# ═════════════════════════════════════════════════════════════════════════════
# FIELD DEFINITIONS — Structured form layout
# ═════════════════════════════════════════════════════════════════════════════
FORM_SECTIONS = [
    {
        "title": "PERSONAL INFORMATION",
        "icon": "👤",
        "fields": [
            ("first_name",      "First Name"),
            ("middle_name",     "Middle Name"),
            ("last_name",       "Last Name"),
            ("date_of_birth",   "Date of Birth"),
            ("gender",          "Gender"),
            ("marital_status",  "Marital Status"),
            ("nationality",     "Nationality"),
        ],
    },
    {
        "title": "CONTACT INFORMATION",
        "icon": "📞",
        "fields": [
            ("email",           "Email Address"),
            ("phone",           "Phone Number"),
            ("alt_phone",       "Alternate Phone"),
            ("street_address",  "Street Address"),
            ("apt_suite",       "Apt / Suite"),
            ("city",            "City"),
            ("state",           "State"),
            ("zip_code",        "ZIP Code"),
            ("country",         "Country"),
        ],
    },
    {
        "title": "EMPLOYMENT DETAILS",
        "icon": "💼",
        "fields": [
            ("employer_name",   "Employer Name"),
            ("job_title",       "Job Title"),
            ("department",      "Department"),
            ("employee_id",     "Employee ID"),
            ("start_date",      "Start Date"),
            ("annual_salary",   "Annual Salary"),
            ("work_phone",      "Work Phone"),
            ("work_email",      "Work Email"),
        ],
    },
    {
        "title": "EMERGENCY CONTACT",
        "icon": "🚨",
        "fields": [
            ("emergency_name",         "Full Name"),
            ("emergency_relationship", "Relationship"),
            ("emergency_phone",        "Phone"),
            ("emergency_email",        "Email"),
        ],
    },
    {
        "title": "GOVERNMENT IDENTIFICATION",
        "icon": "🛂",
        "fields": [
            ("ssn",                "Social Security Number"),
            ("drivers_license",    "Driver License #"),
            ("dl_state",           "DL Issuing State"),
            ("passport_number",    "Passport Number"),
        ],
    },
]


# ═════════════════════════════════════════════════════════════════════════════
# PHASE 1 — Generate the blank PDF form
# ═════════════════════════════════════════════════════════════════════════════

def _draw_header(page, shape):
    """Draw a branded header bar at the top of the page."""
    # Full-width header background
    shape.draw_rect(pymupdf.Rect(0, 0, PAGE_W, 68))
    shape.finish(fill=CLR_PRIMARY)

    # Organisation name
    page.insert_text(
        (MARGIN_L, 30),
        "ACME CORPORATION",
        fontsize=16, fontname="hebo", color=(1, 1, 1),
    )
    # Form title
    page.insert_text(
        (MARGIN_L, 52),
        "Personal Information Form  —  Confidential",
        fontsize=10, fontname="helv", color=(0.75, 0.82, 1.0),
    )
    # Date badge
    page.insert_text(
        (PAGE_W - MARGIN_R - 140, 30),
        f"Date: {datetime.date.today().isoformat()}",
        fontsize=9, fontname="helv", color=(0.85, 0.90, 1.0),
    )
    # Thin accent line under header
    shape.draw_line((0, 68), (PAGE_W, 68))
    shape.finish(color=CLR_ACCENT, width=2)


def _draw_footer(page, shape, page_num, total_pages):
    """Draw a footer with page number and disclaimer."""
    y = PAGE_H - 30
    shape.draw_line((MARGIN_L, y - 10), (PAGE_W - MARGIN_R, y - 10))
    shape.finish(color=CLR_LINE, width=0.5)
    page.insert_text(
        (MARGIN_L, y),
        "CONFIDENTIAL — For authorized use only.",
        fontsize=7, fontname="helv", color=CLR_SECONDARY,
    )
    page.insert_text(
        (PAGE_W - MARGIN_R - 70, y),
        f"Page {page_num} of {total_pages}",
        fontsize=8, fontname="helv", color=CLR_SECONDARY,
    )


def _draw_section_header(page, shape, y, title):
    """Draw a section header band and return the new y position."""
    band_h = 24
    # Background band
    shape.draw_rect(pymupdf.Rect(MARGIN_L - 5, y, PAGE_W - MARGIN_R + 5, y + band_h))
    shape.finish(fill=CLR_BG_HEADER, color=CLR_PRIMARY, width=0.5)
    # Section title
    page.insert_text(
        (MARGIN_L + 4, y + 17),
        title,
        fontsize=11, fontname="hebo", color=CLR_PRIMARY,
    )
    return y + band_h + 10


def _draw_field_row(page, shape, y, label, field_key, field_positions):
    """Draw a single label + underline row, return the new y position."""
    row_h = 28
    label_text = f"{label}:"
    page.insert_text(
        (MARGIN_L + 10, y + 14),
        label_text,
        fontsize=10, fontname="hebo", color=CLR_LABEL,
    )

    # Value underline
    value_x_start = MARGIN_L + 180
    value_x_end = PAGE_W - MARGIN_R - 10
    line_y = y + 16
    shape.draw_line((value_x_start, line_y), (value_x_end, line_y))
    shape.finish(color=CLR_LINE, width=0.5, dashes="[3 2]")

    # Record position for Phase 3
    field_positions[field_key] = {
        "x": value_x_start + 2,
        "y": y + 14,
        "page": -1,  # will be set later
    }

    return y + row_h


def generate_blank_form():
    """
    PHASE 1: Create a professional multi-page PDF form with ~30 labelled fields.
    Returns the field_positions dict mapping field_key → {x, y, page}.
    """
    print("=" * 65)
    print("  PHASE 1 — Generating Blank Personal Information Form")
    print("=" * 65)

    doc = pymupdf.open()
    field_positions = {}

    # --- Pre-calculate pagination ---
    # We'll draw everything on pages, starting a new page when space runs out.
    current_page = None
    shape = None
    page_num = 0
    y = 0

    def new_page():
        nonlocal current_page, shape, page_num, y
        page_num += 1
        current_page = doc.new_page(width=PAGE_W, height=PAGE_H)
        shape = current_page.new_shape()
        _draw_header(current_page, shape)
        y = 90  # below header

    def finalize_page():
        if shape is not None:
            shape.commit()

    new_page()

    for sec_idx, section in enumerate(FORM_SECTIONS):
        # Check if there's room for at least the header + 2 rows
        needed = 24 + 10 + len(section["fields"]) * 28 + 20
        if y + needed > PAGE_H - MARGIN_B - 40:
            finalize_page()
            new_page()

        y = _draw_section_header(current_page, shape, y, section["title"])

        for field_key, label in section["fields"]:
            if y + 28 > PAGE_H - MARGIN_B - 40:
                finalize_page()
                new_page()
                y = _draw_section_header(current_page, shape, y, section["title"] + " (cont.)")

            y = _draw_field_row(current_page, shape, y, label, field_key, field_positions)
            field_positions[field_key]["page"] = page_num - 1  # 0-indexed

        y += 12  # gap between sections

    # --- Signature block on the last page ---
    if y + 100 > PAGE_H - MARGIN_B - 40:
        finalize_page()
        new_page()

    y += 20
    page.insert_text if False else None  # placeholder
    current_page.insert_text(
        (MARGIN_L + 10, y),
        "APPLICANT SIGNATURE",
        fontsize=11, fontname="hebo", color=CLR_PRIMARY,
    )
    y += 30
    shape.draw_line((MARGIN_L + 10, y), (MARGIN_L + 250, y))
    shape.finish(color=(0.2, 0.2, 0.2), width=1)
    current_page.insert_text(
        (MARGIN_L + 10, y + 15),
        "Signature",
        fontsize=8, fontname="helv", color=CLR_SECONDARY,
    )
    shape.draw_line((MARGIN_L + 300, y), (PAGE_W - MARGIN_R - 10, y))
    shape.finish(color=(0.2, 0.2, 0.2), width=1)
    current_page.insert_text(
        (MARGIN_L + 300, y + 15),
        "Date",
        fontsize=8, fontname="helv", color=CLR_SECONDARY,
    )

    # Finalize all pages with footers
    finalize_page()
    total_pages = len(doc)
    for i, pg in enumerate(doc):
        s = pg.new_shape()
        _draw_footer(pg, s, i + 1, total_pages)
        s.commit()

    # Save
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    blank_path = os.path.join(OUTPUT_DIR, "form_blank.pdf")
    doc.save(blank_path)
    doc.close()

    total_fields = sum(len(s["fields"]) for s in FORM_SECTIONS)
    print(f"  ✓ Created blank form  : {blank_path}")
    print(f"    → {total_pages} page(s), {total_fields} fields across {len(FORM_SECTIONS)} sections")
    print()

    return field_positions, blank_path


# ═════════════════════════════════════════════════════════════════════════════
# PHASE 2 — Mock Database API Call
# ═════════════════════════════════════════════════════════════════════════════

def mock_api_fetch_person():
    """
    PHASE 2: Simulate an API endpoint that queries a database and returns
    a JSON object with all personal-information fields populated.
    """
    print("=" * 65)
    print("  PHASE 2 — Mock API Call: Fetching Person Record from Database")
    print("=" * 65)

    # --- Simulate realistic latency & logging ---
    print("  ┌─ Connecting to database server db-primary.acme.internal:5432 ...")
    time.sleep(0.4)
    print("  │  ✓ TLS handshake complete")

    print("  │  Authenticating service account 'svc_form_filler' ...")
    time.sleep(0.3)
    print("  │  ✓ Authenticated  (token expires in 3600s)")

    print("  │  Executing query:")
    print("  │    SELECT * FROM persons WHERE person_id = 'P-2024-08193'")
    time.sleep(0.5)
    print("  │  ✓ Query returned 1 row in 47ms")

    print("  │  Serializing to JSON ...")
    time.sleep(0.2)
    print("  └─ ✓ API response ready")
    print()

    # --- The mock "response" payload ---
    person = {
        # Personal
        "first_name":       "Alexander",
        "middle_name":      "James",
        "last_name":        "Whitfield",
        "date_of_birth":    "03/15/1988",
        "gender":           "Male",
        "marital_status":   "Married",
        "nationality":      "United States",

        # Contact
        "email":            "a.whitfield@email.com",
        "phone":            "(415) 555-0173",
        "alt_phone":        "(415) 555-0299",
        "street_address":   "1842 Maple Ridge Drive",
        "apt_suite":        "Suite 4B",
        "city":             "San Francisco",
        "state":            "California",
        "zip_code":         "94122",
        "country":          "United States",

        # Employment
        "employer_name":    "Acme Corporation",
        "job_title":        "Senior Software Engineer",
        "department":       "Platform Engineering",
        "employee_id":      "EMP-2024-08193",
        "start_date":       "01/10/2020",
        "annual_salary":    "$185,000",
        "work_phone":       "(415) 555-8000 x4421",
        "work_email":       "awhitfield@acme.com",

        # Emergency Contact
        "emergency_name":           "Sophia Whitfield",
        "emergency_relationship":   "Spouse",
        "emergency_phone":          "(415) 555-0174",
        "emergency_email":          "sophia.w@email.com",

        # Government IDs
        "ssn":              "***-**-6789",
        "drivers_license":  "D8834921",
        "dl_state":         "California",
        "passport_number":  "X12345678",
    }

    # Save a copy as a JSON file
    json_path = os.path.join(OUTPUT_DIR, "api_response.json")
    with open(json_path, "w") as f:
        json.dump({"status": "ok", "person_id": "P-2024-08193", "data": person}, f, indent=2)

    print(f"  ✓ Saved API response  : {json_path}")
    print(f"    → {len(person)} fields returned for person_id P-2024-08193")
    print()

    return person


# ═════════════════════════════════════════════════════════════════════════════
# PHASE 3 — Fill the PDF Form with API Data
# ═════════════════════════════════════════════════════════════════════════════

def fill_form(blank_pdf_path, field_positions, person_data):
    """
    PHASE 3: Open the blank form, overlay text values at the recorded
    field positions, save the filled copy, and verify.
    """
    print("=" * 65)
    print("  PHASE 3 — Filling PDF Form with Database Record")
    print("=" * 65)

    doc = pymupdf.open(blank_pdf_path)
    filled_count = 0

    for field_key, pos in field_positions.items():
        value = person_data.get(field_key, "")
        if not value:
            continue

        page = doc[pos["page"]]
        page.insert_text(
            (pos["x"], pos["y"]),
            str(value),
            fontsize=10,
            fontname="helv",
            color=CLR_VALUE,
        )
        filled_count += 1

    filled_path = os.path.join(OUTPUT_DIR, "form_filled.pdf")
    doc.save(filled_path)
    doc.close()

    print(f"  ✓ Filled {filled_count}/{len(field_positions)} fields")
    print(f"  ✓ Saved filled form   : {filled_path}")

    # --- Verification: extract text and confirm values present ---
    print()
    print("  ── Verification ──")
    doc = pymupdf.open(filled_path)
    all_text = ""
    for pg in doc:
        all_text += pg.get_text()
    doc.close()

    verified = 0
    missing = []
    for field_key, value in person_data.items():
        if value in all_text:
            verified += 1
        else:
            missing.append(field_key)

    print(f"  ✓ Verified {verified}/{len(person_data)} field values found in extracted text")
    if missing:
        print(f"  ⚠ Could not verify: {', '.join(missing)}")
    else:
        print(f"  ✓ All values confirmed present in the filled PDF!")
    print()

    return filled_path


# ═════════════════════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════════════════════

def main():
    print()
    print("╔" + "═" * 63 + "╗")
    print("║" + "  PDF Form Fill Workflow".center(63) + "║")
    print("║" + "  Generate → Fetch → Fill → Verify".center(63) + "║")
    print("╚" + "═" * 63 + "╝")
    print()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Phase 1
    field_positions, blank_path = generate_blank_form()

    # Phase 2
    person_data = mock_api_fetch_person()

    # Phase 3
    filled_path = fill_form(blank_path, field_positions, person_data)

    # Summary
    print("═" * 65)
    print("  WORKFLOW COMPLETE")
    print("═" * 65)
    print(f"  Blank form  : {blank_path}")
    print(f"  API response: {os.path.join(OUTPUT_DIR, 'api_response.json')}")
    print(f"  Filled form : {filled_path}")
    print()


if __name__ == "__main__":
    main()
