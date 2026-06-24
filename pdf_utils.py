import fitz  

def extract_text_from_pdf(file_path: str) -> list[dict]:
    """
    Returns a list of {"page": page_number, "text": page_text}
    one entry per page, skipping empty pages.
    """
    doc = fitz.open(file_path)
    pages = []

    for page_num,page in enumerate(doc,start=1):
        page_text = page.get_text().strip()

        if page_text:
            pages.append({
                "page" :page_num,
                "text" : page_text
            })

    doc.close()
    return pages













