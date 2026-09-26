# Database Data Model Specification

## 1. Purpose

Define the PostgreSQL model that stores authoritative business state for the Real Estate Lead Bot.

## 2. Core entities

### customers
Represents a person interacting with PrimeHomes.

Suggested fields: `id`, `name`, `email`, `phone`, `created_at`, `updated_at`.

### leads
Represents a property-sales/rental opportunity.

Suggested fields: `id`, `customer_id`, `status`, `intent`, `property_type`, `location_text`, `bedrooms`, `budget_min`, `budget_max`, `currency`, `timeframe`, `qualification_level`, `qualification_score`, `urgency`, `qualification_version`, `created_at`, `updated_at`.

### conversations
Represents a customer interaction thread.

Suggested fields: `id`, `customer_id`, `lead_id`, `status`, `channel`, `created_at`, `updated_at`.

### messages
Immutable conversation messages where possible.

Suggested fields: `id`, `conversation_id`, `sender_type`, `content`, `external_message_id`, `created_at`, metadata.

### lead_activities
Audit-friendly business events such as status changes, qualification changes, assignment, handoff and follow-up completion.

### follow_ups
Tracks scheduled actions: `id`, `lead_id`, `due_at`, `status`, `reason`, `assigned_to`, `completed_at`.

### users / sales users
Authenticated internal users with roles such as `SALES_AGENT`, `SALES_MANAGER`, `ADMIN`.

### notifications
Tracks sales notifications and delivery state.

### ai_processing_logs (optional)
Stores model/provider, prompt/schema versions, outcome, confidence and timing without unnecessarily storing sensitive raw content.

## 3. Relationships

```text
Customer 1 ─── * Lead
Customer 1 ─── * Conversation
Lead 1 ─── * Conversation
Conversation 1 ─── * Message
Lead 1 ─── * Activity
Lead 1 ─── * FollowUp
Lead 1 ─── * Notification
```

## 4. Enumerations

Intent: `BUY`, `RENT`, `SELL`, `PROPERTY_ENQUIRY`, `GENERAL_ENQUIRY`, `UNKNOWN`.

Property type: `APARTMENT`, `HOUSE`, `DUPLEX`, `LAND`, `OFFICE`, `COMMERCIAL`, `OTHER`, `UNKNOWN`.

Timeframe: `IMMEDIATE`, `WITHIN_1_MONTH`, `WITHIN_3_MONTHS`, `OVER_3_MONTHS`, `RESEARCHING`, `UNKNOWN`.

Qualification: `LOW`, `MEDIUM`, `HIGH`, `UNKNOWN`.

Urgency: `LOW`, `MEDIUM`, `HIGH`, `UNKNOWN`.

Conversation: `ACTIVE`, `WAITING_FOR_CUSTOMER`, `ESCALATED`, `CLOSED`.

Message sender: `CUSTOMER`, `BOT`, `SALES_AGENT`, `SYSTEM`.

Follow-up: `PENDING`, `COMPLETED`, `CANCELLED`, `OVERDUE`.

Lead status: `NEW`, `CONTACTED`, `QUALIFIED`, `FOLLOW_UP`, `PROPERTY_MATCHED`, `VIEWING_SCHEDULED`, `NEGOTIATION`, `CONVERTED`, `LOST`, `CLOSED`, `NOT_INTERESTED`, `UNQUALIFIED`.

## 5. Data rules

- Use UUIDs or another stable non-sequential identifier.
- Store timestamps in UTC.
- Use `NUMERIC/DECIMAL` for money, never floating point.
- Preserve original customer messages.
- Use nullable fields for genuinely unknown values.
- Avoid destructive deletes for business records; prefer lifecycle/soft-deletion strategies where required.
- Keep `external_message_id` unique when supplied by an external channel.

## 6. Indexing

Index common access paths such as lead status, qualification, assigned user, follow-up due date, conversation ID, customer ID, created timestamps and external message IDs.

## 7. Migrations

Use Alembic. Every schema change must have a migration, be reviewed and be tested against representative data. Never silently change production schema manually.

## 8. Integrity

Foreign keys should enforce valid relationships. Domain validation belongs in application services in addition to database constraints.

## 9. Source-of-truth rule

n8n execution history is workflow evidence, not the business database. Google Sheets is an integration/reporting copy. AI logs are processing evidence. PostgreSQL owns current business state.

## 14. Detailed Entity Rules

### Customers
Represents a person or organization interacting with the system. Contact information should be normalized where possible. A customer may have multiple leads.

### Leads
Represents a sales opportunity. Store current structured requirements and lifecycle state. Do not overwrite the original conversation as a substitute for lead history.

### Conversations
Represents a communication thread. A lead may have one or more conversations depending on product/channel design.

### Messages
Immutable customer, bot, agent and system events. Preserve original text, sender type, timestamps, channel metadata and external IDs where available.

### Lead Activities
Append-only audit-style records for significant state changes, assignments, qualification changes and actions.

### Follow-ups
Stores the intended next action, due time, owner, status and completion information.

### Notifications
Tracks what was sent, to whom, through which channel and whether delivery succeeded.

## 15. Data Integrity

Use foreign keys for required relationships, unique constraints for external IDs where applicable, check constraints for bounded values and transactions for multi-record state changes. Avoid storing monetary values as floating-point numbers.

## 16. Indexing Strategy

Prioritize indexes for:
- lead status and qualification;
- lead owner/assignee;
- follow-up due time/status;
- conversation lead ID;
- message conversation ID + created time;
- external message IDs;
- customer contact identifiers where unique lookup is common.

## 17. Deletion and Retention

Do not hard-delete business history casually. Prefer explicit archival/soft-deletion strategies where required by product and retention policies. Customer privacy requirements should be handled through documented data-retention and deletion procedures.

## 18. Migration Rules

Every schema change requires an Alembic migration, a tested upgrade path and, where applicable, a rollback/recovery plan. Never modify production schema manually as the normal deployment process.
