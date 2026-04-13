import unittest

class TestVolatility(unittest.TestCase):

    def test_volatility_stable(self):
        rates = [1.0, 1.0, 1.0, 1.0, 1.0]
        avg   = sum(rates)/len(rates)
        vol   = (sum((r-avg)**2 for r in rates)/len(rates))**0.5
        self.assertEqual(vol, 0.0)

    def test_volatility_high(self):
        rates = [1.0, 1.5, 0.5, 1.8, 0.2]
        avg   = sum(rates)/len(rates)
        vol   = (sum((r-avg)**2 for r in rates)/len(rates))**0.5
        self.assertGreater(vol, 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)