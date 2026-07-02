import os
import tempfile
import unittest

from file_manager import write_map, read_map

class TestFileManager(unittest.TestCase):

    def test_write_and_read_map(self):

        grid = [
            [2, 0, 0],
            [1, 1, 0],
            [0, 0, 3]
        ]

        with tempfile.NamedTemporaryFile(
            mode="w",
            delete=False,
            suffix=".txt",
            encoding="utf-8"
        ) as file:

            filename = file.name

        write_map(filename, grid)

        loaded = read_map(filename)

        os.remove(filename)

        self.assertEqual(grid, loaded)

    def test_file_created(self):

        with tempfile.NamedTemporaryFile(
            mode="w",
            delete=False,
            suffix=".txt",
            encoding="utf-8"
        ) as file:

            filename = file.name

        self.assertTrue(os.path.exists(filename))

        os.remove(filename)

if __name__ == "__main__":
    unittest.main()