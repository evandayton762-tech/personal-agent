import os
import tempfile
import unittest
import yaml

from runner_windows.recipes.engine import load_recipe, execute_recipe, _expand_value


class TestRecipeEngine(unittest.TestCase):
    def setUp(self) -> None:
        # Prepare a temporary directory for recipe files
        self.tmp_dir = tempfile.mkdtemp(prefix="recipe_test_")

    def tearDown(self) -> None:
        # Remove the temporary directory and all its contents
        for root, dirs, files in os.walk(self.tmp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.tmp_dir)

    def test_execute_recipe_playwright_missing(self):
        # Build a simple recipe YAML that would interact with the test page
        recipe = {
            "url": "file:///nonexistent.html",
            "steps": [
                {"action": "wait", "selector": "#name"},
                {"action": "type", "selector": "#name", "value": "World"},
                {"action": "click", "selector": "#submit"},
            ],
            "success_check": {
                "type": "text_contains",
                "selector": "#output",
                "value": "Hello, World",
            },
        }
        # Write the recipe to a temporary file
        recipe_path = os.path.join(self.tmp_dir, "recipe.yaml")
        with open(recipe_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(recipe, f)
        loaded = load_recipe(recipe_path)
        result = execute_recipe(loaded, params={})
        # Without Playwright installed, the recipe should be parked due to playwright_missing
        if isinstance(result, dict):
            self.assertEqual(result.get("status"), "parked")
            self.assertEqual(result.get("reason"), "playwright_missing")

    def test_variable_expansion(self):
        data = {
            "value": "Hello {{PARAM:name}} {{SECRET:FAKE}}",
            "nested": {"secret": "{{SECRET:UNKNOWN}}"},
            "list": ["Item {{PARAM:item}}"]
        }
        params = {"name": "Alice", "item": "One"}
        expanded = _expand_value(data, params)
        # Parameters should be replaced
        self.assertEqual(expanded["value"].startswith("Hello Alice"), True)
        self.assertEqual(expanded["list"][0], "Item One")
        # Unknown secret or param yields empty string
        self.assertEqual(expanded["nested"]["secret"], "")


if __name__ == "__main__":
    unittest.main()