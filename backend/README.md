# Backend — FastAPI + MySQL

Authoritative application layer for the Real Estate Lead Bot.

## Database

Local development uses **MySQL** (not PostgreSQL, not Docker).

```text
DATABASE_URL=mysql+aiomysql://root:YOUR_PASSWORD@localhost:3306/leadbot
DATABASE_URL_SYNC=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/leadbot
```

Create the database once:

```sql
CREATE DATABASE leadbot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

# Ensure backend/.env has correct DATABASE_URL*
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: http://localhost:8000/docs

## Structure

```text
app/
├── main.py
├── config.py
├── api/                 # HTTP routes
├── models/              # SQLAlchemy (MySQL)
├── schemas/
├── services/            # Message, lead, extraction, qualification
├── integrations/        # n8n, AI stubs
└── db/
```
