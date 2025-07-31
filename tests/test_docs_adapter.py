import json
import os
import tempfile
import unittest
from unittest import mock

import orchestrator.docs_adapter as docs_adapter


class TestDocsAdapter(unittest.TestCase):
    def test_docs_adapter_without_token_parks(self):
        """When no token file exists, docs adapter should park with oauth_required."""
        with tempfile.TemporaryDirectory() as tmp:
            token_path = os.path.join(tmp, "google_token.json")
            project_log = os.path.join(tmp, "PROJECT_LOG.md")
            # Patch the token and log paths
            with mock.patch.object(docs_adapter, "_TOKEN_PATH", token_path), \
                 mock.patch.object(docs_adapter, "_PROJECT_LOG_PATH", project_log):
                res = docs_adapter.ensure_doc("Test Project")
                self.assertEqual(res["status"], "parked")
                self.assertEqual(res["reason"], "oauth_required")
                # append_section should also park
                res2 = docs_adapter.append_section(res["doc_id"], "Heading", "Content")
                self.assertEqual(res2["status"], "parked")
                self.assertEqual(res2["reason"], "oauth_required")
                # No log file should be created
                self.assertFalse(os.path.exists(project_log))

    def test_docs_adapter_with_token_writes_to_log(self):
        """With a token file present, docs adapter writes to the local log."""
        with tempfile.TemporaryDirectory() as tmp:
            token_path = os.path.join(tmp, "google_token.json")
            project_log = os.path.join(tmp, "PROJECT_LOG.md")
            # Create a fake token file
            with open(token_path, "w", encoding="utf-8") as f:
                json.dump({"access_token": "fake"}, f)
            with mock.patch.object(docs_adapter, "_TOKEN_PATH", token_path), \
                 mock.patch.object(docs_adapter, "_PROJECT_LOG_PATH", project_log):
                # Ensure doc returns ok
                res = docs_adapter.ensure_doc("Test Project")
                self.assertEqual(res["status"], "ok")
                self.assertEqual(res["doc_id"], project_log)
                # Append a section
                docs_adapter.append_section(project_log, "Test Heading", "This is content.")
                # Insert a table
                docs_adapter.insert_table(project_log, [["A", "B"], ["1", "2"]])
                # Insert an image placeholder
                docs_adapter.insert_image(project_log, "path/to/image.png")
                # Link an artifact
                docs_adapter.link_artifact(project_log, "Artifact", "file:///artifact.txt")
                # Update toc
                docs_adapter.update_toc(project_log)
                # Read log file and check contents
                with open(project_log, "r", encoding="utf-8") as f:
                    text = f.read()
                self.assertIn("## Test Heading", text)
                self.assertIn("This is content.", text)
                self.assertIn("| A | B |", text)
                self.assertIn("![Image](path/to/image.png)", text)
                self.assertIn("[Artifact](file:///artifact.txt)", text)


if __name__ == "__main__":
    unittest.main()