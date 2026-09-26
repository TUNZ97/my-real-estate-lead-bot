# System Architecture

## 1. Goals

Provide a simple, testable architecture where each component has a clear responsibility and where AI automation does not compromise application correctness.

## 2. Architecture

```text
┌───────────────┐
│ Customer / UI │
└───────┬───────┘
        ↓
┌──────────────────┐
│ React Frontend   │
└────────┬─────────┘
         ↓ HTTPS/JSON
┌──────────────────┐
│ FastAPI Backend  │
│ API + Domain     │
└───────┬──────────┘
        ├──────────────→ PostgreSQL
        └──────────────→ n8n
                           ├→ AI provider
                           ├→ Notifications
                           └→ Integrations
```

## 3. Component boundaries

### React
Presentation, forms, chat, dashboard, status display and user interaction. It must not contain authoritative qualification or security decisions.

### FastAPI
Authentication/authorization, request validation, domain rules, database access, lifecycle transitions, idempotency and stable API contracts.

### n8n
Workflow orchestration, event routing, external integrations, scheduled jobs and notification flows.

### AI
Natural-language interpretation and generation. AI output is untrusted until validated.

### PostgreSQL
Source of truth for customers, leads, conversations, messages, activities, follow-ups and notifications.

## 4. Core flows

### Lead intake
1. Customer sends message.
2. Backend validates and records it.
3. Backend starts/updates conversation.
4. n8n processes the event.
5. AI extracts structured information.
6. Backend validates the result.
7. Lead is created/updated.
8. Qualification is recalculated.
9. Customer response is generated and delivered.
10. Sales notification is triggered when rules require it.

### Follow-up
Scheduled n8n workflow finds due follow-ups → validates lead state → sends or requests a follow-up → records activity → updates follow-up state.

## 5. Data authority

PostgreSQL is authoritative. Google Sheets, notification systems and AI context are derived/operational representations.

## 6. Reliability

- Idempotency keys/external message IDs prevent duplicate processing.
- Retry transient integration failures.
- Do not retry non-idempotent actions blindly.
- Record workflow and domain activities.
- Use correlation IDs across API and workflow executions.

## 7. Security boundaries

- HTTPS in deployed environments.
- Secrets only in environment/secret stores.
- Validate all external input.
- Authenticate protected API operations.
- Authorize sales/admin actions by role.
- Protect n8n webhooks/internal endpoints.
- Do not expose provider API keys to React.

## 8. Scalability

Start as a modular monolith. Scale the backend and n8n workers only when actual workload requires it. PostgreSQL indexes and query quality should be addressed before introducing distributed infrastructure.

## 9. Observability

Track request IDs, workflow IDs, lead IDs, errors, durations, AI model/prompt versions, retry counts and notification outcomes. Avoid logging unnecessary sensitive customer content.

## 10. Architecture rules

1. React presents.
2. FastAPI governs.
3. n8n orchestrates.
4. AI interprets/generates.
5. SQL stores authoritative state.
6. Business-critical calculations remain deterministic.
7. No component bypasses validation to write arbitrary business state.

## 15. Detailed Component Contracts

### React
Owns presentation, user interaction, client-side state and authenticated UI flows. It should not contain authoritative qualification or lifecycle rules.

### FastAPI
Owns API contracts, validation, authentication, authorization, domain services, database transactions, lifecycle transitions and deterministic qualification.

### n8n
Owns orchestration, integration routing, scheduling, notifications and workflow control. It calls FastAPI for authoritative operations.

### AI provider
Owns language understanding and generation. Its output is treated as untrusted data and validated against explicit schemas.

### PostgreSQL
Stores authoritative customers, leads, conversations, messages, activities, follow-ups and notifications.

## 16. End-to-End Message Flow

```text
Customer message
 → React/channel
 → FastAPI message endpoint
 → persist original message
 → emit processing event
 → n8n WF-001
 → AI extraction
 → schema validation
 → FastAPI update lead
 → qualification service
 → response generation
 → send response
 → persist bot message
 → optional sales notification
```

## 17. Failure Boundaries

A failure in AI should not corrupt the lead. A notification failure should not roll back a successfully persisted customer message. A frontend failure should not prevent backend processing when the message has already reached the API. Transactions should be used around atomic database operations; external side effects should use idempotency and appropriate retry/outbox patterns where required.

## 18. Scalability Direction

The MVP should remain a modular monolith plus n8n. Scale the API horizontally when required, use connection pooling for PostgreSQL, move long-running work to asynchronous/background processing where appropriate, and separate services only when operational or domain boundaries justify it. Avoid premature microservices and Kubernetes complexity.

## 19. Architecture Decision Records

Document decisions such as:
- why FastAPI is authoritative over n8n;
- why PostgreSQL is the source of truth;
- why qualification is deterministic;
- why n8n is retained for orchestration;
- why the MVP uses a modular monolith;
- why AI output requires schema validation.
