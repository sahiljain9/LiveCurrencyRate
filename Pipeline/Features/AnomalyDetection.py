import pymysql
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def get_conn():
    return pymysql.connect(host="127.0.0.1", port=3306,
        user="root", password="", database="forex_pipeline")

def detect_anomaly(currency, rate, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT rate FROM cleaned_rates WHERE currency_code=%s ORDER BY id DESC LIMIT 1", (currency,))
    last = cursor.fetchone()
    if not last: return 0, 0.0
    pct = round(abs((rate - float(last[0])) / float(last[0]) * 100), 4)
    return 1 if pct > 1.0 else 0, pct
if __name__ == "__main__":
    from DataFetch import fetch_rates
    from Extract import extract
    from Clean import clean
    conn    = get_conn()
    cleaned = clean(extract(fetch_rates()))
    for r in cleaned:
        anomaly, pct = detect_anomaly(r["currency_code"], r["rate"], conn)
        status = " ANOMALY" if anomaly else "Normal"
        print(f"{r['currency_code']} → {pct}% {status}")
    conn.close()