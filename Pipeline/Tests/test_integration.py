import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class TestIntegration(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_dashboard_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_dashboard_contains_currency(self):
        response = self.client.get("/")
        self.assertIn(b"USD", response.data)

    def test_dashboard_contains_features(self):
        response = self.client.get("/")
        self.assertIn(b"Currency Features", response.data)

    def test_dashboard_contains_crisis(self):
        response = self.client.get("/")
        self.assertIn(b"Crisis Spread Risk", response.data)

    def test_database_connection(self):
        from Config import get_conn
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM raw_rates")
        count = cursor.fetchone()[0]
        conn.close()
        self.assertGreater(count, 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)