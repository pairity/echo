FROM python:3.7.3-slim as env

ARG WORK_DIR=/app
ARG FURY_AUTH

WORKDIR $WORK_DIR
ADD Pipfile /app/Pipfile
ADD Pipfile.lock /app/Pipfile.lock

RUN pip install pipenv
RUN pipenv install --deploy --dev --system

VOLUME /app

FROM python:3.7.3-slim as app

ARG WORK_DIR=/app
WORKDIR $WORK_DIR

ADD . /app

COPY --from=env /usr/local/lib/python3.7 /usr/local/lib/python3.7

EXPOSE 50052

ENTRYPOINT ["python", "-m", "echo.echo_server"]
