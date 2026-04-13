import unittest

class TestCorrelation(unittest.TestCase):

    def test_correlation_perfect(self):
        moves1 = [1, 1, 1, 1]
        moves2 = [1, 1, 1, 1]
        score  = sum(1 for a,b in zip(moves1,moves2) if (a>0)==(b>0))/len(moves1)
        self.assertEqual(score, 1.0)

    def test_correlation_zero(self):
        moves1 = [1, 1, 1, 1]
        moves2 = [-1, -1, -1, -1]
        score  = sum(1 for a,b in zip(moves1,moves2) if (a>0)==(b>0))/len(moves1)
        self.assertEqual(score, 0.0)

    def test_correlation_range(self):
        moves1 = [1, -1, 1, -1]
        moves2 = [1, -1, 1, -1]
        score  = sum(1 for a,b in zip(moves1,moves2) if (a>0)==(b>0))/len(moves1)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)

if __name__ == "__main__":
    unittest.main(verbosity=2)