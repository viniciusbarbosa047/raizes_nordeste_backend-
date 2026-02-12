from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.banco_de_dados import get_db
from src.domain.modelos import Usuario
from src.domain.schemas import UsuarioCriar, UsuarioLer
from src.core.seguranca import gerar_hash_senha 

router = APIRouter()

@router.post("/", response_model=UsuarioLer, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: UsuarioCriar, db: Session = Depends(get_db)):
    print(f"Tentando criar usuario: {usuario.email}")

    # 1. Verifica se o email já existe (Não pode ter 2 iguais)
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    # 2. Criptografa a senha (LGPD OBRIGATÓRIO)
    # Nunca salvamos a senha pura. Transformamos em hash.
    senha_segura = gerar_hash_senha(usuario.senha)

    # 3. Salva no Banco
    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=senha_segura, # Salvamos o hash, nao a senha
        perfil=usuario.perfil
    )
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    print(f"Usuario {novo_usuario.nome} criado com ID {novo_usuario.id}")
    return novo_usuario