# IUPI – API de Controle de Despesas

## Sumário
- [Tecnologias utilizadas](#tecnologias-utilizadas)
- [Funcionalidades](#funcionalidades)
- [Arquitetura e Organização do Projeto](#arquitetura-e-organização-do-projeto)
- [Endpoints principais](#endpoints-principais)
- [Como executar](#como-executar)
  - [Usando Docker](#usando-docker)
  - [Sem Docker](#executando-sem-docker)
- [Testes automatizados](#testes-automatizados)
- [Gerar documentação de código](#gerar-documentação-de-código)
- [Logs](#logs)
- [Banco de dados](#banco-de-dados)

## Tecnologias utilizadas
- Python 3.11
- Django
- Django REST Framework
- Simple JWT
- SQLite
- Docker e Docker Compose
- Django TestCase

## Funcionalidades
A API implementa todos os requisitos funcionais do [desafio](desafio.md), incluindo validações, autenticação e testes automatizados.
- CRUD completo para transações
- Filtros por tipo e descrição (combináveis)
- Resumo financeiro com total de receitas, despesas e saldo líquido
- Autenticação via JWT
- Paginação nos endpoints de listagem

### Funcionalidades adicionais implementadas
Além dos requisitos obrigatórios, foram adicionados alguns recursos complementares para tornar o projeto mais completo e alinhado com boas práticas:
- Geração de documentação automática via pydoc, aproveitando as docstrings já estruturadas.
- Configuração de logging com saída para console e arquivo, facilitando depuração e monitoramento.
- Conteinerização da aplicação utilizando Docker, permitindo execução isolada e reprodutível do ambiente.

## Arquitetura e Organização do Projeto
A aplicação segue uma arquitetura modular baseada na estrutura padrão Django:
- `transactions/` contém regras de negócio e endpoints da aplicação
- `tests/` separado por funcionalidades
- `scripts/` contém automações auxiliares
- `docker-compose` para execução isolada

## Endpoints principais
### Autenticação
````
POST /login/
````

### Transações
````
POST    /transactions/
GET     /transactions/
GET     /transactions/:id/
PATCH   /transactions/:id/
PUT     /transactions/:id/
DELETE  /transactions/:id/
````

### Resumo financeiro
````
GET /summary/
````

## Como executar
### Usando Docker
Recomendado, pois elimina a necessidade de ambiente virtual local.
1. Crie um arquivo `.env` na raiz do projeto com as variáveis de ambiente necessárias (veja o exemplo em `.env.example`).

2. Execute o comando:
   ```bash
   docker-compose up --build
   ```
O docker irá configurar o ambiente, instalar dependências, realizar migrações e iniciar o servidor na porta 8000.

3. Em outro terminal, crie um superuser para acessar a API:
Você pode usar o script `create_superuser.py` fornecido:
   ```bash
    bash scripts/create_superuser.sh
   ```

4. A API estará disponível em [http://localhost:8000](http://localhost:8000)

Posteriormente, você pode parar os containers com:
   ```bash
   docker-compose down
   ```

E para iniciar novamente:
   ```bash
   docker-compose up iupi-app
   ```

### Executando sem Docker
1. Crie um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Crie um arquivo `.env` na raiz do projeto com as variáveis de ambiente necessárias (veja o exemplo em `.env.example`).

4. Execute as migrações:
   ```bash
   python manage.py migrate
   ```

5. Crie um superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Inicie o servidor:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
A API estará disponível em [http://localhost:8000](http://localhost:8000)

## Testes automatizados
Os testes cobrem:
- Criação, edição e exclusão de transações
- Restrições por usuário autenticado
- Paginação
- Resumo financeiro
- Validações e códigos de status

Para executar os testes automatizados, use o comando:
1. Se estiver usando Docker:
   ```bash
   bash scripts/run_tests.sh
   ```
2. Se estiver sem Docker:
   ```bash
   python manage.py test
   ```

## Gerar documentação de código
Para gerar a documentação de código utilizando pydoc, execute o seguinte comando no terminal:
1. Se estiver usando Docker:
   ```bash
   docker compose run --rm iupi-docs
   ```

2. Se estiver sem Docker:
   ```bash
   python -m pydoc -w .
   ```

A documentação será gerada em arquivos HTML na pasta `docs/`.

## Logs
A aplicação utiliza logging configurado no settings.py com saída para console e arquivo.
Os logs são armazenados em:
- `logs/app.log` - Logs gerais da aplicação

## Banco de dados
É utilizado SQLite por simplicidade e compatibilidade com o desafio. Nenhuma configuração adicional é necessária.