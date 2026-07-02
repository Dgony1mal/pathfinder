import unittest

from search import bfs

class TestBFS(unittest.TestCase):

    def test_find_path(self):

        grid = [
            [0, 0, 0],
            [1, 1, 0],
            [0, 0, 0]
        ]

        result = bfs(
            grid,
            (0, 0),
            (2, 2)
        )

        self.assertTrue(result["found"])

        self.assertEqual(
            result["path"][0],
            (0, 0)
        )

        self.assertEqual(
            result["path"][-1],
            (2, 2)
        )

    def test_no_path(self):

        grid = [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]
        ]

        result = bfs(
            grid,
            (0, 0),
            (2, 2)
        )

        self.assertFalse(result["found"])

        self.assertEqual(
            len(result["path"]),
            0
        )

if __name__ == "__main__":
    unittest.main()