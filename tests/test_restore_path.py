import unittest

from search import restore_path

class TestRestorePath(unittest.TestCase):

    def test_restore(self):

        parents = {
            (0, 1): (0, 0),
            (0, 2): (0, 1),
            (1, 2): (0, 2)
        }

        path = restore_path(
            parents,
            (0, 0),
            (1, 2)
        )

        self.assertEqual(
            path,
            [
                (0, 0),
                (0, 1),
                (0, 2),
                (1, 2)
            ]
        )

if __name__ == "__main__":
    unittest.main()