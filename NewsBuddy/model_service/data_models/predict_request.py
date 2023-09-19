from pydantic import BaseModel


class Predict(BaseModel):
    text: str
