FROM python:3.7.3-slim as env

ARG WORK_DIR=/app
ARG FURY_AUTH

WORKDIR $WORK_DIR
ADD Pipfile /app/Pipfile
ADD Pipfile.lock /app/Pipfile.lock
ENV PIP_NO_BINARY=grpcio

RUN pip install pipenv
RUN apt-get update -y && apt-get install -y gcc python-dev build-essential --no-install-recommends && rm -rf /var/lib/apt-lists/*
RUN pipenv install --deploy --dev --system

VOLUME /app

FROM python:3.7.3-slim as app

ARG WORK_DIR=/app
WORKDIR $WORK_DIR


COPY --from=env /usr/local/lib/python3.7 /usr/local/lib/python3.7
COPY . ${WORK_DIR}

ENTRYPOINT ["python", "-m", "src.server"]
