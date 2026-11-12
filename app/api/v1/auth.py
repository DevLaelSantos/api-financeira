from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import gerar_hash_senha, verificar_senha, criar_token_acesso

router = APIRouter()

# Dependência para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Verifica se o e-mail já existe
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    
    # Criptografa a senha e cria o usuário
    hashed_password = gerar_hash_senha(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verificar_senha(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos"
        )
    
    # Gera o token JWT
    access_token = criar_token_acesso(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}