from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.banco_de_dados import get_db
from src.domain.modelos import Produto, Usuario
from src.domain.schemas import ProdutoCriar, ProdutoLer
from src.api.deps import obter_usuario_logado

router = APIRouter()

# ROTA PROTEGIDA 🔒 (Só Admin cria produto)
@router.post("/", response_model=ProdutoLer, status_code=status.HTTP_201_CREATED)
def criar_produto(
    produto: ProdutoCriar, 
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_logado)
):
    print(f"Admin {usuario_atual.nome} está cadastrando: {produto.nome}")

    # 1. Validação de Duplicidade
    produto_existente = db.query(Produto).filter(Produto.nome == produto.nome).first()
    if produto_existente:
        raise HTTPException(status_code=409, detail="Produto já existe.")

    try:
        # 2. Criação
        novo_produto = Produto(
            nome=produto.nome,
            categoria=produto.categoria,
            preco=produto.preco,
            estoque=produto.estoque
        )
        db.add(novo_produto)
        db.commit()
        db.refresh(novo_produto)
        return novo_produto

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro interno.")

# ROTA PÚBLICA 🔓 (Cliente pode ver o cardápio sem login)
@router.get("/", response_model=list[ProdutoLer])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(Produto).all()