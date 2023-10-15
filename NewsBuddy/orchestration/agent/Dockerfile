FROM  prefecthq/prefect:2.13.5-python3.10

COPY ./requirements.txt .
COPY ./.prefectignore .
# COPY flows .
#
RUN apt update && pip install --upgrade pip
RUN pip install -r  requirements.txt
