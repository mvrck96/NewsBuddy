import json
from datetime import datetime

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
    layout="wide",
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
        # Welocome to NewsBuddy :runner:
        
        ### Stock news analysis made :green[simple] !

        ---

        With this app you can try next features:
        - Insert your text and get sentiment score
        - Make custom news selection and fetch sentiment scores for them
        - Surf news feed !

        To access any of these feature, select it in sidebar on the left :arrow_left:
    """
    )


# @st.cache_data
def predict_user_input(user_news: str):
    """Sent user text to model."""

    session = requests.Session()
    payload = Predict(text=user_news).json()
    try:
        response = session.post(
            service_settings.model_service_url + "/predict", payload
        ).json()
    except requests.exceptions.ConnectionError as e:
        st.error("Can't connect to model service !")
        service_logger.debug(e)
    return response


def user_input():
    """Uses user input as model input."""

    st.markdown("**FEATURE INFO PLACEHOLDER**")

    with st.form("main-form"):
        user_news = st.text_area(
            "Text to analyze", "AAPL fired 10 thousand employees"
        )
        if st.form_submit_button("Analyze"):
            res = predict_user_input(user_news)

            if isinstance(res, list):
                res = sorted(res[0], key=lambda x: x["score"], reverse=True)

                c1, c2 = st.columns((1, 4))
                c1.markdown("#### Sentiment score ⟶")
                c2.metric(
                    label=res[0]["label"],
                    value=round(res[0]["score"], 4),
                    delta=round(res[0]["score"] - res[1]["score"], 4),
                )
            else:
                st.warning("Model not ready, wait a little.")
                service_logger.info(res)


def user_based_feed():
    """Score latest news by user settings."""

    st.markdown("**FEATURE INFO PLACEHOLDER**")

    with st.form("news_feed_settings"):
        tickers = st.multiselect(
            label="Select tickers:",
            options=["AAPL", "MSFT", "TSLA", "NVDA", "GOOGL"],
        )
        tickers = tickers if len(tickers) > 0 else None

        topics = st.multiselect(
            label="Select news topics:",
            options=[i.value for i in AlphavantageTopics],
        )
        topics = topics if len(topics) > 0 else None

        limit = st.slider("Number of news", 0, 50, 10, 1)

        if st.form_submit_button("Analyze latest news !"):
            api_man_payload = ApiManagerRequest(
                tickers=tickers, topics=topics, limit=limit
            ).json()
            try:
                # api_man_resp = requests.post(
                #     service_settings.api_manager_url + "/user-news",
                #     api_man_payload,
                # ).json()

                with open("test.json", "r") as jf:
                    api_man_resp = json.load(jf)

                session = requests.Session()
                for n in api_man_resp["feed"]:
                    payload = Predict(text=n["title"]).json()
                    try:
                        response = session.post(
                            service_settings.model_service_url + "/predict",
                            payload,
                        ).json()
                        c1, c2, c3 = st.columns((1, 1, 1), gap="medium")

                        title = n["title"].replace(":", "\:")
                        url = n["url"]
                        c1.markdown(f"#### [{title}]({url})")
                        response = sorted(
                            response[0], key=lambda x: x["score"], reverse=True
                        )
 
                        with c2:
                            tp = datetime.strptime(n['time_published'],
                                 "%Y%m%dT%H%M%S").strftime("%-d %b %y @ %H:%M")

                            st.markdown(
                                f"""
                                **Time published:** {tp}

                                **Source:** 

                                **Author:** 
                                """
                                )
                            
                            with st.expander("Summary"):
                                st.write(n['summary'])
                        
                        with c3:
                            ic1, ic2 = st.columns((1, 1))
                            ic1.markdown("#### Sentiment score: ")
                            ic2.metric(
                                label=response[0]["label"],
                                value=round(response[0]["score"], 3),
                                delta=round(
                                    response[0]["score"] - response[1]["score"], 4
                                ),
                            )
 
                        st.divider()

                    except requests.exceptions.ConnectionError as e:
                        st.error("Can't connect to model_service !")
                        service_logger.debug(e)

            except requests.exceptions.ConnectionError as e:
                st.error("Can't connect to api_manager service !")
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
