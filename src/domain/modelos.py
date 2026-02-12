from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

# Base para criar as tabelas do banco
Base = declarative_base()

# 1. Tabela de Unidades (Lojas)
class Unidade(Base):
    __tablename__ = "unidades"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    tem_cozinha = Column(Boolean, default=True)

# 2. Tabela de Produtos (O Cardápio)
class Produto(Base):
    __tablename__ = "produtos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    categoria = Column(String)
    preco = Column(Float)
    # Adicionei isso aqui pra controlar a quantidade
    estoque = Column(Integer, default=0)

# 3. Tabela de Usuários (Login)
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String)
    perfil = Column(String)

# 4. Tabela de Pedidos (Vendas)
class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="RECEBIDO")
    canal_pedido = Column(String) # APP, TOTEM, BALCAO
    forma_pagamento = Column(String)
    valor_total = Column(Float, default=0.0)
    
    # Chaves Estrangeiras (Quem pediu? Onde?)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    unidade_id = Column(Integer, ForeignKey("unidades.id"))
    
    # Relacionamento com os itens
    itens = relationship("ItemPedido", back_populates="pedido")

# 5. Tabela de Itens do Pedido (O que tem dentro do pedido)
class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, index=True)
    quantidade = Column(Integer)
    
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    
    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto")