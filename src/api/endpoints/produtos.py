from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.infrastructure.banco_de_dados import get_db
from src.domain.modelos import Produto
from src.domain.schemas import ProdutoCriar, ProdutoLer

# Criando o roteador de produtos
router = APIRouter()

# POST /produtos/ - Cadastra uma comida nova
@router.post("/", response_model=ProdutoLer)
def criar_produto(produto: ProdutoCriar, db: Session = Depends(get_db)):
    print(f"Tentando cadastrar o produto: {produto.nome}") # Print de teste

    # Cria o objeto Produto com os dados que vieram
    novo_produto = Produto(
        nome=produto.nome,
        categoria=produto.categoria,
        preco=produto.preco
    )

    # Adiciona e salva no banco
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    
    print(f"Produto {produto.nome} salvo com ID {novo_produto.id}")
    return novo_produto

# GET /produtos/ - Lista todo o cardápio
@router.get("/", response_model=list[ProdutoLer])
def listar_produtos(db: Session = Depends(get_db)):
    # Pega tudo da tabela de produtos
    cardapio = db.query(Produto).all()
    return cardapio