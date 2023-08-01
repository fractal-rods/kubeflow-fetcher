from config import config
import requests

REPOSITORY = "fractal"
BRANCH = "uoulu-testing"
MODEL = "model.txt"


def get_data(token: str):
    print("Downloading new model...", end="")
    url = (
        config.get("LAKEFS_HOST")
        + f"/api/v1/repositories/{REPOSITORY}/refs/{BRANCH}/objects?path={MODEL}"
    )
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        print("OK")
    else:
        print("Couldn't download model file:", response.status_code)


def upload_data(token: str):
    print("Uploading model...", end="")
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
    if response.status_code == 201:
        print("OK")
    else:
        print("\nUpload failed:", response.status_code)
        exit(1)


def login_to_lakefs() -> str:
    url = config.get("LAKEFS_HOST") + "/api/v1/auth/login"
    response = requests.post(
        url,
        verify=False,
        json={
            "access_key_id": config.get("LAKEFS_ID"),
            "secret_access_key": config.get("LAKEFS_TOKEN"),
        },
    )
    body = response.json()
    return body["token"]
