import os
from src.authsession import get_istio_auth_session
from src.utils import parse_args
import urllib3
import requests

urllib3.disable_warnings()

PIPELINE_NAME = "test-pipeline"

if __name__ == "__main__":
    try:
        HOST = os.environ.get("KUBEFLOW_HOST")
        USER = os.environ.get("KUBEFLOW_USERNAME")
        PASS = os.environ.get("KUBEFLOW_PASSWORD")
        CERTIFICATE = os.environ.get("KUBEFLOW_SSL_CERTIFICATE")
        NAMESPACE = "-"
    except Exception as e:
        print(e)
        exit(1)

    BASEURL = f"{HOST}/pipeline/apis/v1beta1"
    FILENAME = "add_pipeline.yaml"
    args = parse_args()

    # Get cookie from authorization
    auth_session = get_istio_auth_session(url=HOST, username=USER, password=PASS)

    with requests.Session() as session:
        session.headers.update({"Cookie": auth_session["session_cookie"]})
        session.verify = False

    if args.action == "create":
        with open(f"src/pipelines/{FILENAME}", "rb") as file:
            data = {
                "uploadfile": file,
                "name": PIPELINE_NAME,
                "description": "Pipeline for testing \
                        connection and SDK functionality",
            }
            response = session.post(f"{BASEURL}/pipelines/upload", files=data)
            if response.status_code != 201:
                print("Pipeline already exists.")
                exit(1)
            print("Pipeline created.")

    elif args.action == "delete":
        response = session.get(f"{BASEURL}/pipelines").json()
        for pipeline in response["pipelines"]:
            if pipeline["name"] == FILENAME:
                session.delete(f"{BASEURL}/pipelines/{pipeline['id']}")
                print(f"Pipeline {FILENAME} deleted.")
                exit(0)
        print("No pipeline found.")
    elif args.action == "status":
        response = session.get(f"{BASEURL}/pipelines").json()
        for pipeline in response["pipelines"]:
            if pipeline["name"] == FILENAME:
                print(f"Pipeline {FILENAME} exists.")
                exit(0)
        print("No pipeline found.")
        exit(0)
