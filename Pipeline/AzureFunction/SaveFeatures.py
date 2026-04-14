import sys, os
from datetime import datetime, timezone
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Config import get_conn

from DataFetch import fetch_rates
from Extract import extract
from Features.Volatility import get_volatility
from Features.AnomalyDetection import detect_anomaly
from Features.MarketOpen import get_market_session
from Features.PriceChange import price_change
from Features.Prediction import predict
from Features.REER import reer
from Features.Correlation import correlation
from Features.CrisisSpread import crisis_spread

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Config import get_conn

def save_features(records):
    """
    Calculates all features from raw 166 currencies
    and saves to currency_features table.
    """
    conn    = get_conn()
    cursor  = conn.cursor()
    session = get_market_session()
    saved   = 0

    for r in records:
        c, rate        = r["currency_code"], r["rate"]
        vol, _         = get_volatility(c, conn)
        anomaly, _     = detect_anomaly(c, rate, conn)
        pct, _         = price_change(c, rate, conn)
        pred, dire, _  = predict(c, conn)
        rs, rl         = reer(c, conn)
        cursor.execute("""
            INSERT INTO currency_features
            (currency_code, rate, volatility_score, is_anomaly,
             market_session, price_change_pct, predicted_rate,
             prediction_direction, reer_score, reer_label, fetch_timestamp)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (c, rate, vol, anomaly, session, pct, pred, dire, rs, rl,
              datetime.now(timezone.utc).isoformat()))
        saved += 1

    # Save Correlation
    codes = [r["currency_code"] for r in records]
    for i in range(len(codes)):
        for j in range(i+1, len(codes)):
            c1, c2 = codes[i], codes[j]
            result  = correlation(c1, c2, conn)
            if result == "insufficient_data": continue
            score, label = result
            if label == "high":
                cursor.execute("""
                    INSERT INTO currency_correlation
                    (currency1, currency2, score, label, fetch_timestamp)
                    VALUES (%s,%s,%s,%s,%s)
                """, (c1, c2, score, label,
                      datetime.now(timezone.utc).isoformat()))

    # Save Crisis Spread
    results = crisis_spread(conn)
    for region, volatile, risk in results:
        cursor.execute("""
            INSERT INTO crisis_spread
            (region, volatile_currencies, risk_level, fetch_timestamp)
            VALUES (%s,%s,%s,%s)
        """, (region, ",".join(volatile), risk,
              datetime.now(timezone.utc).isoformat()))

    conn.commit()
    conn.close()
    print(f" Saved {saved} records to currency_features!")

if __name__ == "__main__":
    raw = extract(fetch_rates())
    save_features(raw)