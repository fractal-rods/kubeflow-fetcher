import os
from time import sleep, time
import urllib3
from src.lakefs.client import (
    login_to_lakefs,
    get_data,
    post_data,
)
import requests

urllib3.disable_warnings()


def request_run() -> str:
    url = os.environ.get("RELAY_HOST")
    response = requests.post(f"{url}/pipelines")
    return response.json()["run_id"]


def check_status(run_id: str) -> bool:
    url = os.environ.get("RELAY_HOST")
    response = requests.get(f"{url}/pipelines/{run_id}")
    return response.json()["status"] == "Succeeded"


def check_config() -> bool:
    keys = ["LAKEFS_HOST", "LAKEFS_ID", "LAKEFS_TOKEN", "RELAY_HOST"]
    for key in keys:
        if not os.environ.get(key):
            print(f"{key} missing from config")
            exit(1)
        if len(os.environ.get(key)) <= 1:
            print(f"appears that {key} is too short... check if correct")


if __name__ == "__main__":
    if check_config():
        print("Configuration OK.")

    # Step 1. Upload model
    print(end="Connecting to lakefs...", flush=True)
    token = login_to_lakefs()
    print("OK")
    post_data(token)

    # Step 2. Trigger training
    print(end="Requesting run from relay...", flush=True)
    run_id = request_run()
    print("OK")
    print("Waiting for run to complete.")
    start = time()
    while not check_status(run_id):
        now = time()
        print("Run-time {:.2f} seconds.".format(now - start), end="\r")
        sleep(5)
    print("\nRun finished after {:.2f} seconds.".format(now - start))

    # Step 3. Download results
    get_data(token)
    print("FINISHED :--DDD")
