import requests

from requests import ConnectionError
from tools.logger import service_logger as logger


def check_hugging_face_connection(url: str) -> bool:
    """Checks if HuggingFace API is accessible

    Args:
        url (str): HuggingFace model url

    Returns:
        bool: Success flag
    """
    try:
        response = requests.get(url)
        logger.debug(f"HuggingFace response code: {response.status_code}")
        logger.success(f"Connection to HuggingFace is ok !")
        return True
    except ConnectionError:
        return False
