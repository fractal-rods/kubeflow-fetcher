import kfp
from kfp_server_api.exceptions import ApiException
from decouple import config
from src.authsession import get_istio_auth_session
from src.utils import parse_args
import urllib3

urllib3.disable_warnings()

PIPELINE_NAME = "Addition pipeline"

if __name__ == "__main__":
    try:
        HOST = config("KUBEFLOW_HOST")
        USER = config("KUBEFLOW_USERNAME")
        PASS = config("KUBEFLOW_PASSWORD")
        CERTIFICATE = config("KUBEFLOW_SSL_CERTIFICATE")
    except Exception as e:
        print(e)
        exit(1)

    args = parse_args()

    # Get cookie from authorization
    auth_session = get_istio_auth_session(url=HOST, username=USER, password=PASS)

    # Connect the kubeflow client
    client = kfp.Client(
        host=f"{HOST}/pipeline",
        ssl_ca_cert=CERTIFICATE,
        cookies=auth_session["session_cookie"],
    )

    if args.action == "create":
        try:
            client.upload_pipeline(
                pipeline_name=PIPELINE_NAME,
                description="Pipeline for testing connection and SDK functionality",
                pipeline_package_path="src/pipelines/add_pipeline.yaml",
            )
            print("Pipeline created.")
        except ApiException as e:
            if e.status == 500:
                print("Pipeline already exists.")
            else:
                print(e)
    elif args.action == "delete":
        id = client.get_pipeline_id(PIPELINE_NAME)
        if id:
            client.delete_pipeline(id)
            print(f"Pipeline {id} deleted.")
        else:
            print("No pipeline found.")
    elif args.action == "status":
        id = client.get_pipeline_id(PIPELINE_NAME)
        if id:
            print(f"Pipeline {id} exists.")
        else:
            print("No pipeline found.")
