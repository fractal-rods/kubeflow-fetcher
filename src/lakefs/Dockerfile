FROM python:3.10-alpine

WORKDIR /pipelines/component/src

RUN pip install requests

COPY . /pipelines/component/src

CMD [ "python3", "client.py" ]
