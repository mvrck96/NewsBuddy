ARG DOCKERFILE_BUILD_IMAGE="python"
ARG DOCKERFILE_BUILD_TAG="3.10-slim-buster"

FROM $DOCKERFILE_BUILD_IMAGE:$DOCKERFILE_BUILD_TAG

ARG USER_ID=1001
ARG GROUP_ID=1001

RUN apt update && \
    apt full-upgrade -y 

RUN python3 -m venv /$APP_NAME/.venv
ENV PATH "/$APP_NAME/.venv/bin:$PATH"

ARG APP_NAME=${APP_NAME:-api-manager}
WORKDIR /$APP_NAME

COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN set -eux && \
    pip install --no-cache-dir --requirement requirements.txt

COPY app.py .
COPY ./tools/ ./tools/

# Remove binary files setuid/setgid
RUN find / -perm /6000 -type f -exec chmod a-s {} \; || true

# Rootless
RUN addgroup --gid $GROUP_ID user && \
  adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID user
USER user

CMD gunicorn app:app --worker-class uvicorn.workers.UvicornWorker\
    --workers 1\
    --bind 0.0.0.0:${API_MANAGER_DOCKER_PORT}
