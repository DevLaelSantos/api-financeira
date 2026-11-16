from fastapi import APIRouter, Depends, HTTPException, status # * -> Adicionado o HTTPException e status
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.repositories.transaction_repository import TransactionRepository
from app.models.transaction import Transaction

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

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    repo = TransactionRepository(db)
    # Busca a transação para ver se ela existe e se pertence ao usuário logado
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id, 
        Transaction.owner_id == current_user.id
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Transação não encontrada ou você não tem permissão."
        )
    
    repo.delete(transaction)
    return None