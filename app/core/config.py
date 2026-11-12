import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "API Financeira"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./financas.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "chave_insegura_de_desenvolvimento") # <-- Adicione aqui

settings = Settings()