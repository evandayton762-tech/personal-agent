# Project Log

## Milestone M0 — Tooling & Environment

**Date**: 2025-07-31

**Branch**: `feature/devcontainer-ci`

### What was done

* Initialized a local Git repository for the project and created the `feature/devcontainer-ci` branch.
* Added Python 3.11 toolchain management via a minimal `pyproject.toml` using Poetry.
* Created a devcontainer configuration (`.devcontainer/devcontainer.json`) specifying a Python 3.11 base image and commented installation steps for Playwright and Tesseract to respect the free‑only policy.
* Added a GitHub Actions workflow (`.github/workflows/ci.yml`) that checks out the code, sets up Python, installs dependencies with Poetry, and runs placeholder lint, formatting, and no‑op tests.
* Wrote a `CONTRIBUTING.md` outlining commit guidelines, PR checklist, and secrets policy.

### Artifacts

* `pyproject.toml` – defines the Python project and dependencies.
* `.devcontainer/devcontainer.json` – configures the development container.
* `.github/workflows/ci.yml` – sets up continuous integration.
* `CONTRIBUTING.md` – contributor guidelines.

### What’s next

The next milestone (M1) involves creating shared type definitions, settings resolution, and logging interfaces under the core directories. We will create the `feature/core-kernel` branch, add stub documentation for these components, and update the project log accordingly.

### Notes

CI and devcontainer changes were made locally. The remote repository is not configured in this environment, so pushing the branch and opening a PR could not be completed. We will proceed with the next milestones and merge locally until remote access is available.

## Milestone M1 — Shared Types, Settings, and Logging

**Date**: 2025-07-31

**Branch**: `feature/core-kernel`

### What was done

* Created new directories `/orchestrator/core/` and `/runner_windows/core/` to house core documentation.
* Added `types.md` referencing the task envelope specification.
* Added `settings.md` describing how configuration keys like `OPENAI_API_KEY` are resolved, including fallback to `runner.toml` and Park conditions.
* Added `logging.md` defining log entry fields for both orchestrator and runner.
* Added `/docs/STATUS_REPORT_TEMPLATE.md` to standardize status reports after each milestone.

### Artifacts

* `orchestrator/core/types.md` – overview of orchestrator types.
* `orchestrator/core/settings.md` – configuration resolution rules.
* `orchestrator/core/logging.md` – log field definitions.
* `runner_windows/core/types.md` – runner types reference.
* `runner_windows/core/settings.md` – runner settings resolution.
* `runner_windows/core/logging.md` – runner log fields.
* `docs/STATUS_REPORT_TEMPLATE.md` – template for future status reports.

### What’s next

Milestone M2 introduces dataclass or pydantic models for schemas and validators. We will create the `feature/schemas-validators` branch, implement models for the core objects (ProjectSpec, Plan, Step, StepResult, ParkedItem), write validators that enforce required fields and allowed tools, and add unit tests.

### Notes

As before, changes were merged locally into the `main` branch. Remote PR creation is still blocked due to missing repository credentials.

## Milestone M2 — Schemas in Code & Validators

**Date**: 2025-07-31

**Branch**: `feature/schemas-validators`

### What was done

* Implemented dataclasses for the core schemas (`ProjectSpec`, `Plan`, `Step`, `StepResult`, `ParkedItem`) in `orchestrator/core/models.py`.
* Added validation functions in `orchestrator/core/validators.py` to check required fields and ensure adapter types and statuses are allowed.
* Added unit tests using Python’s built‑in `unittest` framework to verify that invalid plans, steps with unknown tools, and step results with invalid statuses are rejected.
* Updated the CI workflow to run the unit tests using `unittest` and removed dependency on `pytest`.

### Artifacts

* `orchestrator/core/models.py` – defines dataclasses for all core objects.
* `orchestrator/core/validators.py` – contains functions `validate_plan`, `validate_step`, `validate_step_result`.
* `tests/test_validators.py` – unit tests covering invalid cases.
* Updated `.github/workflows/ci.yml` to execute `python -m unittest`.

### What’s next

Milestone M3 focuses on the dynamic intake manager. We will create the `feature/intake-manager` branch and implement IQS scoring, MVI definitions per domain, the question batching algorithm, and consent bundle handling. Unit tests will verify that a vague request results in a single batched question and reaches the READY state.

### Notes

Tests run successfully in the local environment using `unittest`. As remote push and PR functionality remain unavailable, we continue to merge branches locally and document progress in the project log.

## Milestone M3 — Intake Manager

**Date**: 2025-07-31

**Branch**: `feature/intake-manager`

### What was done

