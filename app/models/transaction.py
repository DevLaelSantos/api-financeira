from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    amount = Column(Float, nullable=False) # Positivo para receita, negativo para despesa
    category = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Chave estrangeira ligando ao usuário
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Relacionamento para acessar o usuário a partir da transação
    owner = relationship("User")