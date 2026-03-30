from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class QueryRequest(BaseModel):
    query: str = Field(...,description = "User query")
    # k:int = Field(default=5, ge=1, le=20, description="Top-k results")
    category: Optional[str] = Field(
        default = None,
        description="Optional metadata filter (e,g., hr_support_desk)"
    )

class QueryResult(BaseModel):
    content: str
    metadata: Dict[str,Any]

# class QueryResponse(BaseModel):
#     query: str
#     result:List[QueryResult]

class QueryResponse(BaseModel):
    query: str
    result:str


class ClientCreate(BaseModel):
    id: str
    loan_product: str
    loan_amount: int
    tenor_months: int
    cibil_score: int
    monthly_income: int
    existing_liabilities: Optional[int] = 0
    collateral_offered: bool = False
    employment_type: str