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

## Milestone M6 — Runner Skeleton

**Date**: 2025-07-31

**Branch**: `feature/m6-runner-skeleton`

### What was done

* Added a new `Runner` class in `runner_windows/runner.py` that connects to the orchestrator’s WebSocket, sends heartbeat messages every 10 seconds, validates incoming steps, dispatches them via a placeholder dispatch table, and implements a kill switch. The runner writes logs to a timestamped file under `runner_windows/logs/` with timestamps and redaction logic.
* Implemented `validate_step` to enforce the allowed set of adapter types and return failure for unknown tools.
* Implemented `dispatch_step` to return a dummy `ok` result with placeholder evidence when not killed. When the kill flag is set, it returns a `failed` result with a `killed` note and logs the event.
* Added a `heartbeat` coroutine that reports runner status and free disk space over the WebSocket.
* Added a `kill()` method to set a flag that causes the next dispatch to return a failure.
* Added unit tests in `tests/test_runner.py` verifying that a valid step is processed and logged correctly, and that the kill switch produces a failed result.
* Added a `.gitignore` file to exclude `__pycache__` directories and `.pyc` files from version control.

### Artifacts

* `runner_windows/runner.py` – implementation of the runner skeleton with heartbeats, dispatch, kill switch, and logging.
* `tests/test_runner.py` – unit tests covering normal dispatch and kill switch behavior.
* `.gitignore` – new file to ignore Python cache directories and compiled bytecode.

### What’s next

Milestone M7 introduces deterministic adapters for file operations and OCR. A new branch `feature/m7-actions-files-ocr` will be created to implement the `files` and `ocr` adapters, including hashing and OCR via Tesseract when available, along with unit tests. After that we will proceed to implement the secrets adapter and web actions.

### Notes

The runner currently processes steps locally without interacting with real actions; dispatch only returns a placeholder result. Future milestones will fill in the dispatch table to call into real adapters such as web, files, and OCR. The kill switch uses an in‑process flag; wiring a global hotkey may require platform‑specific libraries on Windows and will be addressed in later iterations.

## Milestone M7 — Files & OCR Adapters

**Date**: 2025-07-31

**Branch**: `feature/m7-actions-files-ocr`

### What was done

* Implemented the first deterministic adapters in `runner_windows/actions`:
  * `files_adapter.py` provides `write`, `read`, `move`, and `hash_file` functions. Each function returns a dictionary containing the file path and a SHA256 hash to be used in evidence objects.
  * `ocr_adapter.py` provides a placeholder `screenshot` function that parks with a clear reason when screenshot capture is unavailable, and a `read` function that attempts to use `pytesseract` and `Pillow` to perform OCR on an image. When dependencies are missing, the function returns a parked object with reason `tesseract_missing`.
* Added unit tests (`tests/test_actions_files_ocr.py`) that verify:
  * A file can be written, hashed, read, moved, and that the hash remains consistent across the move.
  * The OCR adapter properly reports a parked status when Tesseract/Pillow are not installed and returns text when OCR succeeds (if Tesseract were available).
* Updated the `.gitignore` in a previous commit, which continues to ignore Python cache files.

### Artifacts

* `runner_windows/actions/files_adapter.py` – file operations adapter.
* `runner_windows/actions/ocr_adapter.py` – OCR adapter with missing‑dependency handling.
* `tests/test_actions_files_ocr.py` – unit tests for both adapters.

### What’s next

Milestone M8 focuses on the secrets adapter. We will create `feature/m8-actions-secrets` and implement `secrets.get`, `secrets.set`, and rotation stubs, ensuring that secrets are never logged. Unit tests will verify redaction behavior and missing secrets handling.

### Notes

The OCR adapter currently falls back to a parked state when dependencies are absent. This is acceptable under the free‑only policy, as installing Tesseract would require additional system packages not present in the container. In environments where Tesseract is available, the adapter will return extracted text. Future improvements may provide a more robust screenshot implementation using OS APIs or pyautogui.

