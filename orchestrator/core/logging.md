# Orchestrator Logging Fields

This stub defines the fields included in each log entry created by the orchestrator. These fields support auditability and debugging while ensuring sensitive data is never recorded.

## Log Entry Fields

- **ts**: Timestamp of the action in ISO 8601 format.
- **task_id**: Identifier of the task or project.
- **step_id**: Identifier of the step being executed.
- **tool**: Name of the adapter or tool being invoked (e.g., `web`, `files`).
- **action**: Brief description of the action performed (e.g., `click`, `open`, `hash`).
- **status**: Outcome of the action (`ok`, `retry`, `blocked`, `failed`).
- **evidence_refs**: References to evidence captured during the action (e.g., screenshot IDs, URLs, hashes).

Sensitive values such as secrets or personal data must never appear in logs. Only aliases and identifiers should be used.