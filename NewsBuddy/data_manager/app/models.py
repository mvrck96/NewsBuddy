from __future__ import annotations
from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from .database import Base


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(unique=True, index=True)
    url: Mapped[str] = mapped_column(unique=True, index=True)
    time_published: Mapped[datetime] = mapped_column(unique=True, index=True)
    authors: Mapped[List["Author"]] = relationship(back_populates="article")
    summary: Mapped[str] = mapped_column(unique=True, index=True)
    banner_icon: Mapped[str] = mapped_column(unique=True, index=True)
    source: Mapped[str] = mapped_column(unique=True, index=True)
    category_within_source: Mapped[str] = mapped_column(unique=True, index=True)
    source_domain: Mapped[str] = mapped_column(unique=True, index=True)
    topics: Mapped[List["Topic"]] = relationship(back_populates="article")
    overall_sentiment_score: Mapped[float] = mapped_column(unique=True, index=True)
    overall_sentiment_label: Mapped[str] = mapped_column(unique=True, index=True)
    ticker_sentiment: Mapped[List["Ticker"]] = relationship(back_populates="article")


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"))
    author_name: Mapped[str] = mapped_column(index=True)
    article: Mapped["Article"] = relationship(back_populates="articles")


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"))
    topic_name: Mapped[str] = mapped_column(index=True)
    relevance_score: Mapped[float] = mapped_column(unique=True, index=True)
    article: Mapped["Article"] = relationship(back_populates="articles")


class Ticker(Base):
    __tablename__ = "tickers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"))
    ticker_name: Mapped[str] = mapped_column(index=True)
    relevance_score: Mapped[float] = mapped_column(unique=True, index=True)
    ticker_sentiment_score: Mapped[float] = mapped_column(unique=True, index=True)
    ticker_sentiment_label: Mapped[str] = mapped_column(unique=True, index=True)
    article: Mapped["Article"] = relationship(back_populates="articles")
