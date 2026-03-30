def clean(records):
    dups = ["GGP","IMP","JEP","FKP","KID","TVD"]
    cleaned = [r for r in records if r["rate"] > 0
               and r["currency_code"] not in dups]
    print(f"Cleaned: {len(cleaned)} currencies")
    return cleaned

if __name__ == "__main__":
    from DataFetch import fetch_rates
    from Extract import extract
    cleaned = clean(extract(fetch_rates()))