import kfp
from decouple import config
from authsession import get_istio_auth_session

HOST = config("KUBEFLOW_ENDPOINT")
USER = config("KUBEFLOW_USERNAME")
PASS = config("KUBEFLOW_PASSWORD")

if __name__ == "__main__":
    # Get cookie from authorization
    auth_session = get_istio_auth_session(
        url=HOST,
        username=USER,
        password=PASS
    )

    print("session: ", auth_session)

    # Connect the kubeflow client
    client = kfp.Client(
        host=f"{HOST}/pipeline",
        ssl_ca_cert="mycertfile.pem", 
        cookies=auth_session["session_cookie"]
        )

    client.upload_pipeline(
        pipeline_name="Addition pipeline",
        description="Pipeline for testing connection and SDK functionality",
        pipeline_package_path="pipelines/add_pipeline.yaml"
        )