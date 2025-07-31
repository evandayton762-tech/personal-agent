# Specification: Task Envelope and Schemas

This document defines the JSON structures that describe how tasks are specified, planned, executed, and recorded. These models provide a contract between the orchestrator, planner, runner, and reporting layers of the personal agent.

## ProjectSpec (input)

Describes the initial user request. Fields:

- **goal**: A human‑readable description of the user’s objective.
- **domains**: A list of domain tags (e.g., `finance`, `leadgen`, `social`, `jobs`) indicating what skill modules are relevant.
- **constraints**: An object of optional constraints such as `budget`, `schedule`, or `service_limits` that modify how the task should be executed.
- **parameters**: A map of additional parameters required by the domain (e.g., `universe` for finance tasks or `platform` for social posts).

## Plan

A Plan is the output of the planner. It breaks the ProjectSpec into discrete steps and defines how work will proceed through gates. Fields:

- **plan_id**: A unique identifier for this plan instance.
- **gates**: An ordered list of named milestones or checkpoints. Gates may represent major phases; completing a gate implies review or scheduling before proceeding.
- **steps**: An array of Step objects detailing each action. Steps must be ordered; the runner executes them sequentially unless concurrency is explicitly supported.

## Step

Represents a single unit of work. Fields:

- **step_id**: A unique identifier for the step within its plan.
- **team**: The persona responsible for this step (`Governance`, `Planning`, `Research`, `Engineering`, `QA`, `Scheduler`, `Cost`, or `Reporter`).
- **intent**: A short description of what the step aims to accomplish.
- **adapter**: An object describing which tool or adapter will be used. It contains:
  - **type**: One of `web`, `desktop`, `files`, `ocr`, `secrets`, `schedule`, `budget`, `finance`, `docs`.
  - **name**: Optional specific implementation (e.g., `alpaca_paper` for the finance adapter).
- **args**: A JSON object with arguments passed to the adapter.
- **needs_secrets**: A list of secret aliases required before executing this step.
- **evidence**: A list of evidence items collected during execution.
- **budget_tokens**: Estimated token usage for this step.
- **requires_human**: Boolean indicating whether human confirmation is required before or after executing the step.

## StepResult

Captures the outcome of executing a step. Fields:

- **step_id**: Identifier referencing the Step.
- **status**: One of `ok`, `retry`, `blocked`, or `failed`.
- **evidence**: An object containing evidence captured: it may include `urls`, `screenshots`, `dom_checks`, `files`, `hashes`, or `finance` order details.
- **cost**: An object recording tokens consumed and any monetary cost incurred during execution.
- **notes**: Free‑text notes providing context, such as reasons for failure or details of a park condition.

## ParkedItem

Describes a task or step that cannot proceed and is deferred. Fields:

- **reason**: A human‑readable explanation of why the item is parked (e.g., `missing_secret`, `paywall`, `captcha`, `quiet_hours`).
- **proposed_free_alt**: Suggested alternative actions that do not incur costs.
- **requested_info**: A list of specific questions or data needed from the user to unblock the task.
- **next_try**: The time when the system will attempt to resume (may be a timestamp or a scheduled window).

## Evidence Types

Evidence objects may contain the following fields:

- **urls**: An array of URLs visited or resulting from actions.
- **screenshots**: Identifiers for captured screenshots.
- **dom_checks**: Key‑value pairs verifying that specific selectors or text appear in the DOM after an action.
- **files**: Paths or identifiers of files created or modified.
- **hashes**: A map from file paths to their cryptographic hash values (e.g., SHA‑256) to verify file integrity.
- **finance**: An object containing broker order information such as `order_id`, `status`, and `fills` (an array of fill details).