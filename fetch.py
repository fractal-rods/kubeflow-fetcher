from src.authsession import get_istio_auth_session
from config import config
import requests
import urllib3

urllib3.disable_warnings()

REPOSITORY = "testing"
BRANCH = "main"
MODEL = "model.txt"
EXPERIMENT = "AIF team development experiments"


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


def get_model(token: str):
    url = (
        config.get("LAKEFS_HOST")
        + f"/api/v1/repositories/{REPOSITORY}/refs/{BRANCH}/objects?path={MODEL}"
    )
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"}).json()
    print(response)
    return


def upload_model(token: str):
    url = (
        config.get("LAKEFS_HOST")
        + f"/api/v1/repositories/{REPOSITORY}/branches/{BRANCH}/objects?path={MODEL}"
    )
    with open(MODEL, "rb") as file:
        response = requests.post(
            url,
            files={"content": file},
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        print(response.json())
    return


def start_pipeline():
    pass


def login_to_lakefs() -> str:
    url = config.get("LAKEFS_HOST") + "/api/v1/auth/login"
    response = requests.post(
        url,
        json={
            "access_key_id": config.get("LAKEFS_ID"),
            "secret_access_key": config.get("LAKEFS_TOKEN"),
        },
    )
    body = response.json()
    return body["token"]


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


def get_pipeline_id() -> str:
    response = session.get(
        f"{config['KUBEFLOW_HOST']}/pipeline/apis/v1beta1/pipelines"
    ).json()
    for pipeline in response["pipelines"]:
        if pipeline["name"] == "add_pipeline.yaml":
            return pipeline["id"]
    print("No pipeline found.")
    exit(1)


def run_pipeline(pipeline_id: str, experiment_id: str) -> str:
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


def get_experiment_id() -> str:
    response = session.get(
        f"{config['KUBEFLOW_HOST']}/pipeline/apis/v1beta1/experiments?resource_reference_key.type=NAMESPACE&resource_reference_key.id=oulu-profile",
    )
    print("Using experiment", EXPERIMENT)
    for experiment in response.json()["experiments"]:
        if experiment["name"] == EXPERIMENT:
            return experiment["id"]
    print("Experiment not found.")
    exit(1)


if __name__ == "__main__":
    if check_config():
        print("Configuration OK.")
    session = login_to_kubeflow()
    pipeline_id = get_pipeline_id()
    print(pipeline_id)
    if pipeline_id:
        print("Pipeline OK.")
        experiment_id = get_experiment_id()
        run_id = run_pipeline(pipeline_id, experiment_id)
        print("Started run", run_id)
