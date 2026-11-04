# Ecommerce API

Backend FastAPI organizado por domínios (`users`, `products`, `orders`,
`payments` e `inventory`).

## Features

- Mercado Pago payment processing
- RabbitMQ-powered asynchronous checkout processing
- User registration, authentication, and role-based access control
- Administrative dashboards and management workflows
- Product, inventory, order, and payment management
- Secure user and payment workflows

## Desenvolvimento

Na raiz deste repositório:

```bash
uv sync
cp .env.example .env
uv run uvicorn main:app --reload
```

O arquivo `.env` deve existir somente dentro de `backend/`; ele não é
compartilhado com o frontend nem com o diretório organizador.

A documentação OpenAPI fica em `/docs` e a API versionada em `/api/v1`.
Consulte o README da raiz para Docker, banco e migrations.

## Verificações

```bash
uv run pytest
uv run ruff check .
```

As configurações de banco, JWT, RabbitMQ e Mercado Pago são lidas por
`core/config.py`. Nunca versione o arquivo `.env`.
