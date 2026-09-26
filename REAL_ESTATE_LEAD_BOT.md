# Real Estate Lead Bot

## 1. Overview

The Real Estate Lead Bot is an AI-assisted lead intake and qualification system for **PrimeHomes Realty**. It receives natural-language property enquiries, extracts structured requirements, stores the lead, evaluates qualification and urgency, responds to the customer, alerts the sales team when appropriate, and tracks the lead through its lifecycle.

## 2. Example enquiries

- “Hi, I'm looking for a 3-bedroom apartment around Lekki. My budget is around N80 million.”
- “Do you have any 2-bedroom apartments in Ikeja?”
- “I need land around Ibadan, preferably below N20 million.”
- “Hello, I want to buy a house.”

The system must handle both highly detailed and incomplete enquiries without inventing missing information.

## 3. Product promise

The system should turn unstructured property conversations into reliable, actionable sales records while keeping the customer experience conversational and allowing a human salesperson to take over at any point.

## 4. Core architecture

```text
Customer
   ↓
React / External Channel
   ↓
FastAPI Backend
   ↓
n8n Workflow Orchestration
   ↓
AI + Qualification + Notifications
   ↓
PostgreSQL / Sales Team
```

### Responsibilities

- **React:** presentation, chat, lead views and sales UI.
- **FastAPI:** API contracts, validation, authorization, business logic and database access.
- **n8n:** workflow orchestration, integrations, routing, scheduled automation and notifications.
- **AI:** natural-language understanding, extraction, classification, summarization and response drafting.
- **PostgreSQL:** authoritative application state.

## 5. Lead lifecycle

```text
NEW → CONTACTED → QUALIFIED → FOLLOW_UP → PROPERTY_MATCHED
→ VIEWING_SCHEDULED → NEGOTIATION → CONVERTED
```

Possible terminal/exception states include `LOST`, `CLOSED`, `NOT_INTERESTED`, and `UNQUALIFIED`.

**Lead status** represents sales-process position. **Qualification** represents current lead quality/value. **AI confidence** represents confidence in AI interpretation. These must remain separate.

## 6. Key capabilities

1. Receive customer messages.
2. Identify intent.
3. Extract property requirements.
4. Normalize budgets and currency.
5. Preserve original messages.
6. Create/update customers, leads and conversations.
7. Qualify leads deterministically.
8. Identify urgency and missing information.
9. Generate grounded customer responses.
10. Notify or escalate to sales.
11. Schedule and execute follow-ups.
12. Track status and activities.
13. Produce summaries for sales staff.
14. Record enough audit data to understand important automated decisions.

## 7. Non-goals for MVP

- Full property marketplace.
- Autonomous negotiation.
- Autonomous financial/legal advice.
- AI-only source of truth.
- Microservice decomposition.
- Kubernetes deployment.
- Complex recommendation engine before reliable lead capture exists.

## 8. Operating principles

- Never fabricate property availability, pricing or facts.
- Validate all AI structured output.
- Use deterministic rules for business-critical calculations.
- Preserve customer messages exactly as received where permitted.
- Make important workflow actions idempotent.
- Keep human handoff available.
- Prefer simple architecture that can be tested and operated.

## 8. Core Lead Journey

```text
Customer enquiry
 → Message received
 → Lead created/found
 → AI extracts requirements
 → Data validated
 → Qualification calculated
 → Customer receives response
 → Sales notified when required
 → Follow-up created
 → Lead status progresses
 → Conversion or closure
```

## 9. Example

Customer: “Hi, I'm looking for a 3-bedroom apartment around Lekki. My budget is around N80 million.”

The system should preserve the original message, identify a BUY/property-enquiry intent, extract apartment/3 bedrooms/Lekki/approximately NGN 80m, determine missing information such as timeframe, calculate qualification using deterministic rules and ask the customer a useful next question.

## 10. Implementation Principle

The project is intentionally designed as a modular system rather than a collection of disconnected automations. Each document in the repository defines a different engineering concern while the architecture keeps the boundaries consistent.
