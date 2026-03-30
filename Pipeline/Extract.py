from datetime import datetime, timezone

def extract(raw_data):
    return [{"currency_code": c, "rate": float(r),
             "extracted_at": datetime.now(timezone.utc).isoformat()}
            for c, r in raw_data["conversion_rates"].items()]

if __name__ == "__main__":
    from DataFetch import fetch_rates
    data = fetch_rates()
    records = extract(data)
    print(f"Extracted {len(records)} currencies")