from pydantic import BaseModel, Field
from datetime import datetime

class TransactionCreate(BaseModel):
    description: str = Field(..., min_length=3)
    amount: float = Field(..., description="Valor positivo para receita, negativo para despesa")
    category: str

class TransactionResponse(BaseModel):
    id: int
    description: str
    amount: float
    category: str
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True