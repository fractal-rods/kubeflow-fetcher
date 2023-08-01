import requests
from src.authsession import get_istio_auth_session
from config import config

EXPERIMENT = "AIF team development experiments"


def login_to_kubeflow() -> requests.Session:
    with requests.Session() as session:
        auth_session = get_istio_auth_session(
            url=config["KUBEFLOW_HOST"],
            username=config["KUBEFLOW_USERNAME"],
            password=config["KUBEFLOW_PASSWORD"],
        )
        session.verify = False
        session.headers.update({"Cookie": auth_session["session_cookie"]})
        return session


def get_pipeline_id(session: requests.Session) -> str:
    response = session.get(
        f"{config['KUBEFLOW_HOST']}/pipeline/apis/v1beta1/pipelines"
    ).json()
    for pipeline in response["pipelines"]:
        if pipeline["name"] == "add_pipeline.yaml":
            return pipeline["id"]
    print("No pipeline found.")
    exit(1)


def run_pipeline(
    session: requests.Session, pipeline_id: str, experiment_id: str
) -> str:
    response = session.post(
        f"{config['KUBEFLOW_HOST']}/pipeline/apis/v1beta1/runs",
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
    return data["run"]["id"]


def get_experiment_id(session: requests.Session) -> str:
    response = session.get(
        f"{config['KUBEFLOW_HOST']}/pipeline/apis/v1beta1/experiments?resource_reference_key.type=NAMESPACE&resource_reference_key.id=oulu-profile",
    )
    print("Using experiment", EXPERIMENT)
    for experiment in response.json()["experiments"]:
        if experiment["name"] == EXPERIMENT:
            return experiment["id"]
    print("Experiment not found.")
    exit(1)
