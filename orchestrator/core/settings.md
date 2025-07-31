# Orchestrator Settings Resolution

This stub describes how the orchestrator resolves configuration settings. The actual logic will be implemented in later milestones.

## Config Resolution Order

1. **Environment Variables**: If the `OPENAI_API_KEY` environment variable is set, the orchestrator uses it to access the language model.
2. **Runner Configuration**: If the environment variable is absent, the orchestrator looks up the alias for `OPENAI_API_KEY` in the runner’s `runner.toml` configuration file.
3. **Park Condition**: If the key cannot be resolved from either source, execution is parked with reason `missing_secret`. The user must provide the secret via the secrets manager before proceeding.