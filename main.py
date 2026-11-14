from fastapi import FastAPI
from app.api.v1 import health, auth # Importa as rotas
from app.core.config import settings
from app.core.database import engine, Base
from app.models import user, transaction # Importa os modelos para o SQLAlchemy reconhecer
from app.api.v1 import health, auth, transactions # Adicione o transactions
from fastapi.middleware.cors import CORSMiddleware
import time
from sqlalchemy.exc import OperationalError

# todo DEUBG URL DATABASE
from app.core.config import settings 

# 1. Cria a instância do FastAPI PRIMEIRO
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API para gerenciamento financeiro pessoal."
)

# --- CONFIGURAÇÃO DO CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, troque "*" pela URL do seu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ----------------------------

# 2. Cria as tabelas no banco de dados (se não existirem)
# Base.metadata.create_all(bind=engine) -> substituido

# Tenta criar as tabelas até 5 vezes, esperando 3 segundos entre as tentativas
for i in range(5):
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso!")
        break
    except OperationalError as e:
        print(f"⏳ Banco ainda não está pronto (tentativa {i+1}/5). Aguardando 3s...")
        time.sleep(3)

# 3. Registra as rotas (Agora o 'app' já existe, então não vai dar erro)
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticação"])
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["Transações"]) # Nova rota

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API Financeira. Acesse /docs para a documentação."}

@app.get("/debug")
def debug_db():
    return {"database_url": settings.DATABASE_URL}