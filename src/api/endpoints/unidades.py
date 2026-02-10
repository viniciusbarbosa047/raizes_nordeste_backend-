from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.infrastructure.banco_de_dados import get_db
from src.domain.modelos import Unidade
from src.domain.schemas import UnidadeCriar, UnidadeLer

# Criando o roteador para as URLs de unidades
router = APIRouter()

# POST /unidades/ - Cria uma nova loja
@router.post("/", response_model=UnidadeLer)
def criar_nova_unidade(unidade: UnidadeCriar, db: Session = Depends(get_db)):
    print(f"Tentando criar a unidade: {unidade.nome}") # Print pra ajudar no debug

    # 1. Cria o objeto do banco (Model) usando os dados que vieram (Schema)
    nova_loja = Unidade(
        nome=unidade.nome,
        tem_cozinha=unidade.tem_cozinha
    )

    # 2. Adiciona no banco de dados
    db.add(nova_loja)
    
    # 3. Salva de verdade (Commit)
    db.commit()
    
    # 4. Atualiza o objeto com o ID que foi gerado
    db.refresh(nova_loja)
    
    print("Unidade salva com sucesso!")
    return nova_loja

# GET /unidades/ - Lista todas as lojas
@router.get("/", response_model=list[UnidadeLer])
def listar_unidades(db: Session = Depends(get_db)):
    # Busca tudo na tabela de unidades
    lista_de_lojas = db.query(Unidade).all()
    
    return lista_de_lojas