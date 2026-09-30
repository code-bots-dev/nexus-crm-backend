# Nexus CRM API - Backend

Repositório do backend do sistema Nexus CRM API, versão 2.0.0. Esta API foi desenvolvida para gerenciar as principais operações do CRM, oferecendo uma arquitetura modularizada.

## 🚀 Tecnologias e Dependências

*   **Framework Principal:** Construído em Python 3.12.6 utilizando o framework FastAPI.
*   **Banco de Dados:** Utiliza PostgreSQL hospedado na plataforma Supabase.
*   **Serviço de Nuvem Adicional:** Integração com Firebase presente no histórico do projeto.
*   **Autenticação e Segurança:** Implementação de tokens JWT com a biblioteca `python-jose` utilizando o algoritmo HS256.
*   **Criptografia de Senhas:** Hashing e verificação de senhas validados de forma segura com a biblioteca `bcrypt`.
*   **ORM e Conexão:** Uso de SQLAlchemy, `supabase` e `psycopg2` para integração e operações com o banco de dados.

## 📂 Estrutura de Módulos (Rotas)

A aplicação possui um sistema de roteamento modularizado que centraliza os seguintes recursos:
*   `login_router`: Gerenciamento de autenticação e acesso de usuários.
*   `cliente_router`: Operações de cadastro e consulta de clientes.
*   `lead_router`: Gerenciamento de leads do CRM.
*   `produto_router`: Controle e listagem de produtos.
*   `venda_router`: Registro e controle de vendas.
*   `agendamento_router`: Controle de agendamentos do sistema.
*   `permissao_router`: Controle de acessos e níveis de permissões.

## ⚙️ Configurações de Ambiente

Para rodar a aplicação corretamente, é necessário definir um arquivo `.env` na raiz do projeto contendo as seguintes variáveis:
*   `DATABASE_URL`: String de conexão do banco PostgreSQL (ex: Supabase).
*   `SECRET_KEY`: Chave secreta de 64 caracteres para assinatura e validação dos tokens JWT.
*   `ALGORITHM`: Algoritmo de criptografia, definido por padrão como HS256.

A política de CORS (Cross-Origin Resource Sharing) está pré-configurada para permitir a comunicação com frontends em ambiente de desenvolvimento local, liberando acesso para origens como `http://127.0.0.1:5500`, `http://127.0.0.1:5501` e `http://127.0.0.1:5502`.

## 🛠️ Instalação e Execução Local

1. Instale todas as dependências listadas executando o comando `pip install -r requirements.txt`.
2. Inicie o servidor localmente com o Uvicorn, que está listado nas dependências do projeto.

## ☁️ Deploy

O projeto está configurado para deploy contínuo na plataforma Render utilizando o plano gratuito da região de Oregon.
*   **Nome do Serviço:** O Web Service está nomeado como `backend-zeus`.
*   **Comando de Build:** O ambiente é preparado com a execução de `pip install -r requirements.txt`.
*   **Comando de Inicialização:** O serviço entra no ar em produção utilizando o comando `uvicorn main:app --host 0.0.0.0 --port 10000`.
