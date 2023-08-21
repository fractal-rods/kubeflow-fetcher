import requests
from src.authsession import get_istio_auth_session
import os

EXPERIMENT = "AIF team development experiments"
PIPELINE_NAME = "add-pipeline"


def login_to_kubeflow() -> requests.Session:
    with requests.Session() as session:
        auth_session = get_istio_auth_session(
            url=os.environ.get("KUBEFLOW_HOST"),
            username=os.environ.get("KUBEFLOW_USERNAME"),
            password=os.environ.get("KUBEFLOW_PASSWORD"),
        )
        session.verify = False
        session.headers.update({"Cookie": auth_session["session_cookie"]})
        return session


def get_pipeline_id(session: requests.Session) -> str:
    response = session.get(
        f"{os.environ.get('KUBEFLOW_HOST')}/pipeline/apis/v1beta1/pipelines"
    ).json()
    for pipeline in response["pipelines"]:
        if pipeline["name"] == PIPELINE_NAME:
            return pipeline["id"]
    print("No pipeline found.")
    exit(1)


def run_pipeline(
    session: requests.Session, pipeline_id: str, experiment_id: str
) -> str:
    response = session.post(
        f"{os.environ.get('KUBEFLOW_HOST')}/pipeline/apis/v1beta1/runs",
        json={
            "name": "fetcher-test-run",
            "pipeline_spec": {
                "pipeline_id": pipeline_id,
            },
            "resource_references": [
                {
                    "relationship": "OWNER",
                    "key": {
                        "type": "EXPERIMENT",
                        "id": experiment_id,
                    },
                },
            ],
        },
    )

    data = response.json()
    print(data)
    return data["run"]["id"]


def get_experiment_id(session: requests.Session) -> str:
    response = session.get(
        f"{os.environ.get('KUBEFLOW_HOST')}/pipeline/apis/v1beta1/experiments?resource_reference_key.type=NAMESPACE&resource_reference_key.id=oulu-profile",
    )
    print(f"Using experiment '{EXPERIMENT}'")
    for experiment in response.json()["experiments"]:
        if experiment["name"] == EXPERIMENT:
            return experiment["id"]
    print("Experiment not found.")
    exit(1)
