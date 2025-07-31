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
