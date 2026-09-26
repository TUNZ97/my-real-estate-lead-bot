# Backend — FastAPI

Authoritative application layer for the Real Estate Lead Bot.

## Responsibilities
- API contracts & validation
- Authentication / authorization
- Domain logic & lifecycle rules
- Deterministic qualification
- Database access (PostgreSQL)
- Idempotent message processing

## Structure

```text
app/
├── main.py              # FastAPI application entry
├── config.py            # Settings via pydantic-settings
├── dependencies.py      # Shared DI
├── api/                 # Route modules
├── core/                # Security helpers
├── db/                  # Session, Base
├── models/              # SQLAlchemy ORM
├── schemas/             # Pydantic request/response models
├── services/            # Business logic
├── repositories/        # Data access layer
└── integrations/        # n8n client, AI adapter stubs
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Ensure DATABASE_URL is set (see root .env.example)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: http://localhost:8000/docs

## Migrations

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```
