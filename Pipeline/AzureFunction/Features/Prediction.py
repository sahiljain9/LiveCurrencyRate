import pymysql
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Config import get_conn
def predict(currency, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT rate FROM cleaned_rates WHERE currency_code=%s ORDER BY id DESC LIMIT 5", (currency,))
    rates = [float(r[0]) for r in cursor.fetchall()]
    if len(rates) < 2: return None, "insufficient_data", 0.0
    n     = len(rates)
    x_avg = sum(range(n)) / n
    y_avg = sum(rates) / n
    slope = sum((i-x_avg)*(rates[i]-y_avg) for i in range(n)) / (sum((i-x_avg)**2 for i in range(n)) or 1)
    pred  = round(slope*n + y_avg - slope*x_avg, 6)
    return pred, "up" if pred>rates[0] else "down" if pred<rates[0] else "stable", round(min(n/5,1.0),2)
if __name__ == "__main__":
    from DataFetch import fetch_rates
    from Extract import extract
    from Clean import clean
    conn    = get_conn()
    cleaned = clean(extract(fetch_rates()))
    for r in cleaned:
        pred, direction, conf = predict(r["currency_code"], conn)
        if pred: 
            print(f"{r['currency_code']} → {pred} ({direction})")
    conn.close()