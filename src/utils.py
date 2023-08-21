from os import getenv
from src.kubeflow import (
    get_istio_auth_session,
    get_pipeline_id,
    run_pipeline,
    get_experiment_id,
)
from requests import Session


def get_session() -> Session:
    auth = get_istio_auth_session(
        url=getenv("KUBEFLOW_HOST"),
        username=getenv("KUBEFLOW_USERNAME"),
        password=getenv("KUBEFLOW_PASSWORD"),
    )
    session = Session()
    session.verify = False
    session.headers.update({"Cookie": auth["session_cookie"]})
    return session


def get_pipeline_status(run_id: str) -> dict:
    url = getenv("KUBEFLOW_HOST")
    session = get_session()
    response = session.get(f"{url}/pipeline/apis/v1beta1/runs/{run_id}")
    data = response.json()
    return data["run"]


def start_pipeline() -> str:
    session = get_session()
    exp_id = get_experiment_id(session)
    pipeline_id = get_pipeline_id(session)
    run_id = run_pipeline(session, pipeline_id, exp_id)
    return run_id


def get_mode() -> bool:
    try:
        prod_str = getenv("PRODUCTION_MODE", "False")
        PRODUCTION_MODE = prod_str.lower() in [
            "true",
            "1",
            "t",
            "yes",
            "y",
            "prod",
            "production",
        ]
        mode = "production" if PRODUCTION_MODE else "development"
    except Exception as e:
        print(e)
        mode = "development"
        PRODUCTION_MODE = False
    finally:
        print(f"Starting in {mode} mode")
    return PRODUCTION_MODE


def check_config():
    keys = ["KUBEFLOW_USERNAME", "KUBEFLOW_PASSWORD", "KUBEFLOW_HOST"]
    for key in keys:
        if getenv(key) is None:
            print(f"Missing env-variable {key}")
            exit(1)
