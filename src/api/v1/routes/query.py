from fastapi import APIRouter, Depends
from src.core.db import get_vector_store,get_db
from src.api.v1.schema.query_schema import QueryRequest,QueryResponse,ClientCreate
from src.api.v1.agents.agents import agents
from sqlalchemy.orm import Session
from src.api.v1.services.db_service import credit_assess_db, get_profile_db


router = APIRouter()

@router.post("/query",response_model=QueryResponse)
def query_endpoint(request: QueryRequest):

    docs = agents(request.query)
    return{
        'query':request.query,
        # 'result':[
        #     {
        #         'content':doc.page_content,
        #         'metadata':doc.metadata,
        #     }
        #     for doc in docs
        # ]      
        'result': docs["messages"][-1].text
    }

@router.post("/credit/assess")
def credit_assess(request: ClientCreate, db: Session = Depends(get_db)):
    new_p = credit_assess_db(request,db)
    return new_p

@router.get("/credit/{profile_id}")
def get_profile(profile_id: str, db: Session = Depends(get_db)):
    return get_profile_db(profile_id,db)
