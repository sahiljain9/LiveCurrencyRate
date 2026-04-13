from flask import Flask, render_template
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Config import get_conn

app = Flask(__name__)

@app.route("/")
def index():
    conn   = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT currency_code, rate FROM raw_rates ORDER BY id DESC LIMIT 166")
    rates = cursor.fetchall()

    cursor.execute("SELECT currency_code, rate, volatility_score, is_anomaly, market_session, price_change_pct, predicted_rate, prediction_direction, reer_score, reer_label FROM currency_features ORDER BY id DESC LIMIT 166")
    features = cursor.fetchall()

    cursor.execute("SELECT region, volatile_currencies, risk_level FROM crisis_spread ORDER BY id DESC LIMIT 5")
    crisis = cursor.fetchall()

    conn.close()
    return render_template("index.html",
        rates=rates, features=features, crisis=crisis)

if __name__ == "__main__":
    app.run(debug=True)