## Milestone M8 — Secrets Adapter

**Date**: 2025-07-31

**Branch**: `feature/m8-actions-secrets`

### What was done

* Introduced a secrets adapter in `runner_windows/actions/secrets_adapter.py` with functions `get` and `set`:
  * `get(alias)` searches for a secret alias in environment variables first, then in a local JSON file (`runner_windows/config/secrets.json`). If the alias is not found, it returns a parked dictionary with reason `missing_secret`.
  * `set(alias, value)` stores a secret in the local JSON file without ever logging the value. The secrets file is ignored by Git via an update to `.gitignore`.
* Implemented helper functions to load and save the secrets file, ensuring the directory exists and handling corrupted JSON gracefully.
* Added unit tests (`tests/test_actions_secrets.py`) verifying that:
  * Secrets can be set and retrieved correctly.
  * Missing aliases result in a parked object.
  * When using the `Runner` to log messages that reference an alias, the secret value is not recorded in the log file.
* Updated `.gitignore` to exclude `runner_windows/config/secrets.json` to prevent accidental commits of secret values.

### Artifacts

* `runner_windows/actions/secrets_adapter.py` – secrets adapter implementation.
* `tests/test_actions_secrets.py` – unit tests for secrets handling and log redaction.
* Updated `.gitignore` – now ignoring the secrets JSON file.

### What’s next

Milestone M9 will implement the web adapter using Playwright, persistent profiles, and selector drift handling. A new branch `feature/m9-actions-web` will be created to build functions for opening pages, waiting for selectors, typing, clicking, selecting dropdowns, uploading files, extracting text, and capturing screenshots. Tests will verify basic interactions against a local test page and proper blocking on selector failure.

### Notes

The secrets adapter intentionally writes to a local JSON file outside of version control and never logs secret values. Vault integrations (Bitwarden, 1Password) remain unimplemented and will result in a parked reason if requested. Redaction rules are enforced in tests by checking that secret values do not appear in runner logs.

## Milestone M9 — Web Adapter (Playwright Stub)

**Date**: 2025-07-31

**Branch**: `feature/m9-actions-web`

### What was done

* Added `runner_windows/actions/web_adapter.py` implementing stub functions for web interactions (`open`, `wait`, `type`, `click`, `select`, `upload`, `get_text`, `screenshot`). Each function first checks whether Playwright is installed. Because the environment cannot install Playwright due to network restrictions, the functions return a parked dictionary with reason `playwright_missing` and a descriptive note.
* Created a simple test HTML file at `tests/data/test_page.html` with an input field and a button for potential future Playwright tests.
* Added unit tests in `tests/test_actions_web.py` to verify that each web adapter function returns a parked status when Playwright is unavailable. The tests supply appropriate parameters to each function and assert that the `reason` is `playwright_missing`.

### Artifacts

* `runner_windows/actions/web_adapter.py` – stubbed web adapter with Playwright checks.
* `tests/data/test_page.html` – sample HTML page for future interactive tests.
* `tests/test_actions_web.py` – unit tests for the web adapter stub.

### What’s next

Milestone M10 will introduce the recipes engine. In `feature/m10-recipes-engine`, we will create a YAML loader and executor that maps recipe steps to the appropriate web actions, performs variable substitution, and checks for success. Because Playwright is unavailable, the executor may need to park recipes that require browser automation.

### Notes

The web adapter currently cannot perform real browser actions due to the absence of Playwright in this environment. To comply with the free‑only policy and unavailability of external package installation via the proxy, the adapter parks with a clear reason. Future work could integrate a lightweight HTTP client or enable Playwright installation when network access is restored. The presence of a sample HTML page allows future tests to be enabled without structural changes.

## Milestone M10 — Recipes Engine

**Date**: 2025-07-31

**Branch**: `feature/m10-recipes-engine`

### What was done

