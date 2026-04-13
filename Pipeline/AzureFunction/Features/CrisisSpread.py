import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Config import get_conn
REGIONS = {
    "Middle_East": ["AED","SAR","QAR","KWD","IRR"],
    "Europe"     : ["EUR","GBP","CHF","NOK","SEK"],
    "Asia"       : ["JPY","CNY","INR","KRW","SGD"],
    "Africa"     : ["ZAR","NGN","KES","SDG","EGP"],
    "Americas"   : ["CAD","BRL","MXN","ARS","CLP"],}
def crisis_spread(conn):
    cursor  = conn.cursor()
    results = []
    for region, currencies in REGIONS.items():
        volatile = []
        for c in currencies:
            cursor.execute("SELECT rate FROM raw_rates WHERE currency_code=%s ORDER BY id DESC LIMIT 5", (c,))
            rates = [float(r[0]) for r in cursor.fetchall()]
            if len(rates) < 2: continue
            avg = sum(rates)/len(rates)
            vol = (sum((r-avg)**2 for r in rates)/len(rates))**0.5
            pct_vol = (vol/avg) * 100 
            if pct_vol > 1.0: volatile.append(c) 
        risk = "high" if len(volatile)>2 else "medium" if len(volatile)>0 else "low"
        results.append((region, volatile, risk))
    return results

if __name__ == "__main__":
    conn    = get_conn()
    results = crisis_spread(conn)
    print("\n Crisis Spread Risk:")
    for region, volatile, risk in results:
        print(f"{region:<15} → {risk:<8} | {volatile}")
    conn.close()