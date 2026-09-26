# n8n Workflow Specification

## 1. Purpose

This document defines the production-oriented n8n automation layer for the PrimeHomes Realty Real Estate Lead Bot. It translates application events into reliable workflows for AI processing, lead qualification, customer communication, sales notification, follow-up, synchronization, summaries, error handling, and scheduled maintenance.

## 2. Architectural Position

n8n is the **orchestration and integration layer**. It is not the authoritative backend and must not become a second database or undocumented business-logic service.

```text
Customer / Channel
      ↓
   FastAPI
      ↓
     n8n
 ┌────┼───────────────┐
 ↓    ↓               ↓
 AI  Notifications  Scheduled Jobs
      ↓
   FastAPI / PostgreSQL
```

### Ownership boundaries

| Area | Owner |
|---|---|
| API contract | FastAPI |
| Authentication / authorization | FastAPI |
| Authoritative business state | PostgreSQL through FastAPI |
| Lead qualification score | Backend service |
| Lifecycle transition rules | Backend service |
| Natural-language interpretation | AI |
| Response generation | AI, grounded by backend data |
| Workflow routing | n8n |
| Scheduling / waits | n8n |
| External notifications | n8n |
| Audit/activity persistence | FastAPI |

## 3. Core Workflow Rules

1. Every workflow has one clearly defined purpose.
2. Validate input before processing.
3. Use idempotency for externally retried events.
4. Fetch authoritative state from the backend when required.
5. Treat AI output as untrusted until schema validation succeeds.
6. Never allow raw AI output to directly authorize a privileged action.
7. Keep deterministic business rules outside prompts.
8. Record important workflow outcomes through the backend.
9. Use bounded retries for transient failures only.
10. Route unrecoverable failures to the error workflow.
11. Never log secrets, access tokens, or unnecessary customer PII.
12. Keep workflow names and webhook paths stable after release.
13. Version prompts and workflow definitions.
14. Test duplicate, timeout, malformed-input and partial-failure cases.
15. A workflow must be safe to execute more than once when an external system retries an event.

## 4. Workflow Inventory

| ID | Workflow | Trigger | Primary responsibility |
|---|---|---|---|
| WF-001 | Lead Intake | Webhook/API event | Receive and normalize new customer messages |
| WF-002 | Lead Qualification | Lead/message event | Calculate and persist qualification |
| WF-003 | Customer Response | Validated conversation event | Generate and send grounded response |
| WF-004 | Sales Notification | Qualification/status event | Notify sales of actionable leads |
| WF-005 | Human Handoff | Escalation event | Stop conflicting automation and hand off to a person |
| WF-006 | Follow-Up Reminder | Schedule | Process due follow-ups |
| WF-007 | Lead Status Sync | Approved status event | Synchronize external systems |
| WF-008 | Conversation Summary | Conversation event/schedule | Maintain concise sales context |
| WF-009 | Error Handler | Workflow failure | Classify, retry, record and escalate failures |
| WF-010 | Scheduled Maintenance | Cron | Housekeeping and operational checks |

---

# 5. WF-001 — Lead Intake

### Objective
Receive a customer message, validate it, identify the customer/conversation/lead context, persist the message through the backend, and initiate downstream processing.

### Trigger
Preferred trigger: FastAPI event/webhook. A channel-specific webhook may also enter n8n if the channel is intentionally owned by n8n.

### Input contract
```json
{
  "event_id": "evt_123",
  "conversation_id": "conv_123",
  "external_message_id": "msg_external_456",
  "customer_id": "cus_123",
  "message": "I need a 3-bedroom apartment in Lekki around N80m",
  "channel": "web",
  "received_at": "2026-09-25T20:00:00Z"
}
```

### Processing
1. Receive event.
2. Validate required fields.
3. Check event/message idempotency.
4. Normalize whitespace and metadata without changing the original message.
5. Send the message to FastAPI for authoritative persistence.
6. Request AI extraction using the approved schema.
7. Validate AI output.
8. Send validated extraction to the backend.
9. Trigger qualification and response workflows.
10. Record workflow activity.

### Failure behavior
- Malformed payload → reject and record validation error.
- Duplicate event → return safely without creating another message.
- AI timeout → retry according to bounded policy.
- AI schema failure → retry once if appropriate, then route to human/error handling.
- Backend unavailable → retry transient failures and do not mark the event successful until the authoritative operation succeeds.

# 6. WF-002 — Lead Qualification

### Objective
Turn validated lead information into a deterministic qualification result.

### Rule
n8n does **not** calculate the business score itself when the score is defined as a domain rule. It calls the backend qualification service.

### Inputs
- lead ID
- extracted intent
- property requirements
- budget
- timeframe
- location
- contactability
- engagement/completeness data

