from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db, get_current_admin
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
def list_all_users(
    db: Session = Depends(get_db), 
    admin: User = Depends(get_current_admin)
):
    """Lista todos os usuários cadastrados (Apenas Admin)."""
    return db.query(User).all()

@router.delete("/users/{user_id}", status_code=204)
def delete_user_by_admin(
    user_id: int, 
    db: Session = Depends(get_db), 
    admin: User = Depends(get_current_admin)
):
    """Exclui um usuário pelo ID (Apenas Admin)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    db.delete(user)
    db.commit()
    return None