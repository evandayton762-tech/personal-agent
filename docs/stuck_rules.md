# Stuck Rules

These rules outline how the agent behaves when it cannot proceed due to missing information, paywalls, authentication challenges, or other blockers. Each branch describes a specific condition and the corresponding action.

## Missing info

If required information is missing during intake or execution, present default values to the user. If the user declines the defaults or fails to provide the required info, defer the task and issue a ParkedItem with a template for needed inputs.

## Paywall

When encountering a paywall, do not proceed. Park the step with a reason `paywall` and provide the user with a list of free alternatives or suggestions for manual intervention.

## Captcha/2FA

If a website presents a captcha or two‑factor authentication challenge, pause and notify the user. Park the step until the user completes the captcha or provides the necessary code through an approved channel. Resume execution after manual input.

## Selector failure

When a UI selector fails (e.g., element not found), save the DOM and take a screenshot. Record a `recipe_diff` note that the recipe may need updating. Require an update to the recipe before retrying the failed step.

## Near budget cap

If token or monetary usage approaches 90% of the configured cap, defer remaining steps to the next available window. Provide a summary of what remains and schedule continuation after the budget resets.

## Live trade requested without confirmations

Refuse any live trading actions if both confirmations have not been recorded. Request the user to provide the necessary confirmations before proceeding. Until then, operate in paper mode only.
