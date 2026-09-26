# Product Requirements Document (PRD)

## 1. Product

**Real Estate Lead Bot — PrimeHomes Realty**

## 2. Problem

Property enquiries arrive as unstructured conversations. Sales teams need to manually extract requirements, identify valuable/urgent prospects, respond quickly and remember follow-ups. This creates inconsistent qualification, delayed responses and lost opportunities.

## 3. Vision

Create a reliable AI-assisted system that turns property enquiries into structured, actionable leads while keeping humans in control of important sales interactions.

## 4. Goals

- Capture leads consistently.
- Understand customer intent and requirements.
- Respond quickly and appropriately.
- Qualify leads using transparent rules.
- Notify sales staff when action is needed.
- Track follow-ups and lifecycle state.
- Provide a useful sales interface.

## 5. Users

- Potential customer.
- Sales agent.
- Sales manager.
- Administrator.

## 6. Functional requirements

### FR-001 Lead intake
Accept customer property enquiries through the supported chat/channel.

### FR-002 Intent detection
Identify buy/rent/sell/property/general enquiry and unknown cases.

### FR-003 Requirement extraction
Extract property type, location, bedrooms, budget, currency, timeframe and contact information where available.

### FR-004 Lead persistence
Create or update a customer, lead and conversation while preserving original messages.

### FR-005 Qualification
Calculate deterministic qualification and urgency from validated information.

### FR-006 Missing information
Identify important missing information and ask targeted questions.

### FR-007 Response
Generate a grounded response without fabricating availability, price or property facts.

### FR-008 Sales notification
Notify sales when configured qualification/urgency/handoff conditions are met.

### FR-009 Human handoff
Allow a customer to request or trigger human assistance.

### FR-010 Follow-up
Create and execute scheduled follow-ups and track their outcome.

### FR-011 Lifecycle
Track lead status from new enquiry through conversion/loss/closure.

### FR-012 Conversation history
Allow sales users to inspect the conversation and relevant structured lead data.

## 7. Non-functional requirements

- Secure authentication and authorization.
- Reliable persistence.
- Idempotent message processing.
- Observable workflows.
- Responsive customer UI.
- Maintainable modular code.
- Testable AI boundary.
- Controlled AI cost/latency.

## 8. MVP

The MVP includes lead intake, extraction, persistence, qualification, customer response, sales notification, basic sales dashboard, follow-up and lifecycle tracking.

## 9. Future scope

Property inventory integration, richer matching, analytics, omnichannel support, advanced sales automation and deeper CRM integrations.

## 10. Success measures

Track lead capture rate, structured extraction completeness, response latency, qualification coverage, human handoff rate, follow-up completion, conversion tracking and AI error/hallucination rate.

## 11. Business rules

- SQL is authoritative.
- AI cannot invent facts.
- Qualification is deterministic.
- Customer data must not leak across leads/users.
- Important automated actions must be auditable.

## 16. Detailed Functional Requirements

### FR-013 Conversation continuity
The system shall preserve conversation context across multiple messages and avoid asking for information already provided unless the information is contradictory or has become stale.

### FR-014 Contradiction handling
If a customer changes a requirement, the system shall update the current lead state while retaining the previous message history. If the meaning is ambiguous, the bot shall ask for clarification rather than silently replacing important data.

### FR-015 Human escalation
The system shall support explicit customer handoff and automatic escalation for low-confidence, unsupported, complaint, viewing, negotiation, or repeated-failure scenarios.

### FR-016 Follow-up management
Sales users shall be able to create, complete, cancel and review follow-ups. Automated reminders shall verify that a follow-up is still relevant before contacting the customer.

### FR-017 Auditability
Important lead, qualification, status, assignment and follow-up changes shall generate an activity record containing actor/source, timestamp and relevant change information.

### FR-018 Operational resilience
Transient integration failures shall be retried safely; permanent failures shall be surfaced to operators without silently losing customer messages.

## 17. Business Rules

- A lead may exist without being fully qualified.
- Qualification score and lifecycle status are separate concepts.
- AI confidence is separate from qualification.
- The backend is the source of truth for lead state.
- AI cannot invent property availability, pricing or appointment confirmation.
- Financial values are stored using precise numeric types.
- Original messages are immutable records.
- Human handoff overrides conflicting automated response behavior.

## 18. MVP Acceptance Scenarios

**Scenario A — complete enquiry:** A customer provides property type, location and budget. The system stores the message, extracts the fields, calculates qualification and replies with the next useful question or grounded information.

**Scenario B — incomplete enquiry:** “I want a house.” The system creates/updates the lead and asks a focused question such as location or budget.

**Scenario C — high-value enquiry:** A customer gives a clear requirement, substantial budget and near-term timeframe. The system calculates the deterministic qualification and notifies sales according to configured rules.

**Scenario D — human request:** “Please connect me to an agent.” The system escalates, updates conversation state and alerts sales.

**Scenario E — contradiction:** A customer first states N50m then later says N100m. The latest message must be preserved and the system should update the current requirement according to an explicit precedence rule.

## 19. Success Metrics

Track lead creation rate, extraction validity, response latency, qualification completeness, human handoff rate, follow-up completion, notification success, conversation-to-viewing progression and conversion-related business metrics. Metrics should be interpreted by channel and time period rather than treated as a single undifferentiated number.
