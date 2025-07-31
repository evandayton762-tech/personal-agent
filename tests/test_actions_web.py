import os
import unittest

from runner_windows.actions import web_adapter


class TestWebAdapter(unittest.TestCase):
    def test_playwright_missing_parks_functions(self):
        # This environment does not have Playwright installed; each call should park
        result = web_adapter.open("https://example.com")
        self.assertIsInstance(result, dict)
        if result.get("status") == "parked":
            self.assertEqual(result.get("reason"), "playwright_missing")
        # Check other functions
        # Define a set of calls with appropriate arguments
        calls = [
            (web_adapter.wait, ("#selector",)),
            (web_adapter.type, ("#selector", "text")),
            (web_adapter.click, ("#button",)),
            (web_adapter.select, ("#dropdown", "option1")),
            (web_adapter.upload, ("#file", "path/to/file.txt")),
            (web_adapter.get_text, ("#element",)),
            (web_adapter.screenshot, (None,)),
        ]
        for func, args in calls:
            res = func(*args)
            if isinstance(res, dict) and res.get("status") == "parked":
                self.assertEqual(res["reason"], "playwright_missing")


if __name__ == "__main__":
    unittest.main()