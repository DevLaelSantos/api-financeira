import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "API Financeira"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    # Adicionaremos SECRET_KEY para JWT na Sprint 2

settings = Settings()