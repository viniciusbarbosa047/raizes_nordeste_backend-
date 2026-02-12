from datetime import datetime, timedelta
from jose import jwt # Biblioteca que gera o token
import bcrypt

# CONFIGURAÇÕES DO CRACHÁ
# Chave secreta (num app real, isso ficaria escondido num arquivo .env)
SECRET_KEY = "minha_chave_super_secreta_do_projeto_raizes"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # O login dura 30 minutos

# --- PARTE 1: SENHAS (JÁ FIZEMOS ANTES) ---
def verificar_senha(senha_pura: str, senha_criptografada: str) -> bool:
    senha_bytes = senha_pura.encode('utf-8')
    hash_bytes = senha_criptografada.encode('utf-8')
    return bcrypt.checkpw(senha_bytes, hash_bytes)

def gerar_hash_senha(senha: str) -> str:
    senha_bytes = senha.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(senha_bytes, salt)
    return hash_bytes.decode('utf-8')

# --- PARTE 2: TOKENS (NOVIDADE!) ---
def criar_token_acesso(dados_do_usuario: dict):
    """
    Cria um 'crachá' digital com validade de 30 minutos.
    """
    dados_para_token = dados_do_usuario.copy()
    
    # Define quando o crachá vence
    expiracao = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    dados_para_token.update({"exp": expiracao})
    
    # Carimba o crachá com a assinatura digital
    token_jwt = jwt.encode(dados_para_token, SECRET_KEY, algorithm=ALGORITHM)
    
    return token_jwt