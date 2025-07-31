import base64
import os
import unittest

from runner_windows.actions import files_adapter, ocr_adapter


class TestFilesAndOCRAdapters(unittest.TestCase):
    def test_file_write_hash_move(self):
        # Prepare a temporary directory
        tmp_dir = "tmp_test_files"
        os.makedirs(tmp_dir, exist_ok=True)
        src_path = os.path.join(tmp_dir, "sample.txt")
        dst_path = os.path.join(tmp_dir, "moved_sample.txt")

        # Write a text file
        content = "hello world"
        evidence = files_adapter.write(src_path, content)
        self.assertEqual(evidence["path"], src_path)
        # Compute hash separately and ensure it matches
        expected_hash = files_adapter.hash_file(src_path)
        self.assertEqual(evidence["hash"], expected_hash)
        # Read back the file
        read_content = files_adapter.read(src_path)
        self.assertEqual(read_content, content)
        # Move the file
        move_evidence = files_adapter.move(src_path, dst_path)
        self.assertEqual(move_evidence["path"], dst_path)
        # The hash should remain the same after move
        self.assertEqual(move_evidence["hash"], expected_hash)
        # Cleanup
        if os.path.exists(dst_path):
            os.remove(dst_path)
        if os.path.exists(src_path):
            os.remove(src_path)
        os.rmdir(tmp_dir)

    def test_ocr_adapter_read(self):
        # Create a simple PNG file (1x1 white pixel) from base64
        tmp_dir = "tmp_test_ocr"
        os.makedirs(tmp_dir, exist_ok=True)
        image_path = os.path.join(tmp_dir, "sample.png")
        png_base64 = (
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAEklEQVR42mP8/5+hHgAHggJ/"
            "PqRhrwAAAABJRU5ErkJggg=="
        )
        with open(image_path, "wb") as f:
            f.write(base64.b64decode(png_base64))
        result = ocr_adapter.read(image_path)
        # If Tesseract is not available, the adapter should park
        if "status" in result:
            self.assertEqual(result["status"], "parked")
            # Reason should indicate missing tesseract or other error
            self.assertIn(result["reason"], {"tesseract_missing", "ocr_error", "file_not_found"})
        else:
            # When OCR succeeds, text should be a string (may be empty for a blank image)
            self.assertIn("text", result)
            self.assertIsInstance(result["text"], str)
        # Cleanup
        os.remove(image_path)
        os.rmdir(tmp_dir)


if __name__ == "__main__":
    unittest.main()