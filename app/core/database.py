from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Usando SQLite para desenvolvimento inicial. O arquivo "financas.db" será criado na raiz.
SQLALCHEMY_DATABASE_URL = "sqlite:///./financas.db"

# O connect_args é necessário apenas para SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()