# Task Specification

## 1. Purpose

Provide a consistent task system for implementing the Real Estate Lead Bot and coordinating human and AI coding work.

## 2. Statuses

`BACKLOG` → `READY` → `IN_PROGRESS` → `IN_REVIEW` → `TESTING` → `DONE`

Exceptions: `BLOCKED`, `CANCELLED`.

## 3. Priorities

- **P0:** critical/MVP blocker.
- **P1:** core MVP.
- **P2:** important but not blocking MVP.
- **P3:** future/improvement.

## 4. Task types

Feature, bug, refactor, documentation, infrastructure, database, AI, n8n, frontend, backend, testing.

## 5. Task template

```markdown
## TASK-XXX — Short title

**Status:** READY
**Priority:** P1
**Owner:**
**Type:**
**Dependencies:**

### Goal

### Context

### Requirements

### Acceptance Criteria
- [ ]

### Implementation Notes

### Tests

### Related Docs
```

## 6. Definition of Ready

A task has a clear outcome, scope, acceptance criteria, dependencies, relevant specification references and enough context for implementation.

## 7. Definition of Done

Code/documentation is complete, tests pass, acceptance criteria are met, security implications are considered and the change is reviewable.

## 8. Dependency rules

Do not start a task whose prerequisite contract/schema is undefined unless the task explicitly includes defining it. Prefer dependency chains over hidden assumptions.

## 9. AI coding agent rules

An AI agent must read the relevant docs before editing code, inspect existing implementation, make focused changes, run tests, report failures honestly and avoid creating duplicate abstractions.

## 10. Examples

- `DB-001` Create initial schema.
- `BE-001` Implement message intake API.
- `AI-001` Implement extraction schema and provider adapter.
- `N8N-001` Implement lead intake workflow.
- `FE-001` Build customer chat.
- `QA-001` Add end-to-end lead flow.
- `OPS-001` Configure staging deployment.

## 11. MVP workstream

Foundation → database → backend → AI → n8n → qualification → customer UI → sales UI → follow-up → testing → deployment.

## 12. Progress reporting

Each task should communicate current status, completed work, blockers, next step and relevant tests. Avoid reporting percentage complete without concrete evidence.

## 13. Commit/PR guidance

Keep commits focused. Reference task IDs. PRs should explain behavior changes, tests, migration impact and any configuration changes.

## 12. Detailed MVP Task Breakdown

### Foundation
- TASK-FND-001 Initialize repository.
- TASK-FND-002 Configure environment variables.
- TASK-FND-003 Create FastAPI application structure.
- TASK-FND-004 Create React application structure.
- TASK-FND-005 Configure local PostgreSQL.
- TASK-FND-006 Configure local n8n.

### Database
- TASK-DB-001 Create customer model.
- TASK-DB-002 Create lead model.
- TASK-DB-003 Create conversation/message models.
- TASK-DB-004 Create activity/follow-up/notification models.
- TASK-DB-005 Add indexes and constraints.
- TASK-DB-006 Create and test migrations.

### AI
- TASK-AI-001 Implement extraction schema.
- TASK-AI-002 Implement provider adapter.
- TASK-AI-003 Validate structured output.
- TASK-AI-004 Build golden test set.
- TASK-AI-005 Implement response generation.

### n8n
- TASK-N8N-001 Lead intake.
- TASK-N8N-002 Qualification.
- TASK-N8N-003 Customer response.
- TASK-N8N-004 Sales notification.
- TASK-N8N-005 Human handoff.
- TASK-N8N-006 Follow-up.
- TASK-N8N-007 Error handler.

### Frontend
- TASK-FE-001 Customer chat.
- TASK-FE-002 Sales lead list.
- TASK-FE-003 Lead detail.
- TASK-FE-004 Follow-up controls.

### QA/Operations
- TASK-QA-001 Backend test suite.
- TASK-QA-002 AI evaluation suite.
- TASK-QA-003 n8n workflow tests.
- TASK-QA-004 E2E lead journey.
- TASK-OPS-001 Staging deployment.
- TASK-OPS-002 Production readiness review.

## 13. Task Dependency Rule

A task should not be marked READY when its required API, database, credential, environment or architectural dependency is undefined. Parallel work is encouraged only when contracts are stable enough to prevent repeated rework.
