# Audit, History, and Replay

This policy defines how the personal agent records and stores artifacts to enable review, auditing, and replay of tasks.

## Per‑Task Bundle

For each task, the agent creates a bundle directory containing:

- **plan.json**: The serialized `Plan` used for execution.
- **step_results.jsonl**: A JSON lines file containing one entry per step result (`StepResult`).
- **artifacts/**: A folder containing any artifacts produced during execution, such as downloaded files, screenshots, or generated reports.
- **cost_ledger.jsonl**: A JSON lines file recording token and dollar usage per step.

## Replay

Failed steps can be replayed. After updating the underlying recipe or selectors, a single failed step may be rerun without repeating the entire plan. Replay should verify that the updated step now succeeds and produce new evidence.

## Thread‑Style Log Layout

For future UI integration, logs are stored as chronological messages. Each message includes timestamp, persona, action description, evidence references, and any artifacts. This structure allows the user to follow the execution as a conversation thread.

## Export

Upon request, the entire task folder can be zipped and exported. The zip file includes the plan, results, artifacts, cost ledger, and logs. Secret values are never included in the export.
