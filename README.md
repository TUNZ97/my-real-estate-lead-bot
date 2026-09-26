# Real Estate Lead Bot — PrimeHomes Realty

AI-assisted lead intake and qualification system for PrimeHomes Realty.

Turns unstructured property enquiries into structured, actionable leads while keeping human sales representatives in control of the final sales process.

## Architecture Overview

```text
Customer / Channel
        ↓
React Frontend  ←→  FastAPI Backend  ←→  PostgreSQL (source of truth)
                          ↓
                        n8n (orchestration)
                          ↓
              AI Provider + Notifications + Integrations
```

**Key principles**
- FastAPI is authoritative for business logic, validation, and state.
- PostgreSQL is the single source of truth.
- n8n orchestrates workflows and integrations.
- AI interprets and generates; it never owns business truth.
- Qualification is deterministic (not AI-driven).
- Original customer messages are preserved immutably.

## Repository Structure

```text
.
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── api/             # HTTP routes
│   │   ├── core/            # Config, security
│   │   ├── db/              # Database session & base
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Domain services
│   │   ├── repositories/    # Data access
│   │   └── integrations/    # n8n, AI adapters
│   ├── alembic/             # Migrations
│   ├── tests/
│   └── requirements.txt
├── frontend/                # React + Vite + TypeScript
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── types/
│   └── package.json
├── n8n/                     # Workflow definitions & docs
│   └── workflows/
├── docs/                    # All product & engineering specifications
├── tests/                   # Cross-cutting / E2E tests
├── docker-compose.yml
├── .env.example
└── README.md
```

## Documentation

All foundational specifications live in [`docs/`](./docs/):

| Document | Purpose |
|----------|---------|
| [PRD.md](./docs/PRD.md) | Product requirements |
| [REAL_ESTATE_LEAD_BOT.md](./docs/REAL_ESTATE_LEAD_BOT.md) | Product overview & principles |
| [SYSTEM_ARCHITECTURE.md](./docs/SYSTEM_ARCHITECTURE.md) | Architecture & component boundaries |
| [API_SPECIFICATION.md](./docs/API_SPECIFICATION.md) | HTTP API contracts |
| [DATABASE_DATA_MODEL_SPECIFICATION.md](./docs/DATABASE_DATA_MODEL_SPECIFICATION.md) | PostgreSQL schema |
| [AI_SPECIFICATION.md](./docs/AI_SPECIFICATION.md) | AI usage, extraction schema, safety |
| [LEAD_QUALIFICATION_SPECIFICATION.md](./docs/LEAD_QUALIFICATION_SPECIFICATION.md) | Deterministic scoring rules |
| [N8N_WORKFLOW_SPECIFICATION.md](./docs/N8N_WORKFLOW_SPECIFICATION.md) | Workflow inventory & contracts |
| [UI_UX_SPECIFICATION.md](./docs/UI_UX_SPECIFICATION.md) | Customer & sales UI |
| [IMPLEMENTATION.md](./docs/IMPLEMENTATION.md) | Phased build order |
| [TASK.md](./docs/TASK.md) | Task system & MVP breakdown |
| [DEVELOPMENT_SETUP.md](./docs/DEVELOPMENT_SETUP.md) | Local setup guide |
| [TESTING_SPECIFICATION.md](./docs/TESTING_SPECIFICATION.md) | Testing strategy |
| [DEPLOYMENT_SPECIFICATION.md](./docs/DEPLOYMENT_SPECIFICATION.md) | Environments & rollout |

## Quick Start (Development)

### Prerequisites
- Python 3.11+
- Node.js 20 LTS
- PostgreSQL 15+
- n8n (npm or Docker)

### 1. Clone & environment

```bash
git clone https://github.com/TUNZ97/my-real-estate-lead-bot.git
cd my-real-estate-lead-bot
cp .env.example .env
# Edit .env with your values
```

### 2. Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head   # after DB is running
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Database (via Docker)

```bash
docker compose up -d postgres
```

### 5. n8n

```bash
n8n start
# or use Docker; import workflows from n8n/workflows/ when ready
```

## Implementation Status

**Phase 1 — Project foundation** (current)
- [x] Repository structure
- [x] Environment configuration
- [x] Backend / frontend shells
- [ ] CI basics

See [docs/IMPLEMENTATION.md](./docs/IMPLEMENTATION.md) and [docs/TASK.md](./docs/TASK.md) for the full roadmap.

## License

MIT — see [LICENSE](./LICENSE).