### Sequence
```text
Lead event
 → Fetch authoritative lead
 → POST qualification request
 → Validate response
 → Persist/confirm result
 → IF high priority
      → WF-004 Sales Notification
   ELSE
      → continue normal response flow
```

### Example response
```json
{
  "lead_id": "lead_123",
  "score": 82,
  "qualification": "HIGH",
  "urgency": "HIGH",
  "version": "qualification-v1"
}
```

# 7. WF-003 — Customer Response

### Objective
Generate a useful response from validated facts and conversation context, then persist the outgoing message.

### Grounding rules
- Do not invent property availability.
- Do not invent prices.
- Do not claim a viewing is booked unless the backend confirms it.
- Do not expose internal scoring or workflow details unnecessarily.
- Ask for the highest-value missing information.
- Preserve customer language and Nigerian context where natural.

### Sequence
```text
Validated message
 → Fetch conversation context
 → Fetch current lead facts
 → Build AI response input
 → Generate response
 → Validate response
 → Send through channel/backend
 → Persist outgoing message
 → Update conversation state
```

If AI response generation fails, use a safe fallback such as asking the customer to provide the missing information or informing them that a sales representative will assist.

# 8. WF-004 — Sales Notification

### Objective
Notify the sales team when a lead meets configured notification criteria.

### Notification conditions
Examples:
- high qualification
- high urgency
- customer requests a viewing
- customer requests a human
- negotiation intent
- complaint/escalation
- repeated unanswered follow-up

### Notification payload
```json
{
  "lead_id": "lead_123",
  "qualification": "HIGH",
  "urgency": "HIGH",
  "intent": "BUY",
  "property_type": "APARTMENT",
  "location": "Lekki",
  "budget": "NGN 80,000,000",
  "summary": "Customer wants a 3-bedroom apartment in Lekki and is ready to discuss options."
}
```

The notification should link to the sales lead record rather than embedding unnecessary customer data.

# 9. WF-005 — Human Handoff

### Trigger conditions
- explicit request for an agent
- low AI confidence
- unresolved contradiction
- viewing/negotiation request
- complaint
- unsupported request
- repeated automation failure

### Sequence
```text
Escalation event
 → Fetch lead/conversation
 → Set conversation = ESCALATED
 → Stop conflicting bot response automation
 → Assign/notify sales
 → Record activity
 → Await human action
```

Once handed off, automated customer messages must not continue blindly. The conversation state is the control mechanism.

# 10. WF-006 — Follow-Up Reminder

### Trigger
Scheduled execution.

### Sequence
1. Query FastAPI for due follow-ups.
2. For each item, verify the lead is still eligible.
3. Check that no newer customer message or completed follow-up makes the reminder obsolete.
4. Send reminder or create a sales task.
5. Record outcome.
6. Mark follow-up completed/cancelled/overdue as appropriate.

Use n8n `Wait` only when a workflow-specific delayed execution is appropriate; use the backend as the authoritative store for follow-up state.

# 11. WF-007 — Lead Status Sync

Status transitions are controlled by FastAPI. n8n may distribute approved changes to external systems such as Sheets or sales tools.

```text
Backend status event
 → Validate event
 → Determine destination
 → Push approved state
 → Confirm response
 → Record sync activity
```

External copies must not overwrite authoritative database state without an explicit backend API operation.

# 12. WF-008 — Conversation Summary

### Purpose
Maintain a concise, sales-useful summary of a conversation without replacing the original messages.

### Summary should contain
- customer intent
- property requirement
- location
- budget
- timeframe
- key preferences
- objections
- unanswered questions
- next action
- handoff state

AI-generated summaries must be clearly treated as derived information. The original messages remain authoritative.

# 13. WF-009 — Error Handler

### Error classes
| Class | Example | Action |
|---|---|---|
| Validation | Missing required field | Stop and record |
| Duplicate | Same external message | Ignore safely |
| Transient | Timeout/5xx | Bounded retry |
| Rate limit | AI/API 429 | Backoff/retry |
| Provider | AI unavailable | Fallback/escalate |
| Business | Invalid transition | Stop and notify |
| Security | Invalid signature | Reject and alert |

The error workflow should capture workflow ID, execution ID, node, error class, correlation ID and safe diagnostic information.

Never retry indefinitely.

# 14. WF-010 — Scheduled Maintenance

Potential jobs:
- mark overdue follow-ups
- identify failed notifications
- verify workflow health
- clean safe temporary records according to retention policy
- detect stuck conversations
- refresh operational summaries
- verify external synchronization failures

Destructive cleanup must be conservative and governed by the data-retention policy.

# 15. n8n Node Standards

### Webhook / Trigger
Use for external event entry where n8n owns the integration boundary.

### HTTP Request
Preferred for FastAPI calls and external APIs. Centralize authentication through credentials/environment configuration.

