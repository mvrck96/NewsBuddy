ARG DOCKERFILE_BUILD_IMAGE="python"
ARG DOCKERFILE_BUILD_TAG="3.10-slim-buster"

FROM $DOCKERFILE_BUILD_IMAGE:$DOCKERFILE_BUILD_TAG
RUN apt update && pip install --upgrade pip setuptools

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
EXPOSE ${DATA_MANAGER_APP_PORT}
CMD uvicorn app.main:app --port ${DATA_MANAGER_APP_PORT} --reload
