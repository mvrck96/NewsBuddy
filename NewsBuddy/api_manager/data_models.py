from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, conint


class AlphavantageTopics(str, Enum):
    """News API topic options."""

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


class UserNewsRequest(BaseModel):
    """Request to api manager service."""

    tickers: Optional[List[str]] = None
    topics: Optional[List[AlphavantageTopics]] = None
    limit: conint(ge=1, le=50) = 10


class ApiNews(BaseModel):
    """Model for single news entity."""
    title: str
    url: str
    time_published: str
    summary: str
    overall_sentiment_score: float


class UserNewsResponse(BaseModel):
    """Whole news feed model, based on user settings."""
    feed: List[ApiNews]