# Projeto Backend - Raízes do Nordeste 🌵

> Estudo de Caso: Projeto Multidisciplinar UNINTER 2026.
> API para gestão de lanchonetes, focada em multicanalidade e integração de pedidos.

## 📋 Sobre o Projeto
Este sistema é o Backend da rede "Raízes do Nordeste". Ele gerencia o fluxo crítico de vendas, desde o cardápio até a confirmação do pagamento, respeitando regras de estoque e diferenças entre unidades.

### 🛠 Tecnologias Utilizadas
- **Linguagem:** Python 3.12
- **Framework:** FastAPI
- **Banco de Dados:** SQLite (Arquivo `raizes_nordeste.db`)
- **ORM:** SQLAlchemy
- **Servidor:** Uvicorn

---

## 🚀 Como Rodar o Projeto (Passo a Passo)

### 1. Preparar o Ambiente
Certifique-se de ter o Python instalado. No terminal, execute:

```bash
# 1. Criar o ambiente virtual (para isolar as bibliotecas)
python3 -m venv .venv

# 2. Ativar o ambiente (No Mac/Linux)
source .venv/bin/activate

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Executar a API
Com o ambiente ativado, inicie o servidor:

Bash
python main.py
O servidor iniciará em: http://127.0.0.1:8000

# 5. Acessar a Documentação
O projeto possui documentação automática e interativa (Swagger). Acesse no navegador:

Documentação: http://127.0.0.1:8000/docs

# 6. 📦 Funcionalidades Implementadas (MVP)
1. Gestão de Unidades 🏪
Cadastro de Lojas: (POST /unidades) - Permite cadastrar novas filiais, definindo se possuem cozinha completa ou não.

Listagem: (GET /unidades) - Visualiza todas as unidades da rede.

2. Cardápio e Estoque 🍔
Cadastro de Produtos: (POST /produtos) - Inclui itens no cardápio definindo preço e quantidade em estoque.

Controle de Estoque: O sistema impede vendas se a quantidade solicitada for maior que a disponível.

3. Pedidos (Fluxo Crítico) 📝
Criação de Pedidos: (POST /pedidos) - Suporta múltiplos canais (APP, TOTEM).

Regras de Negócio:

Valida se a Unidade existe.

Verifica disponibilidade de estoque item a item.

Calcula o valor total do pedido automaticamente.

Baixa o estoque no momento da criação.

4. Pagamentos (Mock) 💳
Simulação Bancária: (POST /pagamentos/processar) - Simula a comunicação com uma operadora de cartão.

Regras de Aprovação:

Cartões terminados em qualquer número (exceto 1): APROVADO (Status PAGO).

Cartões terminados em 1: RECUSADO (Status CANCELADO_PAGAMENTO).