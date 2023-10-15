from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = "postgresql://{user}:{password}\\@{hostname}/{database_name}"
with open(os.environ["POSTGRES_PASSWORD_FILE"], "r") as f:
    password = f.readline()
SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.format(
    user=os.environ["DB_USER"],
    password=password,
    hostname=os.environ["DB_HOST"],
    database_name=os.environ["DB_NAME"],
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
