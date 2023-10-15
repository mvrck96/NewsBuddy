FROM  prefecthq/prefect:2.13.5-python3.10

COPY ./.prefectignore .
COPY ./startup_server.sh .

# Make the script executable
RUN chmod +x startup_server.sh

RUN apt update && pip install --upgrade pip
# RUN pip install -r  requirements.txt
