import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Config import get_conn

def save(table, records):
    """Saves records only if rate has changed since last save."""
    conn   = get_conn()
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT currency_code, rate FROM {table} 
        WHERE id IN (
            SELECT MAX(id) FROM {table} 
            GROUP BY currency_code
        )
    """)
    last_rates = {row[0]: float(row[1]) for row in cursor.fetchall()}
    
    saved = 0
    for r in records:
        last = last_rates.get(r["currency_code"])
        if not last or last != float(r["rate"]):
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