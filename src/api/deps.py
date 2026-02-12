from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from src.infrastructure.banco_de_dados import get_db
from src.core.seguranca import SECRET_KEY, ALGORITHM
from src.domain.modelos import Usuario

# Isso diz pro Swagger que o token vem de um login (cria o cadeado na tela)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def obter_usuario_logado(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Função 'Guarda'.
    Ela fica na porta das rotas protegidas.
    Se o token for falso ou vencido, ela barra o usuario.
    """
    erro_credenciais = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Tenta ler o crachá (Descriptografar o token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        
        if email is None:
            raise erro_credenciais
            
    except JWTError:
        raise erro_credenciais # Token falso ou vencido
    
    # Busca o dono do token no banco pra ter certeza que ele ainda existe
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    
    if usuario is None:
        raise erro_credenciais
        
    return usuario # Deixa passar e entrega os dados do usuário