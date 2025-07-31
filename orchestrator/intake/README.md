# Dynamic Intake Manager

This document outlines how the intake subsystem manages conversations with the user to gather just enough information to start planning and executing tasks. The manager follows a state machine, evaluates information quality, and applies question strategies to minimize friction.

## A. State Machine

The intake process moves through these states:

- **INTAKE**: Collecting information from the user.
- **READY**: Enough information is gathered to meet the quality threshold; planning can begin.
- **EXECUTE**: Steps are being executed.
- **PARKED/PAUSED**: Execution is deferred due to missing data, quiet hours, or other blockers.
- **EXECUTE**: Resumes execution after a parked state.
- **DONE**: All steps have completed and the task is finished.

## B. Minimum Viable Input (MVI) by domain

Different domains require different essential parameters to create a viable plan. The intake manager must collect at least these fields:

- **Finance (paper by default)**: `mode` (paper or live), `universe` (allowed symbols), `per_trade_cap`, `daily_cap`, `data_provider`, `broker`.
- **Lead‑gen/Content/Social**: `output_type` (e.g., HTML page, PDF, social post), `platform` (e.g., Webflow, LinkedIn), `asset_source` (user‑supplied or to be generated), `cadence` (one‑time or recurring).
- **Ecommerce**: `platform`, `items_count`, `asset_source`, `pricing_rule` (e.g., cost+markup or fixed price).
- **Outreach/Jobs**: `source_csv/url` (where to find prospects), `profile_data` (resume or company details), `throttle_rules` (max applications per day).

## C. Information Quality Score (IQS 0–100) with weights

Information quality is measured to decide when to stop asking questions. Four components contribute to IQS:

- **Completeness (40%)**: Are all required MVI fields provided?
- **Actionability (30%)**: Does the information allow deterministic execution without ambiguous instructions?
- **Risk (20%)**: Does the task avoid actions that could violate policies or incur unexpected costs?
- **Ambiguity (10%)**: Lower ambiguity increases the score.

Thresholds:

- **≥80**: READY – proceed with planning.
- **60–79**: Ask one batch of clarifying questions.
- **<60**: Defer with presets or examples; do not proceed.

Hard stops include any request that implies spending without consent or initiating live trading without two confirmations.

## D. Question Strategy

The intake manager batches questions into a single message when possible (maximum of five items). The system prefers multiple‑choice questions to guide the user toward valid options. If essential information cannot be captured via choices, a short free‑text question is added. Defaults and presets should be offered and recorded when chosen.

## E. Stop Conditions

The intake ends and transitions to READY when one of the following is met:

- The IQS is 80 or higher.
- The expected IQS gain from additional questions is less than 10 points.
- The intake has consumed 15% or more of the per‑task token cap.

## F. Bad/Low‑effort Answers

If the user provides low‑effort or unusable answers, the system substitutes defaults and presents them for confirmation. Should the user decline or fail to clarify after a second attempt, the intake defers with an example template and records a ParkedItem.
