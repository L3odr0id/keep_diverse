import unittest

from keep_diverse.read_files import read_files, read_one_file


class TestFilesReading(unittest.TestCase):

    def test_read_one_file(self):
        text = None
        file_path = "tests/data/1-seed_11691253499933042360,3128299129089410139.sv"
        with open(file_path, "r") as f:
            text = f.read()

        test_str = read_one_file(file_path, 0)[1]

        self.assertEqual(text, test_str)

    def test_read_files(self):
        file_paths = [
            "tests/data/1-seed_11691253499933042360,3128299129089410139.sv",
            "tests/data/2-seed_13510878130923757581,3128299129089410139.sv",
            "tests/data/3-seed_2167559344450510339,3128299129089410139.sv",
            "tests/data/4-seed_11767764356932420300,3128299129089410139.sv",
            "tests/data/5-seed_2769780858164702270,3128299129089410139.sv",
        ]

        sequential_results = []
        for i in range(len(file_paths)):
            sequential_results.append(read_one_file(file_paths[i], i))

        parallel_results = read_files(enumerate(file_paths))

        self.assertEqual(sequential_results, parallel_results)
