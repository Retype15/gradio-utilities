import unittest
import os
from gradio-utilities.utils import collect_included_files

class TestCollectIncludedFiles(unittest.TestCase):

    def setUp(self):
        # Crear un directorio temporal y archivos de prueba
        self.test_root = "test_dir"
        os.makedirs(self.test_root, exist_ok=True)

        self.files = [
            "file1.txt",
            "file2.json",
            "subdir/file3.py",
        ]
        for file in self.files:
            full_path = os.path.join(self.test_root, file)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w") as f:
                f.write(f"Content of {file}")

    def tearDown(self):
        # Eliminar los archivos de prueba
        for root, dirs, files in os.walk(self.test_root, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(self.test_root)

    def test_collect_included_files(self):
        includes = ["file1.txt", "file2.json", "subdir"]
        result = collect_included_files(self.test_root, includes, recursive=True)
        self.assertEqual(len(result), 3)
        self.assertIn("file1.txt", result)
        self.assertIn("file2.json", result)
        self.assertIn("subdir/file3.py", result)

    def test_filter_extensions(self):
        includes = ["file1.txt", "file2.json", "subdir"]
        result = collect_included_files(
            self.test_root, includes, include_extensions=[".json"]
        )
        self.assertEqual(len(result), 1)
        self.assertIn("file2.json", result)

if __name__ == "__main__":
    unittest.main()
