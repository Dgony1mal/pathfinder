import unittest

from search import dfs

class TestDFS(unittest.TestCase):

    def test_find_path(self):

        grid = [
            [0, 0, 0],
            [1, 1, 0],
            [0, 0, 0]
        ]

        result = dfs(
            grid,
            (0, 0),
            (2, 2)
        )

        self.assertTrue(result["found"])

    def test_no_path(self):

        grid = [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]
        ]

        result = dfs(
            grid,
            (0, 0),
            (2, 2)
        )

        self.assertFalse(result["found"])

if __name__ == "__main__":
    unittest.main()