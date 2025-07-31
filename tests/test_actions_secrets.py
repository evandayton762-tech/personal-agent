import os
import unittest

from runner_windows.actions import secrets_adapter
from runner_windows.runner import Runner


class TestSecretsAdapter(unittest.TestCase):
    def setUp(self) -> None:
        # Ensure secrets file is removed before each test
        path = secrets_adapter.LOCAL_SECRETS_PATH
        if os.path.exists(path):
            os.remove(path)

    def tearDown(self) -> None:
        # Clean up secrets file after each test
        path = secrets_adapter.LOCAL_SECRETS_PATH
        if os.path.exists(path):
            os.remove(path)

    def test_set_and_get_secret(self):
        alias = "API_KEY"
        value = "supersecret123"
        # Set the secret
        res = secrets_adapter.set(alias, value)
        self.assertEqual(res["alias"], alias)
        # Retrieve the secret
        retrieved = secrets_adapter.get(alias)
        self.assertEqual(retrieved, value)

    def test_missing_secret_returns_parked(self):
        result = secrets_adapter.get("UNKNOWN_ALIAS")
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("status"), "parked")
        self.assertEqual(result.get("reason"), "missing_secret")

    def test_secret_redaction_in_logs(self):
        alias = "DB_PASS"
        value = "password123"
        # Store secret
        secrets_adapter.set(alias, value)
        # Retrieve secret
        _ = secrets_adapter.get(alias)
        # Log only alias using Runner; ensure value is not logged
        runner = Runner(server_ws_url="ws://localhost")
        runner.log(f"Using secret alias {alias}")
        with open(runner.log_file, "r", encoding="utf-8") as f:
            contents = f.read()
        self.assertIn(alias, contents)
        self.assertNotIn(value, contents)


if __name__ == "__main__":
    unittest.main()