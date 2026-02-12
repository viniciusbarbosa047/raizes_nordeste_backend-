import bcrypt

# Funcao 1: Verificar se a senha esta certa
def verificar_senha(senha_pura: str, senha_criptografada: str) -> bool:
    """
    Compara a senha que o usuario digitou (ex: '123456') 
    com o hash salvo no banco.
    """
    # Precisamos converter texto para bytes antes de verificar
    senha_bytes = senha_pura.encode('utf-8')
    hash_bytes = senha_criptografada.encode('utf-8')
    
    return bcrypt.checkpw(senha_bytes, hash_bytes)

# Funcao 2: Gerar o Hash (Criptografar)
def gerar_hash_senha(senha: str) -> str:
    """
    Cria uma senha criptografada segura.
    """
    senha_bytes = senha.encode('utf-8')
    salt = bcrypt.gensalt() # Gera um 'tempero' aleatorio
    hash_bytes = bcrypt.hashpw(senha_bytes, salt)
    
    return hash_bytes.decode('utf-8') # Devolve como texto pra salvar no banco