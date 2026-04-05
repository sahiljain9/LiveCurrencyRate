import schedule
import time
import sys, os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from DataFetch import fetch_rates
from Extract import extract
from Database import save
from SaveFeatures import save_features

def run_pipeline():
    print(f"Pipeline running at {datetime.now()}")
    raw = extract(fetch_rates())
    save("raw_rates", raw)
    save_features(raw)
    print(f"Done!")

run_pipeline()

schedule.every(1).hours.do(run_pipeline)
print("Running every hour!")

while True:
    schedule.run_pending()
    time.sleep(60)