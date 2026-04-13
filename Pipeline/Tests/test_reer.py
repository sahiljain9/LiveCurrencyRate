import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Features.REER import WEIGHTS

class TestREER(unittest.TestCase):

    def test_reer_weights_sum(self):
        self.assertAlmostEqual(sum(WEIGHTS.values()), 1.0)

    def test_reer_weights_positive(self):
        for w in WEIGHTS.values():
            self.assertGreater(w, 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)