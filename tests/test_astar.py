import unittest

from search import bfs
from search import astar

class TestAStar(unittest.TestCase):

    def test_find_path(self):

        grid = [
            [0, 0, 0],
            [1, 1, 0],
            [0, 0, 0]
        ]

        result = astar(
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

    def test_same_length_as_bfs(self):

        grid = [
            [0, 0, 0, 0],
            [1, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 1, 1, 0]
        ]

        bfs_result = bfs(
            grid,
            (0, 0),
            (3, 3)
        )

        astar_result = astar(
            grid,
            (0, 0),
            (3, 3)
        )

        self.assertEqual(
            len(bfs_result["path"]),
            len(astar_result["path"])
        )

    def test_no_path(self):

        grid = [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]
        ]

        result = astar(
            grid,
            (0, 0),
            (2, 2)
        )

        self.assertFalse(result["found"])

if __name__ == "__main__":
    unittest.main()