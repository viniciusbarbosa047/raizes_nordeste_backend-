from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Unidade(Base):
    __tablename__ = "unidades"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    tem_cozinha = Column(Boolean, default=True)

class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    categoria = Column(String)
    preco = Column(Float)

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String)
    perfil = Column(String)

class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="RECEBIDO")
    canal_pedido = Column(String)
    forma_pagamento = Column(String)
    valor_total = Column(Float, default=0.0)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    unidade_id = Column(Integer, ForeignKey("unidades.id"))
    itens = relationship("ItemPedido", back_populates="pedido")

class ItemPedido(Base):
    __tablename__ = "itens_pedido"
    id = Column(Integer, primary_key=True, index=True)
    quantidade = Column(Integer)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto")