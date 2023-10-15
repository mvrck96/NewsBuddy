import requests
import streamlit as st
import streamlit.components.v1 as components

from tools.settings import service_settings
from tools.logger import service_logger
from data_models import AlphavantageTopics, Predict, ApiManagerRequest


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
    st.sidebar.success("Select option above :arrow_up:")

    st.markdown(
    """
        # Welocome to NewsBuddy !
        
        > **Stock news analysis made for people**

        

    """
    )


def user_input():
    """Uses user input as model input."""

    st.markdown("**FEATURE INFO PLACEHOLDER**")

    user_news = st.text_area(
        "Text to analyze", "AAPL fired 10 thousand employees"
    )
    session = requests.Session()

    if st.button("Analyze"):
        payload = Predict(text=user_news).json()
        try:
            response = session.post(
                service_settings.model_service_url, payload
            ).json()
            st.json(response)
        except requests.exceptions.ConnectionError as e:
            st.error("Can't connect to model service !")
            service_logger.debug(e)


def user_based_feed():
    """Score latest news by user settings."""

    st.markdown("**FEATURE INFO PLACEHOLDER**")

    with st.form("news_feed_settings"):
        tickers = st.multiselect(
            label="Select tickers", 
            options=["AAPL", "MSFT", "TSLA", "NVDA", "GOOGL"]
        )
        tickers = tickers if len(tickers) > 0 else None

        topics = st.multiselect(
            label="Select topics", options=[i.value for i in AlphavantageTopics]
        )
        topics = topics if len(topics) > 0 else None
        
        limit = st.slider("Number of news", 0, 50, 10, 1)

        if st.form_submit_button("Analyze latest news !"):
            api_man_payload = ApiManagerRequest(
                tickers=tickers,
                topics=topics,
                limit=limit
            ).json()
            st.json(api_man_payload)
            try:
                api_man_resp = requests.post(service_settings.api_manager_url,
                                            api_man_payload)
                st.json(api_man_payload)
                titles = [n["title"] for n in api_man_resp["feed"]]
                session = requests.Session()
                for title in titles:
                    payload = Predict(text=title).json()
                    try:
                        response = session.post(
                                service_settings.model_service_url, payload
                            ).json()
                        st.write(title)
                        st.json(response)

                    except requests.exceptions.ConnectionError as e:
                        st.error("Can't connect to model service !")
                        service_logger.debug(e)

            except requests.exceptions.ConnectionError as e:
                st.error("Can't connect to api manager service !")
                service_logger.debug(e)    


def latest_feed():
    """Generate news feed."""

    st.markdown("**FEATURE INFO PLACEHOLDER**")

    st.warning("Feature not implemented yet :((")


page_to_func_mapping = {
    "Intro": intro,
    "User based input": user_input,
    "News selected by user": user_based_feed,
    "Latest news feed": latest_feed,
}

page_to_exec = st.sidebar.selectbox(
    "Select feature you want to use:", page_to_func_mapping.keys()
)
page_to_func_mapping[page_to_exec]()
