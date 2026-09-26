# Setup & Run Guide — Real Estate Lead Bot

Follow these steps on your machine so frontend, backend, Postgres and n8n work together.

---

## 1. Prerequisites

- Python 3.11+
- Node.js 20 LTS
- Docker (for Postgres) **or** a local PostgreSQL 15+
- n8n (`npm install -g n8n` or use Docker)

---

## 2. Clone & env

```bash
git clone https://github.com/TUNZ97/my-real-estate-lead-bot.git
cd my-real-estate-lead-bot
cp .env.example .env
```

Edit `.env` if needed. Defaults work for local Docker Postgres:

```text
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/leadbot
DATABASE_URL_SYNC=postgresql://postgres:postgres@localhost:5432/leadbot
```

---

## 3. Start PostgreSQL

```bash
docker compose up -d postgres
```

Wait a few seconds until healthy.

---

## 4. Backend

```bash
cd backend
python -m venv .venv

# Windows PowerShell:
.\ .venv\Scripts\Activate.ps1

# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Check: http://localhost:8000/health  → `{"status":"ok",...}`  
Swagger: http://localhost:8000/docs

---

## 5. Frontend

Open a **new terminal**:

```bash
cd frontend
npm install
npm run dev
```

Open: http://localhost:5173

- **Customer Chat** — send enquiries (orange/yellow UI)
- **Sales Dashboard** — see leads created by the chat

---

## 6. n8n (optional but recommended)

```bash
n8n start
```

Open: http://localhost:5678

### Minimal WF-001 webhook

1. New workflow → **Webhook** node  
   - Method: `POST`  
   - Path: `lead-intake`  
   - URL becomes: `http://localhost:5678/webhook/lead-intake`
2. Add a **Set** or **Respond to Webhook** node so you can see the payload
3. Activate the workflow

FastAPI already posts to that URL after every message (best-effort).  
If n8n is down, chat still works.

See `n8n/workflows/WF-001-lead-intake.md` for full payload shape and next steps (Slack/email on HIGH leads).

---

## 7. Quick test flow

1. Open http://localhost:5173
2. Click an example or type:  
   `I'm looking for a 3-bedroom apartment around Lekki. Budget is around N80 million.`
3. Bot replies with a grounded response and asks for missing info if needed
4. Go to **Sales Dashboard** — you should see the lead with qualification score
5. Click **View** for full detail
6. If n8n is running, check the webhook execution for the event payload

---

## 8. Architecture reminder

```text
React (5173)  →  FastAPI (8000)  →  PostgreSQL
                      ↓
                    n8n (5678)  →  notifications / extra integrations
```

- FastAPI owns business state and qualification
- n8n orchestrates side effects
- AI extraction is rule-based for MVP (works offline); swap in real LLM later via `app/integrations/ai.py`

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Frontend “Failed to load leads” | Backend not running or CORS; check port 8000 |
| `alembic` errors | Ensure Postgres is up and `DATABASE_URL_SYNC` is correct |
| n8n never receives events | Workflow must be **Active**; path must be `lead-intake` |
| Import errors in Python | Activate venv and reinstall `requirements.txt` |

---

When everything above works, you’re ready to test on your device and extend n8n workflows.
