import requests

from data_models.predict_request import Predict
from fastapi import FastAPI, Response, status
from fastapi.responses import RedirectResponse
from tools.logger import service_logger as logger
from tools.settings import service_settings
from tools.state import State


state = State()

app = FastAPI()
state.set_live_status(True)


API_URL = (
    "https://api-inference.huggingface.co/models/mrm8488/"
    "distilroberta-finetuned-financial-news-sentiment-analysis"
)
HEADERS = {"Authorization": f"Bearer {service_settings.api_token}"}


state.set_ready_status(True)


# User-side endpoints
@app.post("/predict", tags=["Model"])
def base_predict(req: Predict) -> dict:
    """Performs sentiment classification.

    Args:
        req (Predict): Request from UI with user text

    Returns:
        dict: Predict-proba of three classes
    """
    payload = {"inputs": req.text}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()


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