### Set / Edit Fields
Use for small, explicit data mapping.

### If / Switch
Use for business routing that is easy to read visually. Conditions should reference explicit fields.

### Code
Use only when transformation is materially clearer in code or cannot reasonably be expressed using standard nodes. Code nodes must be small, deterministic and documented.

### Merge
Use only when combining streams has a clear semantic meaning. Avoid complex hidden synchronization.

### Wait
Use for delayed workflow behavior where n8n should own execution timing. Persist the business follow-up record in the backend.

### Error Trigger
Use for centralized failure handling where appropriate.

# 16. Data Contract Standards

Every internal workflow payload should carry:
- `event_id`
- `correlation_id`
- `lead_id` when available
- `conversation_id` when available
- `timestamp`
- `source`
- `schema_version`

Example:
```json
{
  "event_id": "evt_001",
  "correlation_id": "corr_001",
  "lead_id": "lead_123",
  "conversation_id": "conv_123",
  "source": "fastapi",
  "schema_version": "1.0",
  "timestamp": "2026-09-25T20:00:00Z"
}
```

# 17. AI Integration Standards

AI prompts should be versioned and separated from workflow wiring where practical. The AI contract must specify:
- allowed enum values
- nullable fields
- confidence range
- missing information
- escalation signals
- response constraints

AI output is validated before it is used. If validation fails, n8n must not silently pass the malformed object to another node.

# 18. Nigerian Real-Estate Normalization

The workflows should recognize common expressions such as:
- `N80m` → NGN 80,000,000
- `80m` in a Nigerian real-estate context → likely NGN 80,000,000, subject to contextual validation
- `below N20m` → maximum budget of NGN 20,000,000
- `around N80m` → approximate range, not an exact equality
- `between N50m and N70m` → explicit min/max range

The AI may interpret language; deterministic backend logic should normalize and validate financial values before business decisions.

# 19. Multiple Requirements

A customer may provide several requirements in one message, for example:

> “I need either a 3-bedroom in Lekki around N80m or a 2-bedroom in Ikeja below N60m.”

The workflow must not overwrite one requirement with another. The backend should support a structured representation or a controlled MVP strategy for multiple property requirements.

# 20. Security

- Use HTTPS in shared/staging/production environments.
- Validate webhook signatures where the source provides them.
- Authenticate internal FastAPI calls.
- Keep API keys in n8n credentials/environment configuration.
- Do not place secrets in Code nodes.
- Minimize PII in logs.
- Restrict access to workflow editing and credentials.
- Protect webhook endpoints from replay and unauthorized invocation.

For local development, ngrok may expose n8n temporarily. It is not the production security boundary.

# 21. Observability

Every important execution should be traceable through a correlation ID. Monitor:
- execution failures
- retries
- AI latency
- AI schema failures
- notification failures
- webhook rejection rates
- follow-up failures
- workflow duration
- stuck executions

# 22. Testing Matrix

Each workflow requires:
1. Happy path.
2. Missing required input.
3. Invalid input.
4. Duplicate event.
5. Backend timeout.
6. AI timeout where applicable.
7. AI malformed output where applicable.
8. External notification failure.
9. Retry behavior.
10. Final failure/error routing.

Critical workflows must also be tested for replay and concurrency.

# 23. Implementation Order

1. WF-001 Lead Intake
2. WF-002 Lead Qualification
3. WF-003 Customer Response
4. WF-004 Sales Notification
5. WF-005 Human Handoff
6. WF-006 Follow-Up Reminder
7. WF-007 Lead Status Sync
8. WF-008 Conversation Summary
9. WF-009 Error Handler
10. WF-010 Scheduled Maintenance

# 24. Definition of Done

A workflow is complete only when:
- trigger is configured;
- input contract is documented;
- credentials are configured safely;
- validation exists;
- idempotency is considered;
- backend ownership boundaries are respected;
- AI output is validated where applicable;
- failure/retry behavior is implemented;
- execution is observable;
- representative tests pass;
- workflow is exported/version-controlled;
- documentation matches the actual implementation;
- no secrets are committed.

# 25. Core Rules

1. n8n orchestrates; FastAPI governs.
2. PostgreSQL is authoritative.
3. AI interprets; it does not own business truth.
4. Qualification is deterministic.
5. Original customer messages are preserved.
6. Every external event should be idempotent.
7. Every retry must be bounded.
8. Every important workflow failure must be observable.
9. Human handoff must stop conflicting automation.
10. External copies such as Sheets never become the source of truth by accident.
11. Code nodes are used deliberately, not by default.
12. Workflow contracts are versioned.
13. Secrets stay out of workflow code.
14. Production workflows must be tested with failure cases.
15. The simplest reliable workflow is preferred over unnecessary complexity.
