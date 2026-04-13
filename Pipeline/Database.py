import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Config import get_conn

def save(table, records):
    conn   = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        f"SELECT DATE(extracted_at) FROM {table} ORDER BY id DESC LIMIT 1")
    last = cursor.fetchone()
    
    new_date = records[0]["extracted_at"][:10]

    if last and str(last[0]) == new_date:
        print(f"Already saved today — skipped {table}")
        conn.close()
        return

    for r in records:
        cursor.execute(
            f"INSERT INTO {table} (currency_code, rate, extracted_at) VALUES (%s,%s,%s)",
            (r["currency_code"], r["rate"], r["extracted_at"]))
    conn.commit()
    conn.close()
    print(f"Saved {len(records)} records to {table}")

if __name__ == "__main__":
    from DataFetch import fetch_rates
    from Extract import extract
    raw = extract(fetch_rates())
    save("raw_rates", raw)