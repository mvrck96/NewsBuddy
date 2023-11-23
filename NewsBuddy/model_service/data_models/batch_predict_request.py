from typing import List

from pydantic import BaseModel


class BatchPredict(BaseModel):
    batch: List[str]