# Packaging and Deployment Models

This document outlines potential packaging models for the personal agent, accommodating both personal use and future monetizable versions. Although implementation details are deferred, the structure defined here ensures current design decisions will not impede future packaging.

## Personal BYOK Desktop

Users run the agent locally with their own keys (Bring Your Own Key). All secrets remain on the user’s machine. Google Docs integration is optional and requires explicit authorization. No telemetry data is collected.

## Hosted Orchestrator + Desktop Runner

For a hosted edition, an orchestrator service manages queues and policies for multiple tenants. Users download a lightweight desktop runner that connects to the orchestrator. A license token authenticates the tenant. Telemetry is opt‑in and limited to performance metrics; BYOK remains optional.

## Licensing

Licenses are managed via Stripe subscriptions. Each license token encodes permitted tasks per day and available skill modules. Tokens are implemented as signed JWTs delivered to the runner and orchestrator.

## Updates

The agent and its components are distributed as signed packages. The system supports rollback in case of issues. A change log accompanies each update so users know what changed.

## Privacy/ToS

Clear privacy and terms of service documentation accompany both personal and hosted editions. Users can export audit logs at any time and review how their data is used. Hosted editions must provide transparency about data flows and allow users to delete their data.
