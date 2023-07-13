import kfp
from decouple import config
from authsession import get_istio_auth_session

HOST = config("KUBEFLOW_ENDPOINT")
USER = config("KUBEFLOW_USERNAME")
PASS = config("KUBEFLOW_PASSWORD")

auth_session = get_istio_auth_session(url=HOST, username=USER, password=PASS)

print("session: ", auth_session)

client = kfp.Client(
    host=f"{HOST}/pipeline",
    ssl_ca_cert="mycertfile.pem",
    cookies=auth_session["session_cookie"],
)
print("health: ", client.get_kfp_healthz())
print("list exps: ", client.list_experiments(namespace="oulu-profile"))
print("so far so good!")
print("list of pipelines: ", client.list_pipelines())
