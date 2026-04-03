import pymysql
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def get_conn():
    return pymysql.connect(host="127.0.0.1", port=3306,
        user="root", password="", database="forex_pipeline")
def correlation(c1, c2, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT rate FROM cleaned_rates WHERE currency_code=%s ORDER BY id DESC LIMIT 5", (c1,))
    r1 = [float(r[0]) for r in cursor.fetchall()]
    cursor.execute("SELECT rate FROM cleaned_rates WHERE currency_code=%s ORDER BY id DESC LIMIT 5", (c2,))
    r2 = [float(r[0]) for r in cursor.fetchall()]
    if len(r1) < 2 or len(r2) < 2: return "insufficient_data"
    m1 = [r1[i]-r1[i+1] for i in range(len(r1)-1)]
    m2 = [r2[i]-r2[i+1] for i in range(len(r2)-1)]
    score = round(sum(1 for a,b in zip(m1,m2) if (a>0)==(b>0))/len(m1), 2)
    return score, "high" if score>0.7 else "medium" if score>0.4 else "low"
if __name__ == "__main__":
    from DataFetch import fetch_rates
    from Extract import extract
    from Clean import clean
    conn    = get_conn()
    cleaned = clean(extract(fetch_rates()))
    codes = [r["currency_code"] for r in cleaned 
         if r["currency_code"] != "USD"]
    high_correlations = []
    for i in range(len(codes)):
        for j in range(i+1, len(codes)):
            c1, c2 = codes[i], codes[j]
            result  = correlation(c1, c2, conn)
            if result == "insufficient_data": continue
            score, label = result
            if label == "high":
                high_correlations.append((c1, c2, score))
    print(f"\n Top 20 Correlated Currency Pairs:")
    for c1, c2, score in sorted(high_correlations, key=lambda x: x[2], reverse=True)[:20]:
        print(f"{c1}-{c2} → {score}")
    print(f"\n Total high correlations: {len(high_correlations)}")
    conn.close()
