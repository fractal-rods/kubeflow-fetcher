from bottle import Bottle, run
from src.relay.utils import get_mode, check_config, start_pipeline, get_pipeline_status
import logging

logging.captureWarnings(True)
app = Bottle()


@app.get("/pipelines/<run_id>")
def get_status(run_id):
    return get_pipeline_status(run_id)


@app.post("/pipelines")
def initiate():
    RUN_ID = start_pipeline()
    return {"run_id": RUN_ID}


def run_server():
    check_config()
    PRODUCTION_MODE = get_mode()
    if PRODUCTION_MODE:
        run(app, host="0.0.0.0", port=8000, server="paste")
    else:
        run(app, host="localhost", port=8000)
