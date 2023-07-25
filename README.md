# Requirements

- [Python](https://www.python.org/downloads/)
- [Pre-commit](https://pre-commit.com/)

# Usage

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 main.py --help
```

# Development

Create a `.env` and populate it with

```shell
KUBEFLOW_ENDPOINT = ... # address
KUBEFLOW_USERNAME = ... # username
KUBEFLOW_PASSWORD = ... # password
KUBEFLOW_CERTIFICATE = ... # certificate file
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
