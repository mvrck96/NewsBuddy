"""_summary_

    Returns:
        _type_: _description_
"""
import os

import requests
from dotenv import load_dotenv
from prefect import flow, get_run_logger, task
from prefect.deployments import Deployment
from prefect.filesystems import GitHub
from prefect.server.schemas.schedules import CronSchedule
from prefect.task_runners import SequentialTaskRunner

load_dotenv()

# query= 'function=NEWS_SENTIMENT&apikey=3NR4AHAG23T6IGFJ&sort=LATEST&limit=50'
# print(response.text)

API_MANAGER_DOCKER_PORT = os.environ["API_MANAGER_DOCKER_PORT"]
PREFECT_BLOCKNAME_GITHUB = os.environ.get("PREFECT_BLOCKNAME_GITHUB")


@task(name="send GET to the news API")
def send_request() -> dict:
    """_summary_

    Returns:
        dict: _description_
    """
    logger = get_run_logger()
    endpoint_name = "news"
    url = f"http://127.0.0.1:{API_MANAGER_DOCKER_PORT}/{endpoint_name}"
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
    # print(json.dumps(response_json,indent=4))


if __name__ == "__main__":
    # Deploy the prefect workflow
    deployment = Deployment.build_from_flow(
        flow=fetch_news,
        name="main",
        version=1,
        storage=GitHub.load(PREFECT_BLOCKNAME_GITHUB),
        schedule=CronSchedule(
            cron="0 8 * * *",  # Run the prefect flow at 08:00 every day
            timezone="Europe/Amsterdam",
        ),
    )
    deployment.apply()
