# API Account and Key Automation

This document specifies how the agent handles creation, verification, storage, and rotation of API accounts and keys. The agent must always adhere to the user’s consent settings and avoid disclosing secrets.

## A. Input Policy Prompt

On first use for each project, the agent asks a series of questions to determine how to manage API accounts and keys:

- **Use master email `<masked@domain>`?** – Confirm whether to use the default masked email for signups.
- **Password policy**: Choose between `generate_strong` (default) or `paste_fixed` (user provides a fixed password).
- **Email access**: Select one of `none`, `read-only`, or `full` (default `none`). Determines if the agent may read verification emails.
- **2FA**: Choose one of `none`, `email_code`, or `totp` (default `none`). Specifies the permitted method for completing two‑factor authentication.
- **Allow the agent to create free‑tier API accounts?** (default `yes`).

## B. Signup Steps (Generic)

1. **Check Free Tier**: Verify that the provider offers a free tier sufficient for the project’s needs. If not, park the step with a list of alternatives.
2. **Navigate to Signup**: Use a web recipe or heuristic to navigate to the provider’s signup page.
3. **Fill Signup Form**: Enter required details, generating a strong password if the policy specifies `generate_strong`.
4. **Email Verification**: If email verification is required and email access is allowed, retrieve the latest code or link by searching the inbox by sender and timestamp. Otherwise, park the signup and request the user to complete verification.
5. **Create API Key**: After account creation, navigate to the provider’s console and generate a new API key.
6. **Store Secret**: Call `secrets.set("PROVIDER_KEY", value)` to store the API key in the local store or vault. The secret is referred to by alias `PROVIDER_KEY` thereafter.
7. **Write Integration Registry Entry**: Record an entry containing the provider name, email used, scope (`personal` or `project`), alias, creation timestamp, and current status.
8. **Sanity Ping**: Make a test call to the provider’s API using the new key and record the result as evidence.

## C. Rotation/Revocation

When a key must be rotated (due to error, expiry, or explicit request):

1. Create a new key in the provider console.
2. Update the secret alias mapping via `secrets.set`.
3. Record an audit entry noting the rotation event (alias and timestamp).
4. Validate the new key by performing a sanity ping.
5. Revoke the old key in the provider console once the new key is confirmed working.

If revocation is requested without immediate replacement, the agent updates the integration registry to mark the alias as inactive and parks any dependent tasks until a new key is provided.