* Added a recipe engine in `runner_windows/recipes/engine.py` capable of loading YAML recipes, performing variable expansion for secrets and parameters, and executing actions via the web adapter. The engine handles unsupported or unavailable tools by propagating a parked state.
* Implemented a variable expansion helper that supports `{{SECRET:ALIAS}}` and `{{PARAM:name}}` placeholders, recursively expanding values in dicts and lists. Unknown secrets or parameters expand to empty strings.
* Added an `execute_recipe` function that iterates through recipe steps (`wait`, `type`, `click`, `select`, `upload`), calling the corresponding web adapter functions. If the web adapter parks (e.g., Playwright missing), execution stops and the reason is returned. A simple success_check is included for future use with real browser actions.
* Wrote unit tests (`tests/test_recipes_engine.py`) covering two scenarios:
  * Executing a simple recipe when Playwright is unavailable results in a parked status with reason `playwright_missing`.
  * Variable expansion replaces parameters and secrets correctly and yields empty strings for unknown secrets.

### Artifacts

* `runner_windows/recipes/engine.py` – recipe engine with loading, expansion, and execution logic.
* `tests/test_recipes_engine.py` – tests verifying parked behavior and variable expansion.

### What’s next

Milestone M11 will integrate the cost governor with queue dispatch to enforce budget caps. We will create branch `feature/m11-budget-enforcement` and connect the cost ledger to the orchestrator queue, adding an endpoint for daily budget totals. Tests will validate refusal of steps when caps are exceeded and proper reporting via `/budget/today`.

### Notes

Because Playwright cannot be installed in this environment, the recipe engine currently parks immediately when attempting to open a URL. This still satisfies the specification by properly propagating the parked reason. Once browser automation is available, the engine will execute the steps and enforce success checks. Variable expansion intentionally omits unknown secrets to avoid leaking sensitive information.

## Milestone M11 — Budget Enforcement

**Date**: 2025-07-31

**Branch**: `feature/m11-budget-enforcement`

### What was done

* Integrated the cost ledger into the orchestrator service to enforce daily token caps. Defined `MAX_DAILY_TOKENS`, `WARN_THRESHOLD`, and `STOP_THRESHOLD` constants (25000 tokens, 80 % and 90 % respectively).
* Added a `/budget/today` endpoint returning the aggregated token and USD totals for the current day, the maximum tokens allowed, thresholds, and the used ratio.
* Modified the WebSocket `/ws` endpoint to check the projected token usage before dispatching each step. When dispatching a step would exceed the stop threshold (≥ 90 % of the daily cap), the step is not sent to the runner but is instead appended to the `parked` list with reason `budget` and a `next_try` of “tomorrow”.
* Updated the `/runs` endpoint to include the current budget status, so run summaries reflect token usage.
* Implemented a unit test (`tests/test_budget_enforcement.py`) that preloads the ledger with sufficient tokens to exceed the stop threshold, then enqueues a step and verifies that it is parked and that the budget endpoint reports high usage. The test cleans up the ledger file in `tearDown` to prevent cross‑test contamination.

### Artifacts

* Updated `orchestrator/service.py` – now enforces budget caps on dispatch, records tokens to the ledger after each step, exposes `/budget/today`, and includes budget status in `/runs`.
* `tests/test_budget_enforcement.py` – verifies refusal of a step when the cap is reached and correct budget endpoint behavior.

### What’s next

Milestone M12 introduces the planner using an LLM (mock for now) to generate structured plans based on the intake summary and consent bundle. We will create `feature/m12-planner-structured` to implement a single‑pass planner, validate its output, and downscope plans when estimates exceed caps.

### Notes

Budget enforcement now interacts with the ledger file stored under `memory/cost_ledger.jsonl`. Tests ensure the ledger is reset between runs to avoid interference. Future enhancements may allow configurable caps via the budget configuration file and integrate warning messages when 80 % of the cap is reached. The simplified token estimation still uses static values per adapter type.
