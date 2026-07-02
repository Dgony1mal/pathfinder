import unittest

from search import bfs
from search import dfs
from search import astar

class TestIntegration(unittest.TestCase):

    def test_all_algorithms(self):

        grid = [
            [0, 0, 0],
            [1, 1, 0],
            [0, 0, 0]
        ]

        bfs_result = bfs(grid, (0, 0), (2, 2))
        dfs_result = dfs(grid, (0, 0), (2, 2))
        astar_result = astar(grid, (0, 0), (2, 2))

        self.assertTrue(bfs_result["found"])
        self.assertTrue(dfs_result["found"])
        self.assertTrue(astar_result["found"])

    def test_same_start_finish(self):

        grid = [
            [0, 0],
            [0, 0]
        ]

        bfs_result = bfs(grid, (0, 0), (0, 0))
        dfs_result = dfs(grid, (0, 0), (0, 0))
        astar_result = astar(grid, (0, 0), (0, 0))

        self.assertEqual(len(bfs_result["path"]), 1)
        self.assertEqual(len(dfs_result["path"]), 1)
        self.assertEqual(len(astar_result["path"]), 1)

    def test_bfs_and_astar_equal(self):

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

if __name__ == "__main__":
    unittest.main()