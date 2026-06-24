import os
import shutil
from fastapi import FastAPI,UploadFile,HTTPException,File
from pdf_utils import extract_text_from_pdf

app = FastAPI(name="Chat with your pdf")
UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR,exist_ok=True)


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
    









