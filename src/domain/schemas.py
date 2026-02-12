from pydantic import BaseModel
from typing import List, Optional

# --- SCHEMAS (REGRAS DE DADOS) ---

# 1. Regras para UNIDADES
class UnidadeBase(BaseModel):
    nome: str
    tem_cozinha: bool

class UnidadeCriar(UnidadeBase):
    pass

class UnidadeLer(UnidadeBase):
    id: int
    class Config:
        from_attributes = True

# 2. Regras para PRODUTOS
class ProdutoBase(BaseModel):
    nome: str
    categoria: str 
    preco: float
    estoque: int # Agora pedimos o estoque na hora de criar

class ProdutoCriar(ProdutoBase):
    pass

class ProdutoLer(ProdutoBase):
    id: int
    class Config:
        from_attributes = True

# 3. Regras para PEDIDOS (A novidade)
class ItemPedidoSchema(BaseModel):
    produto_id: int
    quantidade: int

class PedidoCriar(BaseModel):
    unidade_id: int
    canal_pedido: str # Ex: APP, TOTEM
    itens: List[ItemPedidoSchema] # Uma lista de itens
    
# --- NOVAS REGRAS: USUÁRIOS (LGPD) ---

class UsuarioBase(BaseModel):
    nome: str
    email: str
    perfil: str # Ex: 'ADMIN' ou 'CLIENTE'

# Para CRIAR, precisamos da senha
class UsuarioCriar(UsuarioBase):
    senha: str 

# Para LER (devolver pro front), NÃO mostramos a senha! (Segurança Básica)
class UsuarioLer(UsuarioBase):
    id: int
    class Config:
        from_attributes = True