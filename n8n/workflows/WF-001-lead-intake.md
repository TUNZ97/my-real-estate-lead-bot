# WF-001 — Lead Intake (n8n setup guide)

## Purpose
Receive events from FastAPI after a customer message is processed, and optionally run extra steps (notifications, Sheets sync, etc.).

## Recommended n8n setup (local)

1. Start n8n: `n8n start`
2. Create a new workflow named **WF-001 Lead Intake**
3. Add a **Webhook** node:
   - HTTP Method: `POST`
   - Path: `lead-intake`
   - This creates URL: `http://localhost:5678/webhook/lead-intake`
4. Add an **IF** node (optional) to branch on high qualification:
   - Condition: `{{ $json.qualification.level }}` equals `HIGH`
5. For high leads, add a **Slack** / **Email** / **Respond to Webhook** notification node
6. Optionally call FastAPI internal endpoints:
   - `POST http://localhost:8000/api/internal/qualify` with header `X-N8N-Secret: <your secret>`
   - `GET http://localhost:8000/api/internal/leads/{{ $json.lead_id }}`

## Payload FastAPI sends

```json
{
  "event_id": "...",
  "correlation_id": "...",
  "lead_id": "...",
  "conversation_id": "...",
  "message_id": "...",
  "message": "customer text",
  "channel": "web",
  "extraction": { ... },
  "qualification": {
    "score": 82,
    "level": "HIGH",
    "urgency": "HIGH",
    "version": "qualification-v1"
  },
  "source": "fastapi",
  "schema_version": "1.0"
}
```

## Important
- FastAPI already does extraction + qualification + response **before** calling n8n.
- n8n is for orchestration (notifications, CRM sync, follow-ups), not for replacing the backend.
- If n8n is offline, the customer still gets a response — the webhook call is best-effort.
