# Testing Specification

## 1. Strategy

Testing must protect the business workflow from the UI through the API, automation, AI boundary and database. Use a pyramid: many unit/service tests, a strong API/integration layer, focused workflow/AI tests, and a smaller number of end-to-end tests.

## 2. Backend tests

Test:
- validation
- service/domain logic
- database repositories
- lifecycle transitions
- qualification calculation
- idempotency
- authorization
- transactions
- API contracts
- error handling

## 3. Frontend tests

Test:
- chat rendering
- forms and validation
- loading/error states
- lead lists/details
- filters
- status actions
- accessibility basics
- responsive behavior

## 4. n8n tests

Each workflow must have happy-path, validation failure, external failure, retry and duplicate-event cases where applicable. Test important node mappings and expected payloads.

## 5. AI evaluation

Golden cases must cover clear, incomplete, ambiguous, contradictory, multi-turn and Nigerian currency/budget enquiries. Verify:
- intent accuracy
- extraction accuracy
- schema validity
- hallucination resistance
- missing-question quality
- escalation behavior
- prompt injection resistance
- response grounding

## 6. End-to-end scenarios

1. Customer sends a detailed buy enquiry.
2. Customer sends incomplete enquiry and supplies missing data later.
3. Duplicate external message arrives.
4. High-value/high-urgency lead triggers sales notification.
5. Customer asks for human agent.
6. Customer requests viewing.
7. Follow-up becomes due.
8. AI provider fails and fallback behavior occurs.
9. Invalid AI JSON is returned.
10. Lead is converted or lost.

## 7. Security testing

Test authentication, authorization, input validation, secret exposure, webhook authentication, prompt injection and access to other customers' leads.

## 8. Performance

Measure API latency, workflow duration, database query performance, AI latency/cost and notification delivery. Establish concrete targets before production load testing.

## 9. CI quality gates

Recommended gates:
- formatting/lint
- type checking where applicable
- unit tests
- API/integration tests
- frontend tests/build
- workflow validation/export checks
- AI regression dataset

## 10. Definition of Done

A feature is done only when its acceptance criteria are tested, regressions are covered, failures are handled, documentation is updated and the relevant automated checks pass.

## 15. Detailed Test Scenarios

### Backend
- create customer and lead;
- update an existing lead from a later message;
- reject invalid lifecycle transition;
- prevent duplicate external messages;
- calculate qualification deterministically;
- enforce authorization;
- verify transaction rollback;
- verify pagination and filtering.

### AI
- “3-bedroom apartment in Lekki for N80m” extracts all key fields;
- “I want a house” identifies missing requirements;
- “below N20m” produces a maximum rather than an exact budget;
- conflicting requirements trigger clarification;
- prompt injection text is treated as customer content, not system instructions;
- malformed provider output is rejected;
- provider timeout reaches safe fallback behavior.

### n8n
Test every workflow with success, malformed payload, duplicate event, downstream timeout, retry exhaustion and recovery scenarios.

### Frontend
Test loading states, validation, empty states, API failures, authenticated access, responsive layout and accessible keyboard interaction.

## 16. Regression Strategy

Every production defect should become a regression test when practical. AI defects should be added to the golden evaluation set. Workflow defects should have representative fixtures that can be replayed safely.

## 17. Release Gate

A release requires passing automated tests, successful database migration checks, critical workflow tests, AI evaluation thresholds, frontend smoke tests, security checks and manual acceptance of the main lead journey.
