# Requirements

- [Python](https://www.python.org/downloads/)
- [Pre-commit](https://pre-commit.com/)

# Usage

<<<<<<< HEAD

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 main.py --help
```

# Development

Create a `config.py` and populate it with:

````shell
config = {
    "LAKEFS_HOST": <...>,
    "LAKEFS_ID": <...>,
    "LAKEFS_TOKEN":<...>,
    "KUBEFLOW_HOST": <...>,
    "KUBEFLOW_USERNAME": <...>,
    "KUBEFLOW_PASSWORD": <...>,
}
=======

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 main.py --help
````

# Development

Create a `.env` and populate it with

```shell
KUBEFLOW_ENDPOINT = ... # address
KUBEFLOW_USERNAME = ... # username
KUBEFLOW_PASSWORD = ... # password
KUBEFLOW_CERTIFICATE = ... # certificate file
>>>>>>> main
```

install the required components

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

then install pre-commit hooks

```shell
pre-commit install
```

Happy coding!
