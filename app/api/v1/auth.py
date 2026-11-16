from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate # <-- Adicionado o UserUpdate
from app.core.security import gerar_hash_senha, verificar_senha, criar_token_acesso
from app.core.deps import get_current_user # <-- Import o get_current_user
from app.models.transaction import Transaction

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# * Rota de Registrar
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    
    hashed_password = gerar_hash_senha(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# * Rota de Login
# A MUDANÇA ESTÁ AQUI: Agora o login aceita formulário (para o Swagger) ou JSON
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), # <-- Adicionado para o Swagger
    db: Session = Depends(get_db)
):
    # O Swagger envia o e-mail no campo "username"
    db_user = db.query(User).filter(User.email == form_data.username).first()
    
    if not db_user or not verificar_senha(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos"
        )
    
    access_token = criar_token_acesso(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# * Rota Listagem de Usuario Logado
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Retorna os dados do usuário logado."""
    return current_user

# * Rota Update -> Atualiza Usuario
@router.put("/me", response_model=UserResponse)
def update_me(
    user_update: UserUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # 1. Busca o usuário NOVAMENTE na sessão ativa do banco
    db_user = db.query(User).filter(User.id == current_user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    # 2. Verifica se o novo e-mail já está em uso
    if user_update.email and user_update.email != db_user.email:
        existing = db.query(User).filter(User.email == user_update.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="E-mail já cadastrado por outro usuário.")
        db_user.email = user_update.email

    # 3. Atualiza a senha
    if user_update.password:
        db_user.hashed_password = gerar_hash_senha(user_update.password)

    # 4. Salva as alterações
    db.commit()
    db.refresh(db_user)
    return db_user

# * Rota Delete Usuario
@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_me(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Exclui a conta do usuário logado e todas as suas transações."""
    # Exclui todas as transações do usuário primeiro (para evitar erro de chave estrangeira)
    db.query(Transaction).filter(Transaction.owner_id == current_user.id).delete()
    
    # Exclui o usuário
    db.delete(current_user)
    db.commit()
    return None
