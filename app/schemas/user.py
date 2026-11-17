from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Schema base (dados que vêm na requisição)
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="A senha deve ter no mínimo 8 caracteres")

# Schema de resposta (o que a API devolve, SEM a senha)
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_admin: bool
    plan: str
    created_at: datetime # <-- NOVO CAMPO

    class Config:
        from_attributes = True # Permite ler dados do SQLAlchemy

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, description="A senha deve ter no mínimo 8 caracteres")