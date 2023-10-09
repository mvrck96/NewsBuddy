"""_summary_

    Returns:
        _type_: _description_
"""
import json
import os
from typing import Dict, List

import requests
from dotenv import find_dotenv, load_dotenv
from prefect import flow, get_run_logger, task
from prefect.deployments import Deployment
from prefect.filesystems import GitHub
from prefect.server.schemas.schedules import CronSchedule
from prefect.task_runners import SequentialTaskRunner
from pydantic import BaseModel

load_dotenv(find_dotenv())

API_MANAGER_DOCKER_PORT = os.environ["API_MANAGER_DOCKER_PORT"]
API_MANAGER_CONTAINER_NAME = os.environ["API_MANAGER_CONTAINER_NAME"]


@task(name="Store to database")
def store_data():
    """_summary_"""
    logger = get_run_logger()
    logger.info("Store to database")


@task(name="send GET to the news API")
def send_request(params: Dict) -> dict:
    """_summary_

    Returns:
        dict: _description_
    """
    logger = get_run_logger()
    endpoint_name = "news"
    url = f"http://{API_MANAGER_CONTAINER_NAME}:{API_MANAGER_DOCKER_PORT}/{endpoint_name}"
    response = requests.get(
        url,
        params=params,
        timeout=300,
    )
    logger.info(f"Request sent to {url}")
    return response.json()


class Parameters(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """

    tickers: List[str] = (None,)
    topics: List[str] = (None,)
    time_from: str = (None,)
    time_to: str = (None,)
    sort: str = ("LATEST",)
    limit: str = (None,)


@flow(
    task_runner=SequentialTaskRunner(),
)
def fetch_news(params: Parameters = None):
    """_summary_"""
    logger = get_run_logger()

    if params:
        params = params.dict()
    else:
        params = {}

    logger.info(f"{params}")

    # Removing None values
    params = {k: v for k, v in params.items() if v is not None}

    response_json = send_request(params=params)
    logger.info(json.dumps(response_json, indent=4))


if __name__ == "__main__":
    # fetch_news()

    PREFECT_BLOCKNAME_GITHUB = os.environ.get("PREFECT_BLOCKNAME_GITHUB")
    # Deploy the prefect workflow
    deployment = Deployment.build_from_flow(
        flow=fetch_news,
        name="main",
        version=1,
        output="deploy.yaml",
        skip_upload=True,
        storage=GitHub.load(PREFECT_BLOCKNAME_GITHUB),
        schedule=CronSchedule(
            cron="0 8 * * *",  # Run the prefect flow at 08:00 every day
            timezone="Europe/Amsterdam",
        ),
        path="./NewsBuddy",
    )
    deployment.apply()
    print(
        "Created Prefect deployment \
      **********************************************************************"
    )
