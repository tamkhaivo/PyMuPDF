import pymupdf

def main():
    # Define output filename
    filename = "example.pdf"
    
    # ---------------------------------------------------------
    # Creation Step: Create a new PDF and add some content
    # ---------------------------------------------------------
    print(f"Creating {filename}...")
    doc = pymupdf.open()  # new empty document
    page = doc.new_page()  # new page in the document
    
    # Insert text
    # Point(50, 72) is where the text starts (72 points = 1 inch)
    page.insert_text((50, 72), "Hello PyMuPDF!", fontsize=24)
    page.insert_text((50, 100), "This is a demo showing how to create and read PDFs.", fontsize=12)
    
    # Save the document
    doc.save(filename)
    doc.close()
    print(f"Successfully saved {filename}")
    print("-" * 30)

    # ---------------------------------------------------------
    # Reading Step: Open the PDF and read content (from README)
    # ---------------------------------------------------------
    print(f"Reading {filename}...")
    
    try:
        doc = pymupdf.open(filename) # open a document
        for page_num, page in enumerate(doc): # iterate the document pages
            text = page.get_text() # get plain text encoded as UTF-8
            print(f"Page {page_num + 1} content:")
            print(text)
    except Exception as e:
        print(f"Error reading {filename}: {e}")

if __name__ == "__main__":
    main()
