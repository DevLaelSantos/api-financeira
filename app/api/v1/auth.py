from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import SessionLocal
from app.models.user import User
from app.models.transaction import Transaction # Importante para o delete
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.core.security import gerar_hash_senha, verificar_senha, criar_token_acesso
from app.core.deps import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# ROTAS DE AUTENTICAÇÃO
# ==========================================

@router.post("/register", response_model=UserResponse, summary="Registrar novo usuário")
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário no sistema.
    
    - **email**: E-mail único do usuário.
    - **password**: Senha que será criptografada (mínimo 8 caracteres).
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    
    hashed_password = gerar_hash_senha(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", summary="Login do usuário")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Autentica o usuário e retorna um token JWT.
    
    - **username**: E-mail do usuário.
    - **password**: Senha do usuário.
    """
    db_user = db.query(User).filter(User.email == form_data.username).first()
    if not db_user or not verificar_senha(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos"
        )

        # ... dentro do login, após verificar a senha ...
    if not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sua conta está pendente de aprovação ou foi desativada. Entre em contato com o suporte."
        )
    
    access_token = criar_token_acesso(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# ==========================================
# ROTAS DE GESTÃO DE CONTA (SELF-SERVICE)
# ==========================================

@router.get("/me", response_model=UserResponse, summary="Obter dados do usuário logado")
def get_me(current_user: User = Depends(get_current_user)):
    """
    Retorna os dados do usuário autenticado no momento.
    
    Útil para preencher formulários de perfil no Frontend.
    """
    return current_user

@router.put("/me", response_model=UserResponse, summary="Atualizar dados do usuário logado")
def update_me(
    user_update: UserUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza o e-mail ou a senha do usuário logado.
    
    - **email**: (Opcional) Novo e-mail. Deve ser único.
    - **password**: (Opcional) Nova senha. Será criptografada.
    """
    # Busca o usuário na sessão ativa para evitar erro de "detached instance"
    db_user = db.query(User).filter(User.id == current_user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    if user_update.email and user_update.email != db_user.email:
        existing = db.query(User).filter(User.email == user_update.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="E-mail já cadastrado por outro usuário.")
        db_user.email = user_update.email

    if user_update.password:
        db_user.hashed_password = gerar_hash_senha(user_update.password)

    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT, summary="Excluir conta do usuário logado")
def delete_me(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Exclui permanentemente a conta do usuário logado e todas as suas transações.
    
    ⚠️ **Atenção**: Esta ação é irreversível.
    """
    # Exclui as transações primeiro para evitar erro de chave estrangeira
    db.query(Transaction).filter(Transaction.owner_id == current_user.id).delete()
    db.delete(current_user)
    db.commit()
    return None