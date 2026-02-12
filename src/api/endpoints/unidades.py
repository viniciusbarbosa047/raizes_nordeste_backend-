from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.infrastructure.banco_de_dados import get_db
from src.domain.modelos import Unidade, Usuario
from src.domain.schemas import UnidadeCriar, UnidadeLer
from src.api.deps import obter_usuario_logado 
router = APIRouter()

# ROTA PROTEGIDA 🔒
# Note o novo argumento: usuario_atual: Usuario = Depends(obter_usuario_logado)
# Isso obriga a ter token pra entrar aqui.
@router.post("/", response_model=UnidadeLer, status_code=status.HTTP_201_CREATED)
def criar_nova_unidade(
    unidade: UnidadeCriar, 
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_logado) 
):
    print(f"Usuario autorizado: {usuario_atual.nome} está criando uma loja.")
    
    unidade_existente = db.query(Unidade).filter(Unidade.nome == unidade.nome).first()
    if unidade_existente:
        raise HTTPException(status_code=409, detail="Unidade já existe.")

    try:
        nova_loja = Unidade(nome=unidade.nome, tem_cozinha=unidade.tem_cozinha)
        db.add(nova_loja)
        db.commit()
        db.refresh(nova_loja)
        return nova_loja
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro interno.")

# ROTA PÚBLICA 🔓 (Qualquer um vê)
@router.get("/", response_model=list[UnidadeLer])
def listar_unidades(db: Session = Depends(get_db)):
    return db.query(Unidade).all()