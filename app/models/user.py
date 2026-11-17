from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.core.database import Base
from datetime import datetime  # <-- Deixe apenas esta (apague a outra)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False) # <-- ADMIN
    plan = Column(String, default="free") # --- planos de assinatura
    created_at = Column(DateTime, default=datetime.utcnow)