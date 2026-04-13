import unittest

class TestCrisisSpread(unittest.TestCase):

    def test_crisis_low(self):
        volatile = []
        risk = "high" if len(volatile)>3 else "medium" if len(volatile)>1 else "low"
        self.assertEqual(risk, "low")

    def test_crisis_medium(self):
        volatile = ["IRR", "SDG"]
        risk = "high" if len(volatile)>3 else "medium" if len(volatile)>1 else "low"
        self.assertEqual(risk, "medium")

    def test_crisis_high(self):
        volatile = ["IRR", "SDG", "ARS", "LBP"]
        risk = "high" if len(volatile)>3 else "medium" if len(volatile)>1 else "low"
        self.assertEqual(risk, "high")

if __name__ == "__main__":
    unittest.main(verbosity=2)