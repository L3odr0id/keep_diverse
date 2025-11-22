import unittest

from keep_diverse.fast_pct_filter import distances_without_idxs


class TestPCTFilter(unittest.TestCase):

    def test_distances_without_idxs(self):
        old_dist = {
            (0, 1): 1,
            (1, 2): 2,
            (2, 3): 3,
            (3, 4): 4,
            (0, 4): 5,
            (0, 2): 6,
            (2, 4): 7,
        }

        idxs_to_remove = [1, 3]

        new_dist = distances_without_idxs(old_dist, idxs_to_remove)

        expected_dist = {
            (0, 4): 5,
            (0, 2): 6,
            (2, 4): 7,
        }

        self.assertEqual(new_dist, expected_dist)
