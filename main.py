import os
import re
import shutil
from fastapi import FastAPI,UploadFile,HTTPException,File
from pdf_utils import extract_text_from_pdf
from chunking import chunk_text
from embedding import embed_texts_batched
from vectorstore import store_chunks

app = FastAPI(name="Chat with your pdf")
UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR,exist_ok=True)



def safe_collection_name(filename: str) -> str:
    # Chroma collection names must be alphanumeric + - _ , no spaces/dots
    name = re.sub(r"[^a-zA-Z0-9_-]", "_", filename)
    return name[:60]


@app.get("/health")
def health_check():
    return {"status" : "ok"}


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, details = "Only Pdfs are allowed")
    

    file_path = os.path.join(UPLOAD_DIR,file.filename)

    with open(file_path , "wb") as buffer:
        shutil.copyfileobj(file.file,buffer)

    return {
        "filename" : file.filename,
        "saved_path" : file_path,
        "message": "File uploaded successfully"
    }

@app.post("/extract")

async def extract_pdf(filename : str):
    file_path = os.path.join(UPLOAD_DIR,filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found. Upload it first.")
    
    pages = extract_text_from_pdf(file_path)


    return {
        "filename": filename,
        "total_pages_with_text": len(pages),
        "preview": pages[0] if pages else None
    }


@app.post("/chunk")
async def chunk_pdf(filename:str) :
    file_path = os.path.join(UPLOAD_DIR,filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found. Upload it first.")
    


    pages = extract_text_from_pdf(file_path)
    chunks = chunk_text(pages)

    return {
        "filename" : filename,
        "total_chunks": len(chunks),
        "sample_chunks": chunks[:3]
    }

    

@app.post('/process')
async def process_pdf(filename:str):
    file_path = os.path.join(UPLOAD_DIR,filename)

    if not os.path.exists(file_path):
        return HTTPException(status_code=404,detail="File not found. Upload it first.")
    
    pages = extract_text_from_pdf(file_path)
    chunks = chunk_text(pages)

    if not chunks:
        raise HTTPException(status_code=400, detail="No extractable text found in this PDF.")

    texts = [c["text"] for c in chunks]
    vectors = embed_texts_batched(texts)

    collection_name = safe_collection_name(filename=filename)
    total_stored = store_chunks(collection_name,chunks,vectors)

    return {
       "filename": filename,
       "collection_name": collection_name,
       "total_chunks_stored": total_stored
    }