* Implemented MVI definitions and multiple‑choice options for supported domains in `orchestrator/intake/mvi.py`.
* Added functions for computing the Information Quality Score (IQS) based on completeness, actionability, risk, and ambiguity in `orchestrator/intake/iqs.py`.
* Built a question generator in `orchestrator/intake/questioner.py` that creates batched multiple‑choice or free‑text questions for missing parameters.
* Created a simple consent resolver in `orchestrator/intake/consent.py` returning default consent bundles.
* Implemented `IntakeManager` in `orchestrator/intake/intake_manager.py` to coordinate scoring, question generation, answer application, and readiness determination.
* Added unit tests (`tests/test_intake_manager.py`) verifying that a vague finance request results in one batch of questions and reaches readiness after providing answers.

### Artifacts

* `orchestrator/intake/mvi.py` – MVI definitions and options.
* `orchestrator/intake/iqs.py` – IQS computation.
* `orchestrator/intake/questioner.py` – question generator.
* `orchestrator/intake/consent.py` – default consent resolver.
* `orchestrator/intake/intake_manager.py` – intake manager class.
* `tests/test_intake_manager.py` – unit tests for intake manager functionality.

### What’s next

Milestone M4 introduces the cost governor and ledger. We will create the `feature/cost-governor` branch, implement token estimation per step and plan, tripwire logic, and a cost ledger that records token and monetary usage. Unit tests will ensure downscoping and correct aggregation.

### Notes

The intake manager currently uses simplified heuristics for scoring and expected gain. These will be refined in future iterations. As before, branches are merged locally due to lack of remote connectivity.

## Milestone M4 — Cost Governor & Ledger

**Date**: 2025-07-31

**Branch**: `feature/m4-cost-governor`

### What was done

* Added a cost governor module (`orchestrator/cost/governor.py`) with static token estimation per adapter type and functions to estimate plan tokens and downscope plans when exceeding the per-task token cap.
* Implemented a cost ledger (`orchestrator/cost/ledger.py`) that writes JSONL entries for each executed step and provides aggregated totals for the current day. The ledger creates a `/memory/cost_ledger.jsonl` file automatically.
* Created unit tests (`tests/test_cost_governor.py`) that verify downscoping behavior and correct aggregation of ledger entries.

### Artifacts

* `orchestrator/cost/governor.py` – token estimation and downscoping logic.
* `orchestrator/cost/ledger.py` – ledger implementation with `append()` and `totals_today()` functions.
* `memory/cost_ledger.jsonl` – ledger file (created during runtime).
* `tests/test_cost_governor.py` – tests covering plan downscoping and ledger aggregation.

### What’s next

The next milestone, M5, introduces the skeleton of the orchestrator service with FastAPI endpoints, an in-memory queue, and a WebSocket for step dispatch. We will create the `feature/m5-orchestrator-service` branch to implement these features, including a temporary planner adapter that returns a static plan. A local runner stub will be used to verify connectivity.

### Notes

Static token estimates are conservative placeholders; future improvements will refine them. The ledger path is relative to the repository (`memory/cost_ledger.jsonl`) and ensures that evidence persists across runs.

## Milestone M5 — Orchestrator Service Skeleton

**Date**: 2025-07-31

**Branch**: `feature/m5-orchestrator-service`

### What was done

* Created `orchestrator/service.py` implementing a FastAPI application with the following endpoints:
  - `GET /health` returns a simple status check.
  - `POST /plan` returns a static minimal plan for testing.
  - `POST /enqueue` accepts a plan or step and enqueues the contained steps.
  - `GET /runs` returns a list of executed step results.
  - `GET /parked` returns a list of parked items.
  - `WebSocket /ws` dispatches queued steps to a connected runner and receives `StepResult` objects; results are recorded in runs or parked lists depending on status.
* Implemented in‑memory stores (`queue`, `runs`, `parked`) for managing execution state.
* Added unit tests (`tests/test_orchestrator_service.py`) that verify the health endpoint, plan creation, enqueueing, WebSocket communication for a successful step, and proper handling of blocked steps.

### Artifacts

* `orchestrator/service.py` – FastAPI service skeleton with endpoints and WebSocket handler.
* `tests/test_orchestrator_service.py` – unit tests covering the service’s basic behavior.

### What’s next

Milestone M6 will implement the runner skeleton. We will create the `feature/m6-runner-skeleton` branch, build a runner loop that connects via WebSocket, sends heartbeats, validates steps, dispatches to placeholder actions, and implements a kill switch with logging. Tests will ensure the runner processes a dummy step and logs events correctly.

### Notes

The orchestrator currently returns a hardcoded plan and does not support persistence across restarts. Future milestones will extend the planner and queue functionality, and integrate the cost governor and budget enforcement.
