def chunk_text(pages:list[dict],chunk_size:int = 1000, overlap :int = 150)-> list[dict]:
    """
    Splits page-level text into overlapping chunks.
    chunk_size and overlap are in characters (simple and good enough to start).

    Returns: list of {"chunk_id": int, "page": page_number, "text": chunk_text}
    """

    chunks = []
    chunk_id = 0
    MAX_CHUNKS = 5000  # safety cap so a pathological PDF can't run away

    for page_data in pages:
        page_num = page_data["page"]
        text = page_data["text"]

        start = 0
        while start < len(text):
            if len(chunks) >= MAX_CHUNKS:
                return chunks  # bail out instead of growing forever

            end = start + chunk_size
            chunk = text[start:end].strip()

            if chunk:
                chunks.append({
                    "chunk_id": chunk_id,
                    "page": page_num,
                    "text": chunk
                })
                chunk_id += 1

            start += chunk_size - overlap

    return chunks


