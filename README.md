# Requirements

- [Python](https://www.python.org/downloads/)
- [Pre-commit](https://pre-commit.com/)

# Usage

```shell
python3 fetch.py
```

# Development

Create `.env` and populate it with:

```shell
"LAKEFS_HOST"=<...>,
"LAKEFS_ID"=<...>,
"LAKEFS_TOKEN"=<...>,
"KUBEFLOW_HOST"=<...>,
"KUBEFLOW_USERNAME"=<...>,
"KUBEFLOW_PASSWORD"=<...>,
"RELAY_HOST"=<...>
```

Run this command to initialize the .env

```shell
export $(cat .env | xargs)
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
