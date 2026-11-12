from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.repositories.transaction_repository import TransactionRepository

router = APIRouter()

@router.post("/", response_model=TransactionResponse)
def create_transaction(
    transaction: TransactionCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    repo = TransactionRepository(db)
    return repo.create(transaction, current_user.id)

@router.get("/", response_model=List[TransactionResponse])
def list_transactions(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    repo = TransactionRepository(db)
    return repo.get_by_user(current_user.id)