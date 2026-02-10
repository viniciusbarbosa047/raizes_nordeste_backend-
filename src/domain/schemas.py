from pydantic import BaseModel
from typing import List, Optional

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