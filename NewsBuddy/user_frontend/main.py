import requests
import streamlit as st
import streamlit.components.v1 as components
from pydantic import BaseModel

from tools.settings import service_settings
from data_models import AlphavantageTopics


class Predict(BaseModel):
    text: str


# Set page title and icon
st.set_page_config(
    page_title="NewsBuddy",
    page_icon=":newspaper:",
    initial_sidebar_state="expanded",
)

# Remove made with streamlit in footer
html_string = """
<script>
// To break out of iframe and access the parent window
const streamlitDoc = window.parent.document;

// Make the replacement
document.addEventListener("DOMContentLoaded", function(event){
        streamlitDoc.getElementsByTagName("footer")[0].innerHTML = "";
    });
</script>
"""
components.html(html_string)


def intro():
    """Draw intro text when no options selected."""
    st.title("Welcome to NewsBuddy !")
    st.sidebar.success("Select option above.")

    st.markdown(
        """
        Some great intro about our best app :))
    """
    )


def user_input():
    """Uses user input as model input."""
    user_news = st.text_area(
        "Text to analyze", "AAPL fired 10 thousand employees"
    )

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


def user_based_feed():
    with st.form("news_feed_settings"):
        tickers = st.multiselect(
            label="Tickets", options=["AAPL", "MSFT", "TSLA", "NVDA", "GOOGL"]
        )
        tickers = ",".join(tickers)

        topics = st.multiselect(
            label="topics", options=[i.value for i in AlphavantageTopics]
        )
        topics = ",".join(topics)

        limit = st.slider("Number of news", 0, 50, 10, 1)
        apikey = service_settings.alphavantage_token

        if st.form_submit_button("Generate feed"):
            url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={tickers}&topics={topics}y&apikey={service_settings.alphavantage_token}&limit={limit}"

            resp = requests.get(url).json()
            st.json(resp)
            titles = [n["title"] for n in resp["feed"]]
            titles = titles[:limit]
            
            session = requests.Session()
            for title in titles:
                payload = Predict(text=title).json()
                response = session.post(
                        service_settings.model_service_url, payload
                    ).json()
                st.write(title)
                st.json(response)
    


def latest_feed():
    pass


page_to_func_mapping = {
    "Intro": intro,
    "User based input": user_input,
    "News feed set by user": user_based_feed,
}

page_to_exec = st.sidebar.selectbox(
    "Select model inference option", page_to_func_mapping.keys()
)
page_to_func_mapping[page_to_exec]()
