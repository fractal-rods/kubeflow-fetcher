import os
import urllib3
from src.kubeflow_client import (
    get_experiment_id,
    get_pipeline_id,
    login_to_kubeflow,
    run_pipeline,
)
from src.lakefs_client import login_to_lakefs, get_data, post_data

urllib3.disable_warnings()


def check_config() -> bool:
    keys = [
        "LAKEFS_HOST",
        "LAKEFS_ID",
        "LAKEFS_TOKEN",
        "KUBEFLOW_HOST",
        "KUBEFLOW_USERNAME",
        "KUBEFLOW_PASSWORD",
    ]
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
    print(end="Connecting to lakefs...")
    token = login_to_lakefs()
    print("OK")
    post_data(token)

    # Step 2. Trigger training
    print(end="Connecting to kubeflow...")
    session = login_to_kubeflow()
    print("OK")
    pipeline_id = get_pipeline_id(session)
    if pipeline_id:
        experiment_id = get_experiment_id(session)
        run_id = run_pipeline(session, pipeline_id, experiment_id)
        print("Started run", run_id)

        # Step 3. Download results
        get_data(token)
