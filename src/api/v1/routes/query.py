from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os

from src.ingestion.ingestion import ingest_pdf, get_vector_store

router = APIRouter()

UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class QueryResponse(BaseModel):
    answer: str
    results: list[str]

@router.post("/admin/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Chunk + embed PDF
    ingest_pdf(file_path)

    return {"file": file.filename, "message": "Upload and embedding successful"}
'''
@router.post("/query", response_model=QueryResponse)
async def query_docs(request: QueryRequest):
    vector_store = get_vector_store()
    if vector_store is None:
        return JSONResponse(
            status_code=400,
            content={"detail": "No PDF has been uploaded yet by admin."}
        )

    answer, results = run_query(request.query, vector_store, top_k=request.top_k)
    return {"answer": answer, "results": results}
'''
