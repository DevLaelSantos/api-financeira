from fastapi import FastAPI
from app.api.v1 import health
from app.core.config import settings

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