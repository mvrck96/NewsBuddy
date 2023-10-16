from typing import List

import requests
from fastapi import FastAPI, Query, Response, status
from fastapi.responses import RedirectResponse
from tools.logger import service_logger as logger
from tools.settings import service_settings
from tools.state import State
from data_models import AlphavantageTopics
from tools.utils import is_valid_date
from data_models import UserNewsRequest, UserNewsResponse, ApiNews

state = State()

app = FastAPI()
state.set_live_status(True)
state.set_ready_status(True)


# User-side endpoints
@app.get("/news", tags=["News"])
def get_news(
    topics: List[AlphavantageTopics] = Query(None, description="Select one or more news topics"),
    tickers: List[str] = Query(None, description="Select one or more tickers"),
    time_from: str = None,
    time_to: str = None,
    sort: str = "LATEST",
    limit: int = 50,
) -> dict:
    """
        Get news articles based on specified parameters. \n
    \n
        Args: \n
            topics (List[ALPHAVANTAGE_TOPICS], optional): The news topics. Comma-separated if multiple. \n
            tickers (List[str], optional): The stock/crypto/forex symbols. Comma-separated if multiple. \n
            time_from (str, optional): The starting date and time (YYYYMMDDTHHMM format). \n
            time_to (str, optional): The ending date and time (YYYYMMDDTHHMM format). \n
            sort (str, optional): Sorting order ("LATEST", "EARLIEST", or "RELEVANCE"). \n
            limit (int, optional): The maximum number of results to return. \n
    \n
        Returns: \n
            dict: The response from the external API. \n
    """
    if time_from and not is_valid_date(time_from):
        return {"error": "Invalid 'time_from' format. Use YYYYMMDDTHHMM."}
    if time_to and not is_valid_date(time_to):
        return {"error": "Invalid 'time_to' format. Use YYYYMMDDTHHMM."}

    # Build the query parameters for the external API request
    params = {
        "function": "NEWS_SENTIMENT",
        "apikey": service_settings.alphavantage_token,
    }

    if tickers:
        params["tickers"] = tickers

    if topics:
        params["topics"] = topics

    if time_from:
        params["time_from"] = time_from

    if time_to:
        params["time_to"] = time_to

    if sort:
        params["sort"] = sort

    if limit:
        params["limit"] = limit

    try:
        response = requests.get(service_settings.alphavantage_url, params=params)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as exc:
        return {"error": f"Failed to fetch data from the external API: {str(exc)}"}


@app.post("/user-news", tags=["News"])
def get_user_news(req: UserNewsRequest) -> UserNewsResponse:
    """Get news feed according to user settings."""

    res = get_news(topics=req.topics, tickers=req.tickers)
    feed = res["feed"][:req.limit - 1]
    valid_feed = [ApiNews.model_validate(n) for n in feed]
    return UserNewsResponse(feed=valid_feed)


# Service-side endpoints
@app.get("/health/liveness", tags=["observability"])
def liveness(response: Response):
    """Liveness probe endpoint."""
    _status = state.get_live_status()
    if _status:
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return {"liveness": _status}


@app.get("/health/readiness", tags=["observability"])
def readiness(response: Response):
    """Readiness probe endpoint."""
    _status = state.get_ready_status()
    if _status:
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return {"readiness": _status}


@app.get("/", tags=["redirect"])
def redirect_docs():
    """Redirect on SwaggerUI."""
    logger.info("Request to docs.")
    return RedirectResponse(url="/docs")


@app.on_event("shutdown")
def on_shutdown():
    """State management on shutdown."""
    state.set_ready_status(False)
    state.set_live_status(False)
    logger.info("Service shuted down !")
