# n8n Workflows

Orchestration layer for the Real Estate Lead Bot.

**Rule:** n8n orchestrates; FastAPI governs; PostgreSQL is authoritative.

## Workflow Inventory

| ID | Name | Trigger | Responsibility |
|----|------|---------|----------------|
| WF-001 | Lead Intake | Webhook / API event | Receive & normalize messages, call AI extraction, persist via backend |
| WF-002 | Lead Qualification | Lead/message event | Call backend deterministic qualification service |
| WF-003 | Customer Response | Validated conversation event | Generate grounded response, persist bot message |
| WF-004 | Sales Notification | Qualification/status event | Notify sales of actionable leads |
| WF-005 | Human Handoff | Escalation event | Stop bot automation, alert sales |
| WF-006 | Follow-Up Reminder | Schedule | Process due follow-ups |
| WF-007 | Lead Status Sync | Status event | Sync approved state to external systems |
| WF-008 | Conversation Summary | Event / schedule | Maintain concise sales context |
| WF-009 | Error Handler | Workflow failure | Classify, retry, record, escalate |
| WF-010 | Scheduled Maintenance | Cron | Housekeeping & health checks |

See [docs/N8N_WORKFLOW_SPECIFICATION.md](../docs/N8N_WORKFLOW_SPECIFICATION.md) for full contracts.

## Local development

```bash
n8n start
# Import workflow JSON from workflows/ when available
```

Protect webhooks with `N8N_WEBHOOK_SECRET`. Never commit credentials.
