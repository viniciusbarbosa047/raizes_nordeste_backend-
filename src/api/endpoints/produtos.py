from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.banco_de_dados import get_db
from src.domain.modelos import Produto
from src.domain.schemas import ProdutoCriar, ProdutoLer

router = APIRouter()

# POST - Cadastra produto COM ESTOQUE
@router.post("/", response_model=ProdutoLer, status_code=status.HTTP_201_CREATED)
def criar_produto(produto: ProdutoCriar, db: Session = Depends(get_db)):
    # 1. Validação de Duplicidade
    produto_existente = db.query(Produto).filter(Produto.nome == produto.nome).first()
    
    if produto_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"O produto '{produto.nome}' já está cadastrado."
        )

    try:
        # 2. Criação (Agora salvando o estoque!)
        novo_produto = Produto(
            nome=produto.nome,
            categoria=produto.categoria,
            preco=produto.preco,
            estoque=produto.estoque # <--- ESSA LINHA FALTAVA!
        )
        db.add(novo_produto)
        db.commit()
        db.refresh(novo_produto)
        return novo_produto

    except Exception as e:
        db.rollback()
        print(f"Erro ao inserir produto: {e}")
        raise HTTPException(status_code=500, detail="Erro interno.")

@router.get("/", response_model=list[ProdutoLer])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(Produto).all()