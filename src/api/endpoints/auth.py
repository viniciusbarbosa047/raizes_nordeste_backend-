from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.infrastructure.banco_de_dados import get_db
from src.domain.modelos import Usuario
from src.core.seguranca import verificar_senha, criar_token_acesso

router = APIRouter()

@router.post("/login")
def login_para_pegar_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Rota oficial de Login.
    Recebe 'username' (email) e 'password'.
    Retorna o Token de Acesso (Bearer Token).
    """
    print(f"Tentativa de login: {form_data.username}")

    # 1. Busca o usuário pelo email
    # O FastAPI chama o campo de email de 'username' por padrão
    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()

    # 2. Se usuário não existe ou a senha está errada...
    if not usuario or not verificar_senha(form_data.password, usuario.senha_hash):
        print("Login falhou: Email ou senha incorretos")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Se tudo deu certo, gera o Token (O Crachá)
    token_acesso = criar_token_acesso(dados_do_usuario={"sub": usuario.email})
    
    print(f"Login SUCESSO! Token gerado para {usuario.nome}")
    return {"access_token": token_acesso, "token_type": "bearer"}