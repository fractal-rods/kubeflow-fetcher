from config import config
import urllib3
from src.kubeflow.client import (
    get_experiment_id,
    get_pipeline_id,
    login_to_kubeflow,
    run_pipeline,
)
from src.lakefs.client import login_to_lakefs, get_data, upload_data

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
        if not config.get(key):
            print(f"{key} missing from config")
            exit(1)


if __name__ == "__main__":
    if check_config():
        print("Configuration OK.")

    print("connecting to lakefs...")
    token = login_to_lakefs()
    print("connection established")
    upload_data(token)
    get_data(token)

    print("connecting to kubeflow...")
    session = login_to_kubeflow()
    print("connection established")
    pipeline_id = get_pipeline_id(session)
    if pipeline_id:
        print("Pipeline OK.")
        experiment_id = get_experiment_id(session)
        run_id = run_pipeline(session, pipeline_id, experiment_id)
        print("Started run", run_id)
