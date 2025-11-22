import unittest

from keep_diverse.poisson_metric import poisson_metric_value


class TestMetric(unittest.TestCase):

    def test_poisson_metric_value(self):
        distances_asc = {
            (0, 1): 10.0,
            (0, 2): 100.0,
            (1, 2): 1000.0,
        }

        distances_desc = {
            (1, 2): 1000.0,
            (0, 2): 100.0,
            (0, 1): 10.0,
        }

        val_asc = poisson_metric_value(distances_asc)
        val_desc = poisson_metric_value(distances_desc)

        self.assertAlmostEqual(val_asc - val_desc, 0, delta=1e-6)
