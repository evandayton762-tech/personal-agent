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
