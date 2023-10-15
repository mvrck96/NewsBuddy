from pydantic import BaseModel
from datetime import datetime


class AuthorBase(BaseModel):
    author_name: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    article_id: int

    class Config:
        from_attributes = True


class TopicBase(BaseModel):
    topic_name: str
    relevance_score: float


class TopicCreate(TopicBase):
    pass


class Topic(TopicBase):
    id: int
    article_id: int

    class Config:
        from_attributes = True


class TickerBase(BaseModel):
    ticker_name: str
    relevance_score: float
    ticker_sentiment_score: float
    ticker_sentiment_label: str


class TickerCreate(TickerBase):
    pass


class Ticker(TickerBase):
    id: int
    article_id: int

    class Config:
        from_attributes = True


class ArticleBase(BaseModel):
    title: str
    url: str
    time_published: datetime
    summary: str
    banner_icon: str
    source: str
    category_within_source: str
    source_domain: str
    overall_sentiment_score: float
    overall_sentiment_label: str


class ArticleCreate(ArticleBase):
    pass


class Article(ArticleBase):
    id: int
    authors: list[Author] = []
    topics: list[Topic] = []
    tickers: list[Ticker] = []

    class Config:
        from_attributes = True
