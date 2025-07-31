# Contributing to Personal Agent

Thank you for your interest in contributing! This project follows a strict contribution workflow to ensure quality and protect sensitive information.

## Commit Style

* Make small, logically grouped commits.
* Write clear commit messages following the conventional format: `<type>: <short description>` (e.g., `feat: add intake manager stub`).
* Include a concise body explaining why the change is necessary.

## Pull Request Checklist

When opening a PR:

1. Create your feature branch off of `main` using the naming pattern `feature/<milestone>`.
2. Ensure that CI passes (lint, format, tests).
3. Include a checklist in the PR description that mirrors the acceptance criteria for the milestone.
4. Do not include secrets or sensitive information in commits, PRs, or logs.
5. Reference related issues or milestone numbers in the description.

## Secrets Policy

* Never commit API keys, passwords, or personal data.
* Use aliases defined in the secrets manager; refer to `/docs/secrets.md` for details.
* If a secret is required and missing, park the task and request it through proper channels.

## Code of Conduct

All contributors are expected to adhere to the project's code of conduct. Be respectful and considerate in your interactions.