# API Specification

## 1. Purpose

Define the stable HTTP API between the frontend, external clients, automation workflows and FastAPI backend.

Base path: `/api`.

## 2. Conventions

- JSON request/response bodies.
- ISO-8601 timestamps in UTC.
- Stable resource IDs.
- Pagination for collection endpoints.
- Validation errors return structured details.
- Authentication required for protected sales/admin endpoints.
- API versioning should be introduced when breaking changes are unavoidable.

## 3. Core endpoints

### Messages
`POST /api/messages` — submit a customer message.

Example request:
```json
{"conversation_id":"conv_123","message":"I need a 3-bedroom apartment in Lekki"}
```

Example response:
```json
{"conversation_id":"conv_123","message_id":"msg_456","response":"Thanks! Are you looking to buy or rent?","lead_id":"lead_789"}
```

### Leads
- `GET /api/leads`
- `GET /api/leads/{lead_id}`
- `PATCH /api/leads/{lead_id}`
- `POST /api/leads/{lead_id}/status`
- `POST /api/leads/{lead_id}/qualify`

### Conversations
- `GET /api/conversations/{conversation_id}`
- `GET /api/conversations/{conversation_id}/messages`

### Follow-ups
- `POST /api/leads/{lead_id}/follow-ups`
- `GET /api/leads/{lead_id}/follow-ups`
- `PATCH /api/follow-ups/{follow_up_id}`

### Notifications
- `GET /api/notifications`
- `POST /api/notifications/{id}/acknowledge`

### Health
- `GET /health`
- `GET /ready`

## 4. Error format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": []
  },
  "request_id": "req_123"
}
```

Do not expose stack traces or provider secrets.

## 5. Authentication and authorization

Use a standard token/session mechanism for protected internal APIs. Roles determine access to sales and admin operations. Customer-facing message intake may use a separate channel authentication mechanism.

## 6. Idempotency

Message intake must support an external message identifier or idempotency key. Repeated delivery of the same event must not create duplicate messages/leads or duplicate irreversible notifications.

## 7. Validation

Pydantic models validate syntax and field types. Domain services validate business rules such as legal status transitions, budget ranges and ownership.

## 8. Pagination/filtering

List endpoints should support explicit page/limit or cursor semantics and filters such as status, qualification, urgency, assigned user and date range.

## 9. n8n integration

Internal workflow callbacks must be authenticated and should carry stable identifiers such as `lead_id`, `conversation_id`, `message_id` and correlation/request IDs. n8n should call documented backend operations rather than directly manipulating database tables.

## 10. API change policy

- Additive changes are preferred.
- Breaking changes require versioning/migration planning.
- Update tests and documentation with contract changes.
- Do not let AI coding agents invent undocumented endpoints.

## 13. Core Endpoint Contracts

### POST /api/messages
Accepts a customer message, validates the conversation context and returns the processing result or accepted event reference.

### GET /api/leads/{lead_id}
Returns authoritative lead information including current requirements, qualification, status and assigned sales user.

### PATCH /api/leads/{lead_id}
Updates permitted lead fields according to authorization and lifecycle rules.

### POST /api/leads/{lead_id}/qualify
Runs the deterministic qualification service and persists the versioned result.

### POST /api/leads/{lead_id}/handoff
Escalates the conversation to a human and records the reason.

### POST /api/follow-ups
Creates a follow-up for an eligible lead.

### PATCH /api/follow-ups/{follow_up_id}
Updates follow-up status or completion information.

### GET /api/health
Returns service health suitable for deployment monitoring.

## 14. API Error Contract

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request contains invalid fields.",
    "request_id": "req_123",
    "details": []
  }
}
```

Clients should branch on stable error codes rather than parsing human-readable messages.

## 15. Idempotency

Message ingestion and other externally retried write operations should accept an idempotency key or external event identifier. A repeated request must not create duplicate messages, leads or notifications.

## 16. Authorization

Sales agents may access permitted leads and conversations; managers may have broader operational access; administrators manage system configuration. Authorization is enforced server-side even if the frontend hides controls.

## 17. API Versioning

Use an explicit versioning strategy such as `/api/v1` once public compatibility matters. Breaking changes require migration planning and documentation updates.
