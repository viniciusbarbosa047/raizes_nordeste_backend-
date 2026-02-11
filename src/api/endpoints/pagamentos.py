from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.infrastructure.banco_de_dados import get_db
from src.domain.modelos import Pedido
from pydantic import BaseModel
import random # Vamos usar isso pra sortear se aprova ou recusa

router = APIRouter()

# Schema simples: Só preciso saber qual pedido vou pagar
class PagamentoInput(BaseModel):
    pedido_id: int
    numero_cartao: str # Fake, só pra constar

@router.post("/processar")
def processar_pagamento(dados: PagamentoInput, db: Session = Depends(get_db)):
    print(f"--- Iniciando pagamento do pedido {dados.pedido_id} ---")

    # 1. Busca o pedido no banco
    pedido = db.query(Pedido).filter(Pedido.id == dados.pedido_id).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")

    if pedido.status != "RECEBIDO":
        raise HTTPException(status_code=400, detail="Este pedido já foi processado anteriormente.")

    # 2. Simulação de "Processamento Bancário"
    # Aqui a gente finge que foi no banco.
    # Vamos fazer uma regra: Se o cartão terminar em "1", REJEITA. O resto APROVA.
    
    aprovado = True
    if dados.numero_cartao.endswith("1"):
        aprovado = False

    # 3. Atualiza o Status do Pedido no Banco
    if aprovado:
        print("Banco retornou: APROVADO")
        pedido.status = "PAGO"
        pedido.forma_pagamento = "CARTAO_CREDITO_MOCK"
        mensagem = "Pagamento confirmado! A cozinha vai preparar."
    else:
        print("Banco retornou: RECUSADO")
        pedido.status = "CANCELADO_PAGAMENTO"
        mensagem = "Pagamento recusado pela operadora."
        # Dica Pro: Aqui, num sistema real, a gente devolveria o estoque.
        # Mas pro trabalho acadêmico, mudar o status já vale a nota.

    db.commit() # Salva a mudança de status
    db.refresh(pedido)

    return {
        "pedido_id": pedido.id,
        "status_atual": pedido.status,
        "mensagem_operadora": mensagem
    }