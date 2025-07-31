"""Simple job scheduler for the personal agent.

This scheduler is designed to persist scheduled jobs to a YAML file and
execute them at the appropriate times while respecting quiet hours and
budget caps. It supports interval and basic cron triggers with jitter
(±2–5 minutes) and persists its job definitions across restarts.

Jobs are stored in ``schedules/jobs.yaml``. Each job entry may include:

* ``cron``: a string in the form ``"M H * * *"`` where M is minute and H is hour.
  Only minute and hour are honored; the other fields are ignored. Wildcards (``*``)
  are permitted for either the minute or hour.
* ``interval``: an integer number of seconds between runs. When set, cron is ignored.
* ``task_ref``: a string identifying the task to run when the trigger fires. The
  scheduler calls a function registered for this name in ``job_functions``.
* ``constraints``: a mapping of additional constraints such as quiet hours.

On instantiation, the scheduler loads all defined jobs from the YAML file and
computes an initial ``next_run`` timestamp for each. Calling ``run_pending()``
executes any jobs whose ``next_run`` timestamp is in the past, provided the
current time is outside the quiet hours (02:00–06:00 local) and the daily
budget cap has not been exceeded.

This scheduler does not create background threads. Instead, clients must
periodically call ``run_pending()`` to execute due jobs. This design simplifies
testing and integration with the orchestrator’s existing event loop.
"""

from __future__ import annotations

import datetime as _dt
import os
import random
import threading
from typing import Any, Callable, Dict, List, Optional

import yaml

from .cost.ledger import CostLedger

# Constants for quiet hours (local time)
QUIET_START_HOUR = 2  # 02:00 local
QUIET_END_HOUR = 6    # 06:00 local

JITTER_MIN = 120  # 2 minutes in seconds
JITTER_MAX = 300  # 5 minutes in seconds

