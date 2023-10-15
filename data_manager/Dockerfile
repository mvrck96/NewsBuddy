FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
EXPOSE 80
ENV POSTGRES_HOST="postgres_db:5432"
ENV POSTGRES_USER="postgres"
ENV POSTGRES_PASSWORD_FILE="./db_password.txt"
CMD ["uvicorn", "app.main:app", "--port", "80", "--reload"]
