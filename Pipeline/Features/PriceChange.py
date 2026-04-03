import pymysql
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def get_conn():
    return pymysql.connect(host="127.0.0.1", port=3306,
        user="root", password="", database="forex_pipeline")
def price_change(currency, rate, conn):
    cursor = conn.cursor()
    cursor.execute( "SELECT rate FROM cleaned_rates WHERE currency_code=%s AND DATE(extracted_at) < CURDATE() ORDER BY id DESC LIMIT 1",(currency,))
    last = cursor.fetchone()
    if not last: return 0.0, "no_data"
    pct = round(((rate - float(last[0])) / float(last[0])) * 100, 4)
    return pct, "UP" if pct > 0 else "Down" if pct < 0 else "Its stable"

if __name__ == "__main__":
    from DataFetch import fetch_rates
    from Extract import extract
    from Clean import clean
    conn    = get_conn()
    cleaned = clean(extract(fetch_rates()))
    for r in cleaned:
        pct, direction = price_change(r["currency_code"], r["rate"], conn)
        print(f"{r['currency_code']} → {pct}% ({direction})")
    conn.close()



