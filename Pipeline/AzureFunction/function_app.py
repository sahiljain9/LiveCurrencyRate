import azure.functions as func
import logging
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from DataFetch import fetch_rates
from Extract import extract
from Database import save
from SaveFeatures import save_features

app = func.FunctionApp()

@app.timer_trigger(schedule="0 0 * * * *",
                   arg_name="myTimer",
                   run_on_startup=True)
def pipeline_trigger(myTimer: func.TimerRequest) -> None:
    logging.info("Pipeline running...")
    raw = extract(fetch_rates())
    save("raw_rates", raw)
    save_features(raw)
    logging.info("Pipeline done!")