class Scheduler:
    """Job scheduler that reads jobs from a YAML file and executes them."""

    def __init__(self, jobs_path: str = "schedules/jobs.yaml", timezone: str = "America/Phoenix"):
        self.jobs_path = jobs_path
        self.timezone = timezone  # Not currently used; placeholder for future tz handling
        self.job_functions: Dict[str, Callable[[], None]] = {}
        self.jobs: List[Dict[str, Any]] = []
        self.lock = threading.Lock()
        # Instantiate a ledger to check daily token usage
        self._ledger = CostLedger()
        self.load_jobs()

    def register(self, name: str, fn: Callable[[], None]) -> None:
        """Register a callable to be invoked when a job with task_ref == name fires."""
        self.job_functions[name] = fn

    def load_jobs(self) -> None:
        """Load jobs from the YAML file and compute next_run times."""
        if not os.path.exists(self.jobs_path):
            # Nothing to load
            self.jobs = []
            return
        with open(self.jobs_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        self.jobs = []
        for entry in data.get("jobs", []):
            job = dict(entry)  # shallow copy
            # Convert last_run and next_run to datetime objects if present
            if "last_run" in job and isinstance(job["last_run"], str):
                job["last_run"] = _dt.datetime.fromisoformat(job["last_run"])
            if "next_run" in job and isinstance(job["next_run"], str):
                job["next_run"] = _dt.datetime.fromisoformat(job["next_run"])
            # Compute next_run if missing
            if "next_run" not in job:
                job["next_run"] = self._compute_next_run(job)
            self.jobs.append(job)

    def save_jobs(self) -> None:
        """Persist jobs back to the YAML file. Datetimes are serialized as ISO strings."""
        os.makedirs(os.path.dirname(self.jobs_path), exist_ok=True)
        serialized = {"jobs": []}
        for job in self.jobs:
            entry = dict(job)
            # Convert datetimes to ISO format
            if isinstance(entry.get("last_run"), _dt.datetime):
                entry["last_run"] = entry["last_run"].isoformat()
            if isinstance(entry.get("next_run"), _dt.datetime):
                entry["next_run"] = entry["next_run"].isoformat()
            serialized["jobs"].append(entry)
        with open(self.jobs_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(serialized, f)

    def add_job(self, job: Dict[str, Any]) -> None:
        """Add a new job to the scheduler and persist it."""
        with self.lock:
            job = dict(job)
            # Compute initial next_run time
            job["next_run"] = self._compute_next_run(job)
            job.setdefault("last_run", None)
            self.jobs.append(job)
            self.save_jobs()

    def run_pending(self) -> None:
        """Execute all jobs that are scheduled to run at or before now.

        This method applies jitter, quiet hours, and budget checks before executing a job.
        After execution, the job's next_run time is updated and persisted. If a job
        cannot run due to quiet hours or budget caps, its next_run is deferred.
        """
        now = _dt.datetime.now()
        with self.lock:
            for job in self.jobs:
                next_run = job.get("next_run")
                if not isinstance(next_run, _dt.datetime):
                    continue
                if next_run > now:
                    continue
                # Check quiet hours: if current time falls within quiet hours, postpone until end
                if self._in_quiet_hours(now):
                    # postpone to end of quiet hours; if already past the quiet end hour, defer to next day
                    defer_date = now.date()
                    if now.hour >= QUIET_END_HOUR:
                        defer_date = defer_date + _dt.timedelta(days=1)
                    defer_time = _dt.datetime.combine(defer_date, _dt.time(hour=QUIET_END_HOUR))
                    job["next_run"] = self._apply_jitter(defer_time)
                    continue
                # Check budget caps via ledger. totals_today returns dict with keys 'in_tokens', 'out_tokens', 'usd'.
                totals = self._ledger.totals_today()
                # Hardcoded daily token cap for scheduler enforcement (sum of in/out tokens)
                DAILY_TOKENS_CAP = 25000
                used_tokens = totals.get("in_tokens", 0) + totals.get("out_tokens", 0)
                if used_tokens >= DAILY_TOKENS_CAP:
                    # budget exceeded; defer to next day
                    tomorrow = now + _dt.timedelta(days=1)
                    start = tomorrow.replace(hour=QUIET_END_HOUR, minute=0, second=0, microsecond=0)
                    job["next_run"] = self._apply_jitter(start)
                    continue
                # Execute the job
                task_ref = job.get("task_ref")
                fn = self.job_functions.get(task_ref)
                if fn:
                    try:
                        fn()
                    except Exception:
                        # Ignore exceptions in job functions to prevent scheduler crash
                        pass
                job["last_run"] = now
                job["next_run"] = self._compute_next_run(job)
            # Persist updates
            self.save_jobs()

    def _apply_jitter(self, run_time: _dt.datetime) -> _dt.datetime:
        """Apply positive jitter between 2–5 minutes to a scheduled run time.

        To avoid scheduling jobs in the past due to negative jitter, this function
        always adds a random number of seconds between ``JITTER_MIN`` and
        ``JITTER_MAX`` to the provided run time. This ensures the next run
        occurs no earlier than the baseline time.
        """
        jitter_seconds = random.randint(JITTER_MIN, JITTER_MAX)
        return run_time + _dt.timedelta(seconds=jitter_seconds)

    def _compute_next_run(self, job: Dict[str, Any]) -> _dt.datetime:
        """Compute the next run time for a job based on its trigger.

        Supports basic cron (minute and hour) or interval (seconds). When both are
        absent, runs immediately. Applies jitter and ensures the next run is
        outside quiet hours.
        """
        now = _dt.datetime.now()
        interval = job.get("interval")
        cron_expr = job.get("cron")
        next_run: Optional[_dt.datetime] = None
        if interval is not None:
            try:
                seconds = int(interval)
                next_run = now + _dt.timedelta(seconds=seconds)
            except Exception:
                next_run = now
            # Apply jitter only if interval is greater than zero
            if seconds > 0:
                next_run = self._apply_jitter(next_run)
        elif cron_expr:
            # Parse "M H * * *" format
            parts = cron_expr.split()
            if len(parts) >= 2:
                minute_str, hour_str = parts[0], parts[1]
                # Determine next occurrence of the hour/minute; supports '*' wildcard
                # Start from next minute
                candidate = now.replace(second=0, microsecond=0) + _dt.timedelta(minutes=1)
                while True:
                    minute_ok = (minute_str == "*" or int(minute_str) == candidate.minute)
                    hour_ok = (hour_str == "*" or int(hour_str) == candidate.hour)
                    if minute_ok and hour_ok:
                        next_run = candidate
                        break
                    candidate += _dt.timedelta(minutes=1)
            else:
                next_run = now
        else:
            next_run = now
        # For cron or default, apply jitter
        if cron_expr or interval is None:
            next_run = self._apply_jitter(next_run)
        # If next_run falls within quiet hours, adjust to end of quiet hours on same or next day
        if self._in_quiet_hours(next_run):
            # Determine the date for deferment: if the hour is already past QUIET_END_HOUR, defer to next day
            defer_date = next_run.date()
            if next_run.hour >= QUIET_END_HOUR:
                defer_date = defer_date + _dt.timedelta(days=1)
            adjusted = _dt.datetime.combine(defer_date, _dt.time(hour=QUIET_END_HOUR))
            next_run = self._apply_jitter(adjusted)
        return next_run

    def _in_quiet_hours(self, dt: _dt.datetime) -> bool:
        return QUIET_START_HOUR <= dt.hour < QUIET_END_HOUR

    # -------------------------------------------------------------------------
    # Run summary

    def nightly_summary(self) -> None:
        """Append a run summary entry to the project log.

        This method is intended to be registered as a job function with
        ``task_ref='nightly_summary'``. When invoked, it appends a simple
        timestamped summary to the project log. A real implementation would
        gather executed runs, parked items, and budget information. Here we
        record a placeholder entry to demonstrate scheduling.
        """
        log_path = os.path.join("docs", "PROJECT_LOG.md")
        timestamp = _dt.datetime.now().isoformat(timespec="seconds")
        entry = (
            f"\n### Nightly Summary — {timestamp}\n\n"
            "This is an automatically generated summary of runs executed in the last day.\n"
        )
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(entry)
        except Exception:
            # If the log cannot be written (e.g., during tests), ignore silently.
            pass
