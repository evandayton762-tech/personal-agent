import datetime as dt
import os
import tempfile
import unittest
from unittest import mock

from orchestrator.scheduler import Scheduler, CostLedger


class TestScheduler(unittest.TestCase):
    def test_interval_job_runs_and_persists(self):
        """Interval jobs should run immediately, update last_run/next_run, and persist."""
        with tempfile.TemporaryDirectory() as tmp:
            jobs_path = os.path.join(tmp, "jobs.yaml")
            scheduler = Scheduler(jobs_path=jobs_path)
            ran = {"flag": False}

            def task_fn():
                ran["flag"] = True

            scheduler.register("test", task_fn)
            scheduler.add_job({"interval": 0, "task_ref": "test"})
            # Run pending jobs
            scheduler.run_pending()
            self.assertTrue(ran["flag"])
            # last_run recorded
            job = scheduler.jobs[0]
            self.assertIsNotNone(job.get("last_run"))
            # next_run should be populated (may be immediate for zero interval)
            self.assertIsInstance(job.get("next_run"), dt.datetime)
            # Reload scheduler from file and ensure job persists
            scheduler2 = Scheduler(jobs_path=jobs_path)
            self.assertEqual(len(scheduler2.jobs), 1)

    def test_quiet_hours_deferral(self):
        """Jobs due during quiet hours should be deferred to after quiet hours."""
        with tempfile.TemporaryDirectory() as tmp:
            jobs_path = os.path.join(tmp, "jobs.yaml")
            scheduler = Scheduler(jobs_path=jobs_path)
            ran = {"flag": False}

            def task_fn():
                ran["flag"] = True

            scheduler.register("test", task_fn)
            # Create a job due now
            job = {"interval": 0, "task_ref": "test", "next_run": dt.datetime.now()}
            scheduler.jobs.append(job)
            # Force quiet hours by patching _in_quiet_hours to always return True
            with mock.patch.object(scheduler, "_in_quiet_hours", return_value=True):
                scheduler.run_pending()
            # Task should not have run
            self.assertFalse(ran["flag"])
            # next_run should be in the future (deferred)
            self.assertGreater(job["next_run"], dt.datetime.now())

    def test_budget_deferral(self):
        """When daily token cap is exceeded, jobs are deferred to the next day."""
        with tempfile.TemporaryDirectory() as tmp:
            jobs_path = os.path.join(tmp, "jobs.yaml")
            scheduler = Scheduler(jobs_path=jobs_path)
            ran = {"flag": False}

            def task_fn():
                ran["flag"] = True

            scheduler.register("test", task_fn)
            job = {"interval": 0, "task_ref": "test", "next_run": dt.datetime.now()}
            scheduler.jobs.append(job)
            # Patch CostLedger.totals_today to simulate high usage
            with mock.patch.object(CostLedger, "totals_today", return_value={"in_tokens": 30000, "out_tokens": 0, "usd": 0.0}):
                scheduler.run_pending()
            # Task should not have run
            self.assertFalse(ran["flag"])
            # next_run should be deferred by at least 12 hours (tomorrow morning)
            self.assertGreater(job["next_run"], dt.datetime.now() + dt.timedelta(hours=12))


if __name__ == "__main__":
    unittest.main()