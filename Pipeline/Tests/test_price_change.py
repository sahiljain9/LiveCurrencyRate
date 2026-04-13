import unittest

class TestPriceChange(unittest.TestCase):

    def test_price_change_up(self):
        pct = round(((1.1 - 1.0) / 1.0) * 100, 4)
        self.assertGreater(pct, 0)

    def test_price_change_down(self):
        pct = round(((0.9 - 1.0) / 1.0) * 100, 4)
        self.assertLess(pct, 0)

    def test_price_change_stable(self):
        pct = round(((1.0 - 1.0) / 1.0) * 100, 4)
        self.assertEqual(pct, 0.0)

if __name__ == "__main__":
    unittest.main(verbosity=2)