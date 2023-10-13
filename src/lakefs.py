import requests
import os

REPOSITORY = "uc4"
BRANCH = "upload-test"
MODEL = "yolov3.weights"
TRAINING_DATA = "training_data.txt"


def login_to_lakefs() -> str:
    url = os.environ.get("LAKEFS_HOST") + "/api/v1/auth/login"
    response = requests.post(
        url,
        verify=False,
        json={
            "access_key_id": os.environ.get("LAKEFS_ID"),
            "secret_access_key": os.environ.get("LAKEFS_TOKEN"),
        },
    )
    body = response.json()
    return body["token"]


def get_data(token: str) -> requests.Response:
    url = (
        os.environ.get("LAKEFS_HOST")
        + f"/api/v1/repositories/{REPOSITORY}/refs/{BRANCH}/objects?path={MODEL}"
    )
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        with open(MODEL, "wb") as file:
            file.write(response.content)
        return response
    else:
        print("Couldn't download model file:", response.status_code)
        exit(1)


def post_data(token: str) -> None:
    print("Uploading training data...", end="")

    url = (
        os.environ.get("LAKEFS_HOST")
        + f"/api/v1/repositories/{REPOSITORY}/branches/{BRANCH}"
        + f"/objects?path={TRAINING_DATA}"
    )

    response = requests.post(
        url,
        files={"content": open(TRAINING_DATA, "rb")},
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    if response.status_code == 201:
        print("OK")
    else:
        print("\nUpload failed:", response.status_code)
        print(response.json())
        exit(1)
