import unittest

class TestPrediction(unittest.TestCase):

    def test_prediction_up(self):
        rates = [1.0, 1.1, 1.2, 1.3, 1.4]
        n     = len(rates)
        x_avg = sum(range(n))/n
        y_avg = sum(rates)/n
        slope = sum((i-x_avg)*(rates[i]-y_avg) for i in range(n)) / \
                sum((i-x_avg)**2 for i in range(n))
        pred  = slope*n + y_avg - slope*x_avg
        self.assertGreater(pred, rates[0])

    def test_prediction_down(self):
        rates = [1.4, 1.3, 1.2, 1.1, 1.0]
        n     = len(rates)
        x_avg = sum(range(n))/n
        y_avg = sum(rates)/n
        slope = sum((i-x_avg)*(rates[i]-y_avg) for i in range(n)) / \
                sum((i-x_avg)**2 for i in range(n))
        pred  = slope*n + y_avg - slope*x_avg
        self.assertLess(pred, rates[0])

    def test_prediction_stable(self):
        rates = [1.0, 1.0, 1.0, 1.0, 1.0]
        n     = len(rates)
        x_avg = sum(range(n))/n
        y_avg = sum(rates)/n
        denom = sum((i-x_avg)**2 for i in range(n))
        pred  = rates[0] if denom == 0 else \
                sum((i-x_avg)*(rates[i]-y_avg) for i in range(n))/denom*n + y_avg
        self.assertAlmostEqual(pred, 1.0)

if __name__ == "__main__":
    unittest.main(verbosity=2)