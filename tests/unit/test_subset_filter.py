import unittest

from keep_diverse.subset_filter import calc_all_distances, calculate_distance
from keep_diverse.distance import fast_distance
from keep_diverse.compress_lzma import compress_lzma


class TestSubsetFilter(unittest.TestCase):

    def test_calc_all_distances(self):
        files = [(0, "aaaaa"), (1, "bbb"), (2, "cccc")]
        compressed_caches = [10, 21, 42]
        len_01 = compress_lzma(bytes("aaaaa" + "bbb", "utf-8"))
        dist_01 = fast_distance(x_len=10, y_len=21, xy_len=len_01)

        len_12 = compress_lzma(bytes("bbb" + "cccc", "utf-8"))
        dist_12 = fast_distance(x_len=21, y_len=42, xy_len=len_12)

        res = calc_all_distances(
            files=files, subset_compressed_caches=compressed_caches, max_workers=3
        )

        self.assertEqual(res[(0, 1)], dist_01)
        self.assertEqual(res[(1, 2)], dist_12)
