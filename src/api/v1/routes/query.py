from fastapi import APIRouter
#, Depends
#from src.core.db import get_vector_store,get_db
from src.api.v1.schema.query_schema import QueryRequest,QueryResponse
from src.api.v1.agents.agents import agents
from sqlalchemy.orm import Session


router = APIRouter()

@router.post("/query",response_model=QueryResponse)
def query_endpoint(request: QueryRequest):

    docs = agents(request.query) 

    return docs

