import unittest

from search import heuristic

class TestHeuristic(unittest.TestCase):

    def test_zero_distance(self):

        self.assertEqual(
            heuristic((2, 2), (2, 2)),
            0
        )

    def test_distance(self):

        self.assertEqual(
            heuristic((0, 0), (2, 3)),
            5
        )

    def test_symmetric(self):

        self.assertEqual(
            heuristic((1, 4), (5, 2)),
            heuristic((5, 2), (1, 4))
        )

if __name__ == "__main__":
    unittest.main()