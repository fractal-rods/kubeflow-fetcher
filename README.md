# Requirements

- [Python](https://www.python.org/downloads/)
- [Pre-commit](https://pre-commit.com/)

# Development

Create a `.env` and populate it with

```shell
KUBEFLOW_ENDPOINT = ... # address
KUBEFLOW_USERNAME = ... # username
KUBEFLOW_PASSWORD = ... # password
```

install the required components

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements
```

then install pre-commit hooks

```shell
pre-commit install
```

and run the application

```shell
python3 main.py
```

Happy coding!
