from typing import List, Optional
from enum import Enum

from pydantic import BaseModel, conint


class Predict(BaseModel):
    """Model for user text inference."""

    text: str


class AlphavantageTopics(str, Enum):
    """Possible topics in"""

    EARNINGS = "earnings"
    IPO = "ipo"
    MERGERS_AND_ACQUSITIONS = "mergers_and_acqusitions"
    FINANCIAL_MARKETS = "financial_markets"
    FINANCE = "finance"
    MANUFACTURING = "manufacturing"
    REAL_ESTATE = "real_estate"
    RETAIL_WHOLESAIL = "retail_wholesail"
    TECHNOLOGY = "technology"
    ECONOMY_MACRO = "economy_macro"
    ECONOMY_FISCAL = "economy_fiscal"
    ECONOMY_MONETARY = "economy_monetary"
    LIFE_SCIENCES = "life_sciences"


class ApiManagerRequest(BaseModel):
    """Request to api manager srevice."""

    tickers: Optional[List[str]] = None
    topics: Optional[List[AlphavantageTopics]] = None
    limit: conint(ge=1, le=50) = 10
