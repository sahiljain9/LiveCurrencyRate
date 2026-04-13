import unittest

class TestAnomaly(unittest.TestCase):

    def test_anomaly_detected(self):
        pct = abs((1.02 - 1.0) / 1.0 * 100)
        self.assertTrue(pct > 1.0)

    def test_no_anomaly(self):
        pct = abs((1.005 - 1.0) / 1.0 * 100)
        self.assertFalse(pct > 1.0)

if __name__ == "__main__":
    unittest.main(verbosity=2)