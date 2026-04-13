import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Config import get_conn

def get_volatility(currency, conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT AVG(rate) as daily_rate 
        FROM raw_rates 
        WHERE currency_code = %s
        GROUP BY DATE(extracted_at)
        ORDER BY DATE(extracted_at) DESC
    """, (currency,))
    rates = [float(r[0]) for r in cursor.fetchall()]
    if len(rates) < 2: return 0.0, "insufficient_data"
    avg   = sum(rates)/len(rates)
    vol   = round((sum((r-avg)**2 for r in rates)/len(rates))**0.5, 6)
    label = "stable" if vol<0.001 else "low" if vol<0.01 else "medium" if vol<0.05 else "high"
    return vol, label

if __name__ == "__main__":
    from DataFetch import fetch_rates
    from Extract import extract
    conn    = get_conn()
    raw     = extract(fetch_rates())
    for r in raw:
        vol, label = get_volatility(r["currency_code"], conn)
        print(f"{r['currency_code']} → {vol} ({label})")
    conn.close()