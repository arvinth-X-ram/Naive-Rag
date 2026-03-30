from fastapi import APIRouter, Depends, HTTPException
from src.core.db import get_vector_store,get_db
from src.api.v1.schema.query_schema import QueryRequest,QueryResponse,ClientCreate
from src.api.v1.agents.agents import agents
from sqlalchemy.orm import Session
from src.api.v1.model.model import Client
from src.api.v1.schema.query_schema import QueryRequest,QueryResponse,ClientCreate


def credit_assess_db(request: ClientCreate, db: Session):
    new_p = Client(**request.model_dump())
    db.add(new_p)
    db.commit()
    db.refresh(new_p)
    return new_p

def get_profile_db(profile_id: str, db: Session):
    profile = db.query(Client).filter(Client.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
