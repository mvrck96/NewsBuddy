ARG DOCKERFILE_BUILD_IMAGE="python"
ARG DOCKERFILE_BUILD_TAG="3.8-slim-buster"

FROM $DOCKERFILE_BUILD_IMAGE:$DOCKERFILE_BUILD_TAG

ARG USER_ID=1001
ARG GROUP_ID=1001

RUN apt update && \
    apt full-upgrade -y

RUN python3 -m venv /$APP_NAME/.venv
ENV PATH "/$APP_NAME/.venv/bin:$PATH"

ARG APP_NAME=${APP_NAME:-model-service}
WORKDIR /$APP_NAME

COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN set -eux && \
    pip install --no-cache-dir --requirement requirements.txt

COPY app.py .
COPY ./tools/ ./tools/
COPY ./data_models/ ./data_models/
COPY .env .

# Remove binary files setuid/setgid
RUN find / -perm /6000 -type f -exec chmod a-s {} \; || true

# Rootless
RUN addgroup --gid $GROUP_ID user && \
  adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID user
USER user

CMD gunicorn app:app --worker-class uvicorn.workers.UvicornWorker\
    --workers 1\
    --bind 0.0.0.0:8000
