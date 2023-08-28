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

    with open(MODEL, "wb") as file:
        try:
            with requests.get(
                url, headers={"Authorization": f"Bearer {token}"}, stream=True
            ) as stream:
                total = int(stream.headers.get("content-length", 0))
                current = 0
                stream.raise_for_status()
                for chunk in stream.iter_content(chunk_size=8192):
                    if total is not None and total != 0:
                        current += len(chunk)
                        done = int((50 * current) / total)
                        print(
                            f"[{'=' * done}> {' ' * (50-done)}]", end="\r", flush=True
                        )
                    file.write(chunk)
                print(f"[{'=' *50}][OK]")
        except Exception as e:
            print("Couldn't download model file:", e)
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
