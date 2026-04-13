import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Config import get_conn

def detect_anomaly(currency, rate, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT rate FROM raw_rates WHERE currency_code=%s ORDER BY id DESC LIMIT 1", (currency,))
    last = cursor.fetchone()
    if not last: return 0, 0.0
    pct = round(abs((rate - float(last[0])) / float(last[0]) * 100), 4)
    return 1 if pct > 1.0 else 0, pct
if __name__ == "__main__":
    from DataFetch import fetch_rates
    from Extract import extract
    raw = extract(fetch_rates())
    conn    = get_conn()
    for r in raw:
        anomaly, pct = detect_anomaly(r["currency_code"], r["rate"], conn)
        status = " ANOMALY" if anomaly else "Normal"
        print(f"{r['currency_code']} → {pct}% {status}")
    conn.close()