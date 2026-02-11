from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- SCHEMAS (REGRAS DE DADOS) ---
# Aqui eu defino o que o usuario manda e o que ele recebe de volta.

# 1. Regras para UNIDADES
class UnidadeBase(BaseModel):
    nome: str
    tem_cozinha: bool

class UnidadeCriar(UnidadeBase):
    # Pra criar, so preciso dos dados base mesmo
    pass

class UnidadeLer(UnidadeBase):
    id: int # Quando eu leio do banco, ele tem ID.

    class Config:
        from_attributes = True # Isso serve pro Pydantic ler dados do SQLAlchemy

# 2. Regras para PRODUTOS
class ProdutoBase(BaseModel):
    nome: str
    categoria: str # Ex: Lanche, Bebida
    preco: float

class ProdutoCriar(ProdutoBase):
    pass

class ProdutoLer(ProdutoBase):
    id: int
    
    class Config:
        from_attributes = True

# --- REGRAS PARA PEDIDOS (O CORAÇÃO DO SISTEMA) ---

# 3. Regras para ITENS DO PEDIDO (Ex: 2x Cuscuz)
class ItemPedidoBase(BaseModel):
    produto_id: int
    quantidade: int

class ItemPedidoCriar(ItemPedidoBase):
    pass

class ItemPedidoLer(ItemPedidoBase):
    id: int
    # Aqui vamos permitir mostrar o nome do produto junto, pra ficar chique
    
    class Config:
        from_attributes = True

# 4. Regras para O PEDIDO COMPLETO
class PedidoBase(BaseModel):
    unidade_id: int
    forma_pagamento: str # PIX, MOCK, DINHEIRO
    canal_pedido: str # APP, TOTEM, BALCAO

class PedidoCriar(PedidoBase):
    # O pedido TEM que ter uma lista de itens
    itens: List[ItemPedidoCriar]

class PedidoLer(PedidoBase):
    id: int
    status: str
    valor_total: float
    data_criacao: datetime = None # datetime precisa importar lá em cima
    itens: List[ItemPedidoLer] = []

    class Config:
        from_attributes = True        