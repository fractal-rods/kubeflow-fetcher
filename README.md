# Development

Create a `.env` and populate it with

```shell
KUBEFLOW_ENDPOINT = ... # address
KUBEFLOW_USERNAME = ... # username
KUBEFLOW_PASSWORD = ... # password
```

then install the required components

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements
```

and run the application

```shell
python3 main.py
```

Happy coding!
