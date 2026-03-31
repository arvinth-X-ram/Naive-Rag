import os
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, List
from src.api.v1.agents.agents import agents
from src.api.v1.schema.query_schema import QueryRequest,QueryResponse

# Import your ingestion and query utilities
from src.ingestion.ingestion import ingest_pdf
router = APIRouter()

UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# --- Upload Endpoint ---
@router.post("/admin/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Call ingestion pipeline (chunking + embedding into PGVector)
    ingest_pdf(file_path)

    return {"file": file.filename, "message": "Upload and embedding successful"}

@router.post("/query",response_model=QueryResponse)
def query_endpoint(request: QueryRequest):

    docs = agents(request.query) 

    return docs