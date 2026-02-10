from fastapi import FastAPI
from src.api.endpoints import unidades

# Criando o aplicativo FastAPI
app = FastAPI(
    title="API Raizes do Nordeste",
    description="Sistema para gerenciar lanchonetes - Trabalho da Faculdade",
    version="1.0.0"
)

# Aqui eu aviso que as rotas de Unidades existem
app.include_router(unidades.router, prefix="/unidades", tags=["Unidades"])

# Uma rota simples so pra testar se ta rodando
@app.get("/")
def raiz():
    return {"mensagem": "API Raizes do Nordeste esta online!"}

# Se rodar esse arquivo direto, ele liga o servidor
if __name__ == "__main__":
    import uvicorn
    # Rodando na porta 8000
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)