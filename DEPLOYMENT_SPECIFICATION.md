# Deployment Specification

## 1. Environments

- **Development:** local services, n8n local, ngrok only when necessary.
- **Staging:** production-like configuration for integration/UAT.
- **Production:** secured HTTPS deployment with backups, monitoring and controlled access.

## 2. Deployment components

React frontend, FastAPI backend, PostgreSQL, n8n, AI provider and notification/integration providers.

## 3. Production requirements

- HTTPS.
- Secure secrets management.
- Restricted database access.
- Authenticated internal/admin endpoints.
- Protected n8n instance and webhooks.
- Automated backups.
- Logging and alerting.
- Health/readiness checks.

## 4. Deployment order

1. Provision infrastructure/secrets.
2. Deploy/verify PostgreSQL.
3. Run migrations.
4. Deploy backend.
5. Verify health/readiness.
6. Deploy n8n workflows and credentials.
7. Deploy frontend.
8. Run smoke tests.
9. Monitor.

## 5. CI/CD

Recommended pipeline: lint/type checks → tests → build → artifact creation → staging deploy → integration tests → approval → production deploy.

## 6. Migrations

Run migrations as a controlled release step. Back up before risky schema changes. Prefer backward-compatible migrations when application and database versions overlap during rollout.

## 7. Rollback

Rollback application artifacts when safe. Database rollbacks must be planned separately because destructive schema reversal can cause data loss. Prefer forward fixes for production data migrations.

## 8. Backups and restore

Back up PostgreSQL regularly and test restoration. A backup that has never been restored is not sufficient evidence of recoverability.

## 9. Monitoring

Monitor availability, API errors, latency, database health, n8n workflow failures, AI failures/cost, notification delivery and follow-up failures.

## 10. n8n deployment

Export/version workflows, configure credentials securely, verify webhook URLs and test critical workflows after deployment.

## 11. Incident response

Contain the issue, preserve relevant logs, communicate impact, restore service, validate data integrity and document the root cause/follow-up actions.

## 12. Production Definition of Done

Smoke tests pass, migrations are verified, secrets are configured, workflows execute successfully, customer and sales flows work, monitoring is active, backups are verified and rollback steps are known.

## 13. Deployment Sequence

```text
Infrastructure
 → PostgreSQL
 → migrations
 → FastAPI
 → n8n
 → credentials/configuration
 → frontend
 → smoke tests
 → monitoring
```

## 14. Rollback

Application deployments should be reversible. Database migrations must be designed with backward compatibility where practical. If a workflow version is faulty, restore the previously tested workflow definition rather than editing production blindly.

## 15. Backup and Recovery

Backups should be automated, monitored and periodically restored in a non-production environment. A backup that has never been restored should not be treated as proven recovery capability.

## 16. Production Security

Use HTTPS, secret management, least-privilege credentials, restricted administrative access, protected database access and monitored authentication failures. n8n editor access must not be exposed publicly without appropriate protection.
