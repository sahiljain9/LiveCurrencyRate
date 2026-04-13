import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Features.MarketOpen import get_market_session

class TestMarketSession(unittest.TestCase):

    def test_market_session_valid(self):
        session = get_market_session()
        self.assertIn(session, ["asian","european","american","off_peak","overlap"])

    def test_market_session_string(self):
        session = get_market_session()
        self.assertIsInstance(session, str)

if __name__ == "__main__":
    unittest.main(verbosity=2)