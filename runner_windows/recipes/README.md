# Recipes Library

Recipes define reusable sequences of actions for interacting with specific websites or applications. Each recipe is stored as a YAML file describing the steps required to complete a common task such as logging in or uploading a document. The runner uses these recipes to reduce reliance on language model tokens and increase determinism.

## YAML Structure

Each recipe YAML file contains top‑level keys such as `login` or a custom `task_name`. Within each key, the structure includes:

- **url**: The starting URL for the recipe.
- **steps[]**: An ordered list of step objects. Each step has:
  - **type**: The kind of action (`wait`, `type`, `click`, `select`, `upload`).
  - **selector**: The CSS selector or UI automation locator (for web recipes).
  - **value**: Optional value to type, select, or upload.
- **success_check**: A selector or condition that must be satisfied to consider the recipe successful (e.g., a dashboard element appearing).

## Variables

Recipes may contain placeholder variables:

- `{{SECRET:ALIAS}}`: Inserts the secret value associated with `ALIAS` at runtime (never stored in the YAML itself).
- `{{PARAM:name}}`: Substitutes a parameter provided by the planner or user.
- `{{STORE_SLUG}}`: A slug generated from a store or project name.

## Policy

Secrets must never be stored directly in the recipe file. Only aliases should appear. On selector failure, the runner saves the current DOM and a screenshot, records a `recipe_diff` note, and requires a recipe update before retrying. This process helps maintain robustness when websites change their layouts.
