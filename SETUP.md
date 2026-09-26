# Setup & Run Guide — Local MySQL (no Docker)

This guide uses **MySQL on your PC**, **Python** for the backend, and **npm** for the frontend and n8n. Docker is not required for development.

---

## 1. Prerequisites

- Python 3.11+
- Node.js 20 LTS + npm
- **MySQL** running locally (MySQL Workbench / XAMPP / WAMP / standalone)
- n8n via npm: `npm install -g n8n`

---

## 2. Create the MySQL database

Open MySQL (CLI or Workbench) and run:

```sql
CREATE DATABASE leadbot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Note your MySQL username and password (often `root` and a password you set, or empty on some XAMPP installs).

---

## 3. Clone & configure env

```bash
git pull origin main
cd my-real-estate-lead-bot
cp .env.example .env
```

Edit `.env` and set your MySQL credentials:

```text
DATABASE_URL=mysql+aiomysql://root:YOUR_PASSWORD@localhost:3306/leadbot
DATABASE_URL_SYNC=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/leadbot
```

Examples:
- Password is `secret`: `mysql+aiomysql://root:secret@localhost:3306/leadbot`
- No password (XAMPP default sometimes): `mysql+aiomysql://root@localhost:3306/leadbot`

Also copy the same values into `backend/.env` **or** keep a single `.env` at the repo root and run uvicorn from `backend` with env loaded (pydantic-settings looks for `.env` in the working directory — easiest is to put `.env` inside `backend/` as well):

```bash
cp .env backend/.env
```

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

# Create tables
alembic upgrade head

# Start API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Check:
- http://localhost:8000/health
- http://localhost:8000/docs

---

## 5. Frontend (npm)

New terminal:

```bash
cd frontend
npm install
npm run dev
```

Open: **http://localhost:5173**

---

## 6. n8n (npm)

New terminal:

```bash
n8n start
```

Open: **http://localhost:5678**

Create a workflow:
1. **Webhook** node → Method `POST` → Path `lead-intake`
2. Activate the workflow
3. URL will be `http://localhost:5678/webhook/lead-intake`

FastAPI posts there after every chat message (optional — chat works even if n8n is off).

---

## 7. Quick test

1. Chat: *“I'm looking for a 3-bedroom apartment around Lekki. Budget is around N80 million.”*
2. Bot replies with a grounded answer
3. Sales Dashboard shows the lead with qualification score
4. If n8n is active, check the webhook execution

---

## Architecture (local)

```text
React (npm, :5173)
    → FastAPI (Python, :8000)
        → MySQL (local, :3306)
        → n8n (npm, :5678)  [optional notifications]
```

---

## Troubleshooting

| Problem | Fix |
|--------|-----|
| `Access denied for user` | Wrong user/password in `.env` |
| `Unknown database 'leadbot'` | Run `CREATE DATABASE leadbot ...` |
| `Can't connect to MySQL` | Ensure MySQL service is running (Windows Services / XAMPP control panel) |
| Alembic fails | Confirm `DATABASE_URL_SYNC` uses `mysql+pymysql://...` |
| Frontend can’t reach API | Backend must be on port 8000; Vite proxies `/api` |
| n8n no events | Workflow must be **Active**; path exactly `lead-intake` |

---

Docker is **not** used for local development. You can introduce it later for deployment only.
