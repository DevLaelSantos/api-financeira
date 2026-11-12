from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate

class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, transaction: TransactionCreate, user_id: int) -> Transaction:
        db_transaction = Transaction(
            description=transaction.description,
            amount=transaction.amount,
            category=transaction.category,
            owner_id=user_id
        )
        self.db.add(db_transaction)
        self.db.commit()
        self.db.refresh(db_transaction)
        return db_transaction

    def get_by_user(self, user_id: int):
        return self.db.query(Transaction).filter(Transaction.owner_id == user_id).all()