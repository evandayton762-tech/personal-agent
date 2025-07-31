# Policies

## Free-only policy (default true)

The agent operates under a free-only policy by default. It will utilize only free tiers of services and avoid any actions that incur costs unless explicit consent is obtained from the user.

## Ask-before-spend policy (default true)

Spending money on third‑party services or paid features requires user confirmation. The agent will ask for consent before any cost‑incurring action.

## Token budgets: per_task_token_cap, daily_token_cap

Two token budgets govern the agent's usage of language model tokens: a per‑task cap and a daily cap. These caps help control resource consumption and ensure that execution stays within affordable limits.

## Quiet hours (default 02:00–06:00 local)

The agent respects quiet hours and avoids executing tasks or sending notifications between 02:00 and 06:00 in the user's local timezone (America/Phoenix by default).

## Live‑trading lock (default false; requires 2 confirmations to turn on)

By default, live trading is disabled. To enable live trading, the agent requires two separate confirmations from the user. Without these confirmations, the agent will operate in paper mode only.

## Site/tool allowlist (web, desktop, files, ocr, secrets, schedule, budget, finance, docs)

Only certain categories of tools may be used: web automation, desktop automation, file handling, optical character recognition, secret management, scheduling, budgeting, finance (paper by default), and document integration. Any other tools are disallowed without explicit expansion of this allowlist.

## Evidence requirements (every step must add at least one deterministic check)

Each execution step must produce verifiable evidence. This evidence can include URLs, DOM checks, screenshots, file hashes, or order JSON. The evidence verifies that the agent performed the intended action.

## First‑run supervision for any new website’s submit action

For any new website where the agent attempts to submit a form or complete a transaction, the first run requires human supervision. The agent will pause and request confirmation before submitting, ensuring safe and predictable behavior.
