import requests
import os

REPOSITORY = "fractal"
BRANCH = "uoulu-testing"
MODEL = "model.txt"


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
    print("Downloading new model...", end="")
    url = (
        os.environ.get("LAKEFS_HOST")
        + f"/api/v1/repositories/{REPOSITORY}/refs/{BRANCH}/objects?path={MODEL}"
    )
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        print("OK")
    else:
        print("Couldn't download model file:", response.status_code)
        exit(1)

    return response


def post_data(token: str) -> None:
    print("Uploading model...", end="")
    url = (
        os.environ.get("LAKEFS_HOST")
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


if __name__ == "__main__":
    # 1.Login
    token = login_to_lakefs()

    # 2.Get data from response and modify it
    response = get_data(token)
    data = response.text
    print("data: " + data)

    data += " ...new data here also"
    print("updated data: " + data)

    # 3.Write the data into a file and send to lakefs
    with open("model.txt", "w") as file:
        file.write(data)

    post_data(token)
