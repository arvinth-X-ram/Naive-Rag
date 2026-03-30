from fastapi import FastAPI
from src.api.v1.routes.query import router as rag_router

app = FastAPI(title="NAIVE RAG API")

app.include_router(rag_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "API v1 is active"}
