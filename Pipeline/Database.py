import pymysql

def get_conn():
    return pymysql.connect(
        host     = "127.0.0.1",
        port     = 3306,
        user     = "root",
        password = "",
        database = "forex_pipeline"
    )

def save(table, records):
    conn   = get_conn()
    cursor = conn.cursor()
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
    from Clean import clean
    raw = extract(fetch_rates())
    cln = clean(raw)
    save("raw_rates", raw)
    save("cleaned_rates", cln)