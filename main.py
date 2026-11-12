from fastapi import FastAPI
from app.api.v1 import health
from app.core.config import settings
# ... imports anteriores ...
from app.core.database import engine, Base
# Importe os modelos aqui para que o SQLAlchemy os reconheça
from app.models import user, transaction 

# Cria as tabelas no banco de dados (se não existirem)
Base.metadata.create_all(bind=engine)

# ... resto do código do main.py ...

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API para gerenciamento financeiro pessoal."
)

# Registrando as rotas
app.include_router(health.router, prefix="/api/v1", tags=["Health"])

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API Financeira. Acesse /docs para a documentação."}