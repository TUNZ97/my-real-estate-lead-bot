# Real Estate Lead Bot — PrimeHomes Realty

AI-assisted lead intake and qualification system for PrimeHomes Realty.

Turns unstructured property enquiries into structured, actionable leads while keeping human sales representatives in control of the final sales process.

## Architecture Overview

```text
Customer / Channel
        ↓
React Frontend  ←→  FastAPI Backend  ←→  MySQL (source of truth)
                          ↓
                        n8n (orchestration)
                          ↓
              AI Provider + Notifications + Integrations
```

**Key principles**
- FastAPI is authoritative for business logic, validation, and state.
- **MySQL** is the single source of truth (local development).
- n8n orchestrates workflows and integrations.
- AI interprets and generates; it never owns business truth.
- Qualification is deterministic (not AI-driven).
- Original customer messages are preserved immutably.

## Repository Structure

```text
.
├── backend/                 # FastAPI application (MySQL)
├── frontend/                # React + Vite + TypeScript
├── n8n/                     # Workflow definitions & docs
├── docs/                    # Product & engineering specifications
├── SETUP.md                 # Local setup (MySQL + npm, no Docker)
├── .env.example
└── README.md
```

## Local development (no Docker)

Full steps: **[SETUP.md](./SETUP.md)**

Summary:

1. Create MySQL database `leadbot`
2. Copy `.env.example` → `.env` and set MySQL user/password
3. Backend: `pip install -r requirements.txt` → `alembic upgrade head` → `uvicorn ...`
4. Frontend: `npm install` → `npm run dev`
5. n8n (optional): `n8n start` + webhook path `lead-intake`

```text
React :5173  →  FastAPI :8000  →  MySQL :3306
                     ↓
                   n8n :5678
```

## License

MIT — see [LICENSE](./LICENSE).
