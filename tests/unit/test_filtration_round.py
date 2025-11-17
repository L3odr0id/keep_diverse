import unittest

from keep_diverse.filtration_round import select_subset_compressed_caches, split_list_by


class TestFiltrationRound(unittest.TestCase):

    def test_split_by(self):
        res = split_list_by([1, 2, 3, 4, 5], 2)

        self.assertEqual(res, [[1, 2], [3, 4], [5]])

    def test_subset_compressed_caches(self):
        test_compressed_lens = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110]
        files_set = [(4, "e"), (2, "c"), (0, "a"), (1, "b"), (3, "d")]
        res = select_subset_compressed_caches(
            files_set=files_set,
            compressed_file_lens_cached=test_compressed_lens,
        )

        envtov_revold_michailovich = [104, 102, 100, 101, 103]
        self.assertEqual(res, envtov_revold_michailovich)
