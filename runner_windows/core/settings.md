# Runner Settings Resolution

This stub outlines how the runner resolves configuration for secrets and environment variables.

## Config Resolution Order

1. **Environment Variables**: Check for required keys (e.g., `OPENAI_API_KEY`) in the runner process environment.
2. **Local Config File**: If missing, look up the alias in `runner_windows/config/runner.toml` under the `[auth]` section.
3. **Park Condition**: If the key cannot be found, the runner will park the step, noting that a secret is required.