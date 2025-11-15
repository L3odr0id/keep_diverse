import unittest

from keep_diverse.compressed_file_lens import (
    compressed_file_lens_list,
    compressed_file_len,
)


class TestFileCompression(unittest.TestCase):

    def test_compressed_file_len(self):
        import lzma

        btext = None
        file_path = "tests/data/1-seed_11691253499933042360,3128299129089410139.sv"
        with open(file_path, "rb") as f:
            btext = f.read()

        idiomatic_len = len(lzma.compress(btext))
        test_len = compressed_file_len(initial_idx=0, file_path=file_path)[1]

        self.assertEqual(idiomatic_len, test_len)

    def test_compressed_file_lens_list(self):
        file_paths = [
            "tests/data/1-seed_11691253499933042360,3128299129089410139.sv",
            "tests/data/2-seed_13510878130923757581,3128299129089410139.sv",
            "tests/data/3-seed_2167559344450510339,3128299129089410139.sv",
            "tests/data/4-seed_11767764356932420300,3128299129089410139.sv",
            "tests/data/5-seed_2769780858164702270,3128299129089410139.sv",
        ]

        sequential_lens = []
        for i in range(len(file_paths)):
            sequential_lens.append(
                compressed_file_len(initial_idx=i, file_path=file_paths[i])[1]
            )

        parallel_lens = compressed_file_lens_list(file_paths)

        self.assertEqual(sequential_lens, parallel_lens)
