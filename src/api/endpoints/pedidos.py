from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.infrastructure.banco_de_dados import get_db
from src.domain.modelos import Pedido, ItemPedido, Produto, Unidade
from src.domain.schemas import PedidoCriar

router = APIRouter()

# Rota para CRIAR um novo pedido
@router.post("/", status_code=201)
def criar_pedido(pedido: PedidoCriar, db: Session = Depends(get_db)):
    print(f"--- Novo Pedido Chegando via {pedido.canal_pedido} ---")

    # 1. Verifica se a Unidade existe
    loja = db.query(Unidade).filter(Unidade.id == pedido.unidade_id).first()
    if not loja:
        print("Erro: Loja nao encontrada")
        raise HTTPException(status_code=404, detail="Loja nao encontrada")
    
    valor_total_pedido = 0.0
    lista_de_itens_para_salvar = []

    # 2. Verifica cada item do pedido (Estoque e Preco)
    for item in pedido.itens:
        print(f"Verificando produto ID: {item.produto_id}")
        
        produto_banco = db.query(Produto).filter(Produto.id == item.produto_id).first()
        
        if not produto_banco:
            raise HTTPException(status_code=404, detail=f"Produto {item.produto_id} nao existe")
        
        # AQUI TA O PULO DO GATO: Verifica se tem estoque
        if produto_banco.estoque < item.quantidade:
            print(f"Erro de estoque: Pediu {item.quantidade}, so tem {produto_banco.estoque}")
            raise HTTPException(status_code=422, detail=f"Estoque insuficiente para {produto_banco.nome}")
        
        # Calcula o preco desse item
        valor_item = produto_banco.preco * item.quantidade
        valor_total_pedido += valor_item

        # Guarda na memoria pra salvar depois
        lista_de_itens_para_salvar.append({
            "produto": produto_banco,
            "quantidade": item.quantidade
        })

    # 3. Se tudo deu certo, salva no banco
    try:
        print("Tudo certo com os itens. Salvando pedido...")
        
        novo_pedido = Pedido(
            unidade_id=pedido.unidade_id,
            canal_pedido=pedido.canal_pedido,
            valor_total=valor_total_pedido,
            status="RECEBIDO"
        )
        db.add(novo_pedido)
        db.flush() # Gera o ID do pedido mas nao fecha a transacao ainda

        # Agora salva os itens e baixa o estoque
        for item_dados in lista_de_itens_para_salvar:
            prod = item_dados["produto"]
            qtd = item_dados["quantidade"]
            
            # Baixa o estoque
            prod.estoque = prod.estoque - qtd
            
            # Cria o item ligado ao pedido
            novo_item = ItemPedido(
                pedido_id=novo_pedido.id,
                produto_id=prod.id,
                quantidade=qtd
            )
            db.add(novo_item)

        db.commit() # Salva tudo de verdade
        print(f"Pedido {novo_pedido.id} criado com sucesso!")
        return {"id": novo_pedido.id, "total": valor_total_pedido, "status": "CRIADO"}

    except Exception as erro:
        db.rollback() # Se der erro, desfaz tudo
        print(f"Erro ao salvar: {erro}")
        raise HTTPException(status_code=500, detail="Erro interno ao criar pedido")