from fastapi import FastAPI
from src.api.endpoints import unidades, produtos # <--- ADICIONEI PRODUTOS AQUI

app = FastAPI(
    title="API Raizes do Nordeste",
    description="Sistema para gerenciar lanchonetes - Trabalho da Faculdade",
    version="1.0.0"
)

# Registrando as rotas
app.include_router(unidades.router, prefix="/unidades", tags=["Unidades"])
app.include_router(produtos.router, prefix="/produtos", tags=["Produtos"]) # <--- LINHA NOVA

@app.get("/")
def raiz():
    return {"mensagem": "API Raizes do Nordeste esta online!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)