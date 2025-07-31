# Consent Bundle Specification

This file describes the structure of the consent object used by the intake and policy modules. The consent bundle captures user preferences and restrictions about spending, account creation, email access, and live trading. All fields are default‑strict unless the user explicitly relaxes them.

## Consent Fields

- **free_only** (boolean, default `true`): When `true`, the agent must avoid any actions that incur cost unless explicitly overridden.
- **ask_before_spend** (boolean, default `true`): Require user confirmation before any paid action.
- **allow_account_creation** (boolean, default `true`): Whether the agent can create accounts on behalf of the user.
- **allow_email_access** (string, one of `none`, `read-only`, `full`; default `none`): Specifies whether the agent may read or send emails to complete verification steps.
- **allow_2fa** (string, one of `none`, `email_code`, `totp`; default `none`): Determines which forms of two‑factor authentication the agent may assist with.
- **live_trading** (boolean, default `false`): Controls whether the finance adapter may place live trades. Paper trading is used when false.
- **max_daily_llm_usd** (numeric, default `1.00`): The maximum US dollars allowed for language model usage per day. All tokens are costed against this limit.
- **max_daily_third_party_usd** (numeric, default `0.00`): The maximum spending allowed on third‑party services per day.

## Two‑Step Confirmation for Live Trading

Enabling live trading requires two distinct confirmations from the user. The first confirmation acknowledges the request to enable live trading. The second confirmation must be provided at the moment of placing a live order. Without both confirmations, the agent will remain in paper mode and will not execute real trades.
