# Secrets Management

Secrets such as API keys, passwords, tokens, and sensitive configuration must be managed carefully. The agent follows these rules:

1. **Alias References**: All secrets are referenced via aliases (e.g., `ALPHA_VANTAGE_KEY`) instead of raw values. These aliases map to actual values stored locally or in a vault.

2. **No Plaintext in Logs or Docs**: Secrets must never appear in logs, reports, audit trails, or documentation. Only aliases should be recorded.

3. **Storage Locations**: Secrets can be stored in a local configuration file or in a secure vault. The runner’s `runner.toml` specifies whether the vault is enabled. Local files should be access‑controlled and excluded from version control.

4. **Rotation**: When rotating a secret, create a new key in the provider console, update the alias mapping in the secret store, and record an audit entry (without the key itself). After rotation, validate that calls using the new key succeed.

5. **Audit**: Every change to secrets (creation, usage, rotation, revocation) should be logged with a timestamp, the alias affected, and the action taken. Never log the secret value.

6. **Disclosure**: If a task requires a secret that is missing, the system must park the step and ask the user to provide the value through a secure channel before proceeding.
