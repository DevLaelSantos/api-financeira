<!-- * 🗺️ Roadmap de Nivelamento e Etapas do Projeto -->

<!-- * Vamos dividir o projeto em 5 Sprints. Cada Sprint tem um objetivo técnico, o nível de conhecimento exigido e o que você aprenderá. -->


<!-- ? Sprint 1: Fundação e Arquitetura Limpa (Nível Júnior Avançado) -->
<!-- todo - Objetivo: Criar a estrutura de pastas, configurar o FastAPI e a conexão com o PostgreSQL usando o padrão Repository. -->

<!-- *
*
* - Conhecimento Necessário: Python (POO), FastAPI básico, SQLAlchemy (Models), Pydantic (Schemas).

* => O que você vai aprender: Injeção de Dependência (Depends), separação de responsabilidades (Router não fala com o Banco), e como usar o SQLModel para unificar Model e Schema .

* - Entregável: Um endpoint /health funcionando e a estrutura de pastas (models, schemas, repositories, services) criada.

*
* -->


<!-- * ===================================================================================== -->
<!-- * ===================================================================================== -->


<!-- ? Sprint 2: O Coração Financeiro e Autenticação (Nível Pleno) -->
<!-- todo Objetivo: Implementar o CRUD de Transações (Receitas/Despesas) e o sistema de Login com JWT. -->

<!-- *
*
* - Conhecimento Necessário: JWT (JSON Web Tokens), Hashing de senha (Bcrypt), Migrações com Alembic.

* => O que você vai aprender: Como proteger rotas (Authorization Header), como criar tabelas de usuários e transações com relacionamentos (1:N), e como versionar o banco de dados sem perder dados .

* Entregável: Usuário consegue se registrar, logar e criar uma transação financeira atrelada ao seu ID.

*
* -->

<!-- * ===================================================================================== -->
<!-- * ===================================================================================== -->


<!-- ? Sprint 3: Regras de Negócio e Robustez (Nível Pleno) -->
<!-- todo Objetivo: Adicionar validações complexas (ex: não permitir saldo negativo, categorizar gastos) e tratamento de erros personalizado. -->

<!-- *
* 
* - Conhecimento Necessário: Pydantic Validators, HTTPException, Logging.

* => O que você vai aprender: Como garantir a integridade dos dados financeiros. O Service Layer será o guardião das regras (ex: "Se a transação for 'saída', verifique se o saldo é suficiente").

* - Entregável: API retorna erros amigáveis (400, 422) em vez de quebrar (500).

*
* -->

<!-- * ===================================================================================== -->
<!-- * ===================================================================================== -->


<!-- ? Sprint 4: Qualidade e Testes (Nível Pleno Sênior) -->
<!-- todo Objetivo: Escrever testes automatizados para garantir que o código não quebre ao ser refatorado. -->

<!-- *
*
* - Conhecimento Necessário: Pytest, TestClient (FastAPI), Mocking. 

* => O que você vai aprender: Como testar endpoints, como testar regras de negócio isoladamente e como usar um banco de dados de teste (SQLite in-memory ou PostgreSQL de teste) .

* - Entregável: Cobertura de testes (coverage) acima de 80% nas rotas principais.

*
* -->


<!-- * ===================================================================================== -->
<!-- * ===================================================================================== -->


<!-- ? Sprint 5: Containerização e Deploy (Nível Sênior) -->
<!-- todo Objetivo: Colocar a API e o Banco de Dados em containers Docker para rodar em qualquer lugar (Produção). -->

<!-- * 
*
* - Conhecimento Necessário: Docker, Docker Compose, Variáveis de Ambiente. 

* => O que você vai aprender: Como criar um Dockerfile otimizado para FastAPI, como subir o PostgreSQL junto com a API usando docker-compose e como fazer o deploy no Render/Railway .

* - Entregável: Link público da API rodando com o Swagger (/docs) acessível.

*
* -->
