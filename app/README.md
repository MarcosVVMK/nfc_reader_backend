# prog3_backend
Backend do projeto da disciplina de Programação 3

## Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido para construção de APIs
- **PostgreSQL**: Banco de dados relacional
- **Docker**: Containerização da aplicação
- **SQLAlchemy**: ORM para Python
- **Pydantic**: Validação de dados
- **Poetry**: Gerenciamento de dependências Python

## Versões

- Python: 3.12 (latest)
- FastAPI: 0.115.6 (latest)
- PostgreSQL: 16 (latest)

## Pré-requisitos

- Docker
- Docker Compose

## Como executar

1. **Clone o repositório:**
   ```bash
   git clone <repository-url>
   cd prog3_backend
   ```

2. **Configure as variáveis de ambiente:**
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas configurações se necessário
   ```

3. **Execute a aplicação usando Docker Compose:**
   ```bash
   docker-compose up --build
   ```

4. **A API estará disponível em:**
   - http://localhost:8000
   - Documentação interativa (Swagger): http://localhost:8000/docs
   - Documentação alternativa (ReDoc): http://localhost:8000/redoc

## Endpoints Disponíveis

### Health Check
- `GET /` - Endpoint raiz
- `GET /api/v1/health` - Verifica se a API está funcionando
- `GET /api/v1/health/db` - Verifica a conexão com o banco de dados

### Usuários
- `POST /api/v1/users/` - Criar novo usuário
- `GET /api/v1/users/` - Listar usuários (com paginação)
- `GET /api/v1/users/{user_id}` - Obter usuário por ID
- `PUT /api/v1/users/{user_id}` - Atualizar usuário
- `DELETE /api/v1/users/{user_id}` - Deletar usuário

## Estrutura do Projeto

```
prog3_backend/
├── app/
│   ├── __init__.py
│   ├── config.py          # Configurações da aplicação
│   ├── database.py        # Configuração do banco de dados
│   ├── models.py          # Modelos do SQLAlchemy
│   ├── schemas.py         # Schemas do Pydantic
│   ├── controllers/       # Controladores (endpoints/roteadores)
│   │   ├── __init__.py
│   │   └── user_controller.py
│   ├── services/          # Lógica de negócio
│   │   ├── __init__.py
│   │   ├── base_service.py
│   │   └── user_service.py
│   ├── repositories/      # Camada de acesso a dados
│   │   ├── __init__.py
│   │   ├── base_repository.py
│   │   └── user_repository.py
│   └── routers/
│       ├── __init__.py
│       ├── health.py      # Endpoints de health check
│       └── users.py       # Endpoints de usuários
├── main.py                # Arquivo principal da aplicação
├── pyproject.toml         # Configuração do Poetry
├── poetry.lock           # Lock file do Poetry
├── Dockerfile            # Configuração do Docker
├── docker-compose.yml    # Orquestração dos containers
├── .env.example          # Exemplo de variáveis de ambiente
└── README.md
```

## Desenvolvimento

### Executar localmente (sem Docker)

1. **Instale o Poetry (se não tiver instalado):**
   ```bash
   pip install poetry
   ```

2. **Instale as dependências:**
   ```bash
   poetry install
   ```

3. **Configure o banco PostgreSQL localmente e ajuste a DATABASE_URL no .env**

4. **Execute a aplicação:**
   ```bash
   poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Comandos Poetry úteis

```bash
# Instalar dependências
poetry install

# Adicionar nova dependência
poetry add package_name

# Adicionar dependência de desenvolvimento
poetry add --group dev package_name

# Ativar o ambiente virtual
poetry shell

# Executar comandos no ambiente Poetry
poetry run command
```

### Comandos Docker úteis

```bash
# Parar os containers
docker-compose down

# Reconstruir e executar
docker-compose up --build

# Ver logs
docker-compose logs -f

# Executar comandos no container da aplicação
docker-compose exec web bash

# Executar comandos no container do banco
docker-compose exec db psql -U postgres -d prog3_db
```

## Banco de Dados

O banco PostgreSQL será criado automaticamente quando você executar `docker-compose up`. As tabelas são criadas automaticamente através do SQLAlchemy.

### Configurações padrão:
- **Host**: localhost (db dentro do Docker)
- **Port**: 5432
- **Database**: prog3_db
- **Username**: postgres
- **Password**: postgres

Para alterar essas configurações, edite o arquivo `docker-compose.yml` e o arquivo `.env`.
