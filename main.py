from fastapi import FastAPI
from src.api.endpoints import unidades, produtos, pedidos, pagamentos # <--- AQUI
from src.infrastructure.banco_de_dados import engine
from src.domain.modelos import Base

# Cria as tabelas se não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Raizes do Nordeste",
    description="Trabalho da Faculdade - Backend",
    version="1.0.0"
)

# Registrando as rotas
app.include_router(unidades.router, prefix="/unidades", tags=["Unidades"])
app.include_router(produtos.router, prefix="/produtos", tags=["Produtos"])
app.include_router(pedidos.router, prefix="/pedidos", tags=["Pedidos"])
app.include_router(pagamentos.router, prefix="/pagamentos", tags=["Pagamentos"]) # <--- E AQUI

@app.get("/")
def raiz():
    return {"mensagem": "API Raizes do Nordeste esta online!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)