import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Config import get_conn

def save(table, records):
    """Saves records only if rate has changed since last save."""
    conn   = get_conn()
    cursor = conn.cursor()
    saved  = 0
    
    for r in records:
        cursor.execute(
            f"SELECT rate FROM {table} WHERE currency_code=%s ORDER BY id DESC LIMIT 1",
            (r["currency_code"],))
        last = cursor.fetchone()
        
        if not last or float(last[0]) != float(r["rate"]):
            cursor.execute(
                f"INSERT INTO {table} (currency_code, rate, extracted_at) VALUES (%s,%s,%s)",
                (r["currency_code"], r["rate"], r["extracted_at"]))
            saved += 1
    
    conn.commit()
    conn.close()
    print(f"Saved {saved} changed records to {table}")

if __name__ == "__main__":
    from DataFetch import fetch_rates
    from Extract import extract
    raw = extract(fetch_rates())
    save("raw_rates", raw)