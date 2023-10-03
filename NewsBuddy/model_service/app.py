import requests

from data_models.predict_request import Predict
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.responses import RedirectResponse
from tools.logger import service_logger as logger
from tools.settings import service_settings
from tools.state import State
from tools.utils import check_hugging_face_connection


API_URL = (
    "https://api-inference.huggingface.co/models/mrm8488/"
    "distilroberta-finetuned-financial-news-sentiment-analysis"
)
HEADERS = {"Authorization": f"Bearer {service_settings.api_token}"}


state = State()

app = FastAPI(root_path=service_settings.root_path)
state.set_live_status(True)

api_accessible = check_hugging_face_connection(API_URL)
# Readiness init should be rewritten in order to exit dead state
state.set_ready_status(True) if api_accessible else state.set_ready_status(
    False
)


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
    logger.info(f"Incoming request: {payload}")
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if (
        not isinstance(response.json(), list)
        and "error" in response.json().keys()
    ):
        logger.warning("Model not ready !")
        raise HTTPException(status_code=503, detail=response.json()["error"])
    elif isinstance(response.json(), list):
        logger.info(f"Response: {response.json()}")
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


@app.get(f"/", tags=["redirect"])
def redirect_docs():
    """Redirect on SwaggerUI."""
    logger.info("Request to docs.")
    return RedirectResponse(url=f"{app.root_path}/docs")


@app.on_event("shutdown")
def on_shutdown():
    """State management on shutdown."""
    state.set_ready_status(False)
    state.set_live_status(False)
    logger.info("Service shuted down !")
