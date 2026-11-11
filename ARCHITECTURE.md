# 🏗️ Arquitetura do Projeto

Este projeto utiliza uma arquitetura em camadas (inspirada no MVC) para garantir a separação de responsabilidades, facilitar os testes e permitir a escalabilidade.

## Estrutura de Pastas e Responsabilidades

- **`app/core/`**: Configurações centrais do projeto. Aqui ficam a conexão com o banco de dados, as configurações de segurança (JWT), e a leitura do arquivo `.env`.

- **`app/models/`**: Camada de Dados (Model). Contém as definições das tabelas do banco de dados usando SQLAlchemy. Elas não contêm regras de negócio, apenas a estrutura dos dados.

- **`app/schemas/`**: Camada de Validação (View/Schema). Contém os modelos Pydantic. Eles são responsáveis por validar os dados que entram (Request) e saem (Response) da API. Garantem que o JSON esteja no formato correto.

- **`app/repositories/`**: Camada de Acesso ao Banco (Repository Pattern). Isola a lógica de consulta ao banco de dados. Os serviços não sabem como o banco funciona, eles apenas pedem os dados ao repositório.

- **`app/services/`**: Camada de Regras de Negócio (Service Layer). É o "cérebro" da aplicação. Aqui ficam as validações complexas (ex: não permitir saldo negativo, calcular totais) e a orquestração do fluxo de dados.

- **`app/api/v1/`**: Camada de Roteamento (Controller). Define os endpoints (URLs) e recebe as requisições HTTP. Ela apenas recebe a requisição, chama o Service correspondente e devolve a resposta. Não contém lógica de negócio.

- **`main.py`**: Ponto de entrada da aplicação. Onde o FastAPI é instanciado e as rotas são registradas.