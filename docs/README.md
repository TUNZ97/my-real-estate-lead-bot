# Documentation

Foundational specifications for the Real Estate Lead Bot (PrimeHomes Realty).

These documents are the approved source of truth for product, architecture, and implementation.

## Core Documents

| File | Description |
|------|-------------|
| [PRD.md](./PRD.md) | Product Requirements Document |
| [REAL_ESTATE_LEAD_BOT.md](./REAL_ESTATE_LEAD_BOT.md) | Product overview, architecture summary, operating principles |
| [SYSTEM_ARCHITECTURE.md](./SYSTEM_ARCHITECTURE.md) | Component boundaries, flows, reliability & security rules |
| [API_SPECIFICATION.md](./API_SPECIFICATION.md) | HTTP API contracts |
| [DATABASE_DATA_MODEL_SPECIFICATION.md](./DATABASE_DATA_MODEL_SPECIFICATION.md) | PostgreSQL entities, enums, indexes, integrity rules |
| [AI_SPECIFICATION.md](./AI_SPECIFICATION.md) | AI responsibilities, extraction schema, safety, evaluation |
| [LEAD_QUALIFICATION_SPECIFICATION.md](./LEAD_QUALIFICATION_SPECIFICATION.md) | Deterministic scoring model |
| [N8N_WORKFLOW_SPECIFICATION.md](./N8N_WORKFLOW_SPECIFICATION.md) | Full workflow inventory & contracts |
| [UI_UX_SPECIFICATION.md](./UI_UX_SPECIFICATION.md) | Customer chat & sales UI |
| [IMPLEMENTATION.md](./IMPLEMENTATION.md) | Phased build order & vertical slice |
| [TASK.md](./TASK.md) | Task system, statuses, MVP breakdown |
| [DEVELOPMENT_SETUP.md](./DEVELOPMENT_SETUP.md) | Local development guide |
| [TESTING_SPECIFICATION.md](./TESTING_SPECIFICATION.md) | Testing strategy & scenarios |
| [DEPLOYMENT_SPECIFICATION.md](./DEPLOYMENT_SPECIFICATION.md) | Environments, CI/CD, rollback |

**Before writing code**, read the relevant documents above. Do not invent architecture or endpoints that contradict these specs.
