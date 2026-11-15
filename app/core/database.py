from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os  # <-- Adicione esta linha
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ... resto do código ...
# Usando SQLite para desenvolvimento inicial. O arquivo "financas.db" será criado na raiz.
# SQLALCHEMY_DATABASE_URL = "sqlite:///./financas.db" ---- linha comentada!

# * LINHA ATUALIZADA!
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# O connect_args é necessário apenas para SQLite
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()