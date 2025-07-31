# Scheduler Specification

This document describes how recurring and scheduled jobs are stored and executed by the agent’s scheduler.

## Job Store Format

Jobs are persisted in a YAML file named `jobs.yaml`. Each job entry includes:

- **cron | interval**: Either a cron expression or an interval specification indicating when the job should run.
- **task_ref**: A reference to a plan or step to execute when the schedule triggers.
- **constraints**: Additional constraints such as quiet hours or resource restrictions.

## Quiet Hours

The scheduler honors the global quiet hours (02:00–06:00 local) defined in the consent and budget settings. Jobs scheduled to run during quiet hours are deferred until the quiet window ends.

## Jitter

To avoid predictable bursts of activity, the scheduler adds a random jitter of ±2–5 minutes to the scheduled time of each job. This randomization reduces the likelihood of simultaneous execution in multi‑tenant setups.

## Resume on Restart

The job store is persisted to disk. When the runner or orchestrator restarts, previously scheduled jobs are reloaded and resumed. Any jobs that were due during downtime are executed immediately after restart, respecting quiet hours and budgets.

### Example

A nightly job might be defined as:

```
jobs:
  - cron: "10 2 * * *"  # every day at 02:10 local time
    task_ref: nightly_summary
    constraints:
      quiet_hours: true
```

The scheduler will add jitter and ensure that the job runs after quiet hours.
