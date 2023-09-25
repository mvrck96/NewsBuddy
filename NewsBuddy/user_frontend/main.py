import requests
import streamlit as st

from pydantic import BaseModel
from tools.settings import service_settings


class Predict(BaseModel):
    text: str


# Set page title and icon
st.set_page_config(
    page_title="NewsBuddy",
    page_icon=":newspaper:",
)

st.title("📈 Stock news sentiment analysis")

user_news = st.text_area("Text to analyze", "AAPL fired 10 thousand employees")

if st.button("Analyze"):
    session = requests.Session()
    payload = Predict(text=user_news).json()
    try:
        response = session.post(
            service_settings.model_service_url, payload
        ).json()
        st.json(response)
    except requests.exceptions.ConnectionError as e:
        st.warning("Can't connect to model service !")
