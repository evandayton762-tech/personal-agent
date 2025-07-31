# Runner Logging Fields

This stub defines the log fields recorded by the runner for each action. Logs support debugging and audit trails while ensuring secrets are never exposed.

## Log Entry Fields

- **ts**: Timestamp of the action in ISO 8601 format.
- **task_id**: Identifier of the current task.
- **step_id**: Identifier of the step being executed.
- **tool**: Name of the adapter or tool invoked (e.g., `web`, `files`, `ocr`).
- **action**: Description of the action performed (e.g., `type`, `screenshot`).
- **status**: Result of the action (`ok`, `retry`, `blocked`, `failed`).
- **evidence_refs**: Identifiers or hashes referencing captured evidence.

Secrets must be redacted; only aliases may appear in logs.