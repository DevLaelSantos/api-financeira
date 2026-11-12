from pydantic import BaseModel, EmailStr, Field

# Schema base (dados que vêm na requisição)
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="A senha deve ter no mínimo 8 caracteres")

# Schema de resposta (o que a API devolve, SEM a senha)
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True # Permite ler dados do SQLAlchemy