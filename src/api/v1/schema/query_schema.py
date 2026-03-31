from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class QueryRequest(BaseModel):
    query : str = Field(..., example="What is the minimum CIBIL score for personal loans?")
    #loan_product: str = Field(..., example="Home Loan,Personal Loan") 

class QueryResponse(BaseModel):
    query : str
    answer : str
    policy_citations : str
    page_no : str
    document_name : str 
