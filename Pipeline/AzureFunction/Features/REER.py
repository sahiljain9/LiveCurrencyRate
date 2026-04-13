import pymysql
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Config import get_conn
WEIGHTS ={
    "EUR":0.20,"GBP":0.15,"JPY":0.15,
    "CNY":0.12,"CAD":0.10,"CHF":0.08,
    "AUD":0.08,"INR":0.07,"KRW":0.05}
import math

def reer(base, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT rate FROM cleaned_rates WHERE currency_code=%s ORDER BY id DESC LIMIT 1", (base,))
    base_result = cursor.fetchone()
    if not base_result: return 0.0, "no_data"
    base_rate = float(base_result[0])

    total, weight_sum = 0, 0
    for currency, w in WEIGHTS.items():
        if currency == base: continue
        cursor.execute("SELECT rate FROM cleaned_rates WHERE currency_code=%s ORDER BY id DESC LIMIT 1", (currency,))
        r = cursor.fetchone()
        if not r: continue
        ratio = math.log(float(r[0]) + 1) / math.log(base_rate + 1)
        total += w * ratio
        weight_sum += w

    score = round((total/weight_sum)*100, 4) if weight_sum else 0
    return score, "overvalued" if score>110 else "undervalued" if score<90 else "fair_value"

if __name__ == "__main__":
    from DataFetch import fetch_rates
    from Extract import extract
    from Clean import clean
    conn    = get_conn()
    cleaned = clean(extract(fetch_rates()))
    for r in cleaned:
        score, label = reer(r["currency_code"], conn)
        print(f"{r['currency_code']} → {score} ({label})")
    conn.close()