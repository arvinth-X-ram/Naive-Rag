from sqlalchemy import Column, Integer, String, Float, Boolean
from src.core.db import Base

class Client(Base):
    __tablename__ = "client_db"
    id = Column(String(20), primary_key=True, index=True)
    
    loan_product = Column(String(50), nullable=False)
    loan_amount = Column(Integer, nullable=False)
    tenor_months = Column(Integer, nullable=False)
    
    cibil_score = Column(Integer, nullable=False)
    monthly_income = Column(Integer, nullable=False)
    existing_liabilities = Column(Integer, default=0)
    
    collateral_offered = Column(Boolean, default=False)
    employment_type = Column(String(30), nullable=False)