import unittest

from orchestrator.intake.intake_manager import IntakeManager


class TestIntakeManager(unittest.TestCase):
    def setUp(self):
        self.manager = IntakeManager()
        self.project_name = "test_project"
        self.consent = self.manager.get_consent(self.project_name)

    def test_vague_finance_request_generates_questions_and_becomes_ready(self):
        # Vague spec with only goal and domain
        spec = {
            "goal": "Manage my portfolio",
            "domains": ["finance"],
            "constraints": {},
            "parameters": {},
        }
        iqs, questions, ready = self.manager.assess(spec, self.consent)
        # Should not be ready yet
        self.assertFalse(ready)
        # One batch of questions (<=5)
        self.assertGreater(len(questions), 0)
        self.assertLessEqual(len(questions), 5)
        # Provide answers for all missing fields
        answers = {
            "mode": "paper",
            "universe": ["AAPL", "MSFT"],
            "per_trade_cap": 1000,
            "daily_cap": 5000,
            "data_provider": "alpha_vantage_free",
            "broker": "alpaca_paper",
        }
        spec = self.manager.collect_answers(spec, answers)
        iqs, questions, ready = self.manager.assess(spec, self.consent)
        self.assertTrue(iqs >= 80)
        self.assertTrue(ready)
        # No further questions needed
        self.assertEqual(len(questions), 0)


if __name__ == "__main__":
    unittest.main()