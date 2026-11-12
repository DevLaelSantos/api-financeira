from fastapi import FastAPI
from app.api.v1 import health, auth # Importa as rotas
from app.core.config import settings
from app.core.database import engine, Base
from app.models import user, transaction # Importa os modelos para o SQLAlchemy reconhecer

# 1. Cria a instância do FastAPI PRIMEIRO
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API para gerenciamento financeiro pessoal."
)

# 2. Cria as tabelas no banco de dados (se não existirem)
Base.metadata.create_all(bind=engine)

# 3. Registra as rotas (Agora o 'app' já existe, então não vai dar erro)
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticação"])

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API Financeira. Acesse /docs para a documentação."}