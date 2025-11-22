import unittest

from .test_file_compression import TestFileCompression
from .test_files_reading import TestFilesReading
from .test_filtration_round import TestFiltrationRound
from .test_subset_filter import TestSubsetFilter
from .test_pct_filter import TestPCTFilter

if __name__ == "__main__":
    suite = unittest.TestSuite()

    loader = unittest.TestLoader()
    test_cases = [
        TestFileCompression,
        TestFilesReading,
        TestFiltrationRound,
        TestSubsetFilter,
        TestPCTFilter,
    ]

    for test_case in test_cases:
        suite.addTests(loader.loadTestsFromTestCase(test_case))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
