# 🌵 Raízes do Nordeste - API Backend

> Estudo de Caso: Projeto Multidisciplinar UNINTER.  
> Desenvolvido por: **Vinicius Eugénio Barbosa (RU: 4662400)**

## 📋 Sobre o Projeto
API RESTful desenvolvida para gerenciar as operações de uma rede de franquias de comida regional. O sistema atua como o motor principal para pedidos multicanal (App, Totens de autoatendimento e Balcão), controle rigoroso de estoque e processamento (mock) de pagamentos.

O foco central desta aplicação é garantir consistência nas regras de negócio e **segurança de nível comercial**, implementando criptografia de senhas e proteção de rotas via tokens JWT, em conformidade com as boas práticas de proteção de dados.

## 🚀 Tecnologias e Ferramentas
- **Linguagem:** Python 3.12
- **Framework Web:** FastAPI
- **Banco de Dados:** SQLite (Relacional)
- **ORM:** SQLAlchemy
- **Segurança e Criptografia:** JWT (JSON Web Tokens), bcrypt e Passlib
- **Servidor Local:** Uvicorn

## ⚙️ Instruções de Instalação e Execução

Siga os passos abaixo para rodar o projeto localmente em ambientes Mac/Linux:

**1. Clone o repositório e acesse a pasta:**
git clone <URL_DO_SEU_REPOSITORIO_AQUI>
cd raizes_nordeste_backend

**2. Crie e ative o ambiente virtual:**
python3 -m venv .venv
source .venv/bin/activate

**3. Instale as dependências exigidas:**
pip install -r requirements.txt

**4. Inicie o Servidor:**
python main.py

O servidor estará rodando em: http://127.0.0.1:8000

## 📖 Documentação da API (Swagger UI)
A documentação interativa das rotas e schemas pode ser acessada com o servidor rodando através do link:
- **Acessar Swagger:** http://127.0.0.1:8000/docs

## 🔐 Principais Funcionalidades (Endpoints)

### Autenticação & Segurança
- `POST /auth/login`: Autentica o usuário e gera o Token JWT (Bearer).
- `POST /usuarios/`: Cadastra novos administradores (senha criptografada).

### Gestão do Negócio (Rotas Protegidas)
- `POST /unidades/`: Cadastro de novas franquias.
- `POST /produtos/`: Cadastro de itens do cardápio com inserção de quantidade em estoque.
- `POST /pedidos/`: Criação de pedidos com baixa automática de estoque.
- `POST /pagamentos/processar`: Simulação de gateway de pagamento.

---
*Projeto acadêmico desenvolvido para fins de avaliação.*