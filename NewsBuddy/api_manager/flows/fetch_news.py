"""_summary_

    Returns:
        _type_: _description_
"""
import os

import requests
from dotenv import find_dotenv, load_dotenv
from prefect import flow, get_run_logger, task
from prefect.deployments import Deployment
from prefect.filesystems import GitHub, LocalFileSystem
from prefect.infrastructure import DockerContainer
from prefect.server.schemas.schedules import CronSchedule
from prefect.task_runners import SequentialTaskRunner

load_dotenv(find_dotenv())

API_MANAGER_DOCKER_PORT = os.environ["API_MANAGER_DOCKER_PORT"]
PREFECT_BLOCKNAME_GITHUB = os.environ.get("PREFECT_BLOCKNAME_GITHUB")
GITHUB_REPO_PATH = os.environ.get("GITHUB_REPO_PATH")
GITHUB_REPO_PATH = "https://github.com/mvrck96/NewsBuddy.git"
GITHUB_REPO_BRANCH = os.environ.get("GITHUB_REPO_BRANCH")


@task(name="send GET to the news API")
def send_request() -> dict:
    """_summary_

    Returns:
        dict: _description_
    """
    logger = get_run_logger()
    endpoint_name = "news"
    IP_ADDRESS = "127.0.0.1"
    url = f"http://{IP_ADDRESS}:{API_MANAGER_DOCKER_PORT}/{endpoint_name}"
    response = requests.get(
        url,
        params=dict(time_from="20230925T1001", time_to="20230925T1201", topics=["technology"]),
        timeout=300,
    )
    logger.info("Request sent...")

    return response.json()


@flow(
    task_runner=SequentialTaskRunner(),
)
def fetch_news():
    """_summary_"""
    response_json = send_request()
    print(response_json)


if __name__ == "__main__":
    fetch_news()

    # # Deploy the prefect workflow
    # deployment = Deployment.build_from_flow(
    #     flow=fetch_news,
    #     name="main",
    #     version=1,
    #     output="deploy.yaml",
    #     # storage=LocalFileSystem(basepath='./NewsBuddy/api_manager/flows/'),
    #     # skip_upload=True,
    #     # storage=GitHub(
    #     #     name=PREFECT_BLOCKNAME_GITHUB,
    #     #     repository=GITHUB_REPO_PATH,
    #     #     include_git_objects=False,
    #     #     reference=GITHUB_REPO_BRANCH,
    #     #     path="NewsBuddy/api_manager/flows/fetch_news.py"
    #     # ),
    #     schedule=CronSchedule(
    #         cron="0 8 * * *",  # Run the prefect flow at 08:00 every day
    #         timezone="Europe/Amsterdam",
    #     ),
    #     # path="fetch_news.py"
    # )
    # deployment.apply()
