from sqlalchemy.orm import Session

from . import models, schemas


def get_article(db: Session, article_id: int):
    return db.query(models.Article).filter(models.Article.id == article_id).first()


def get_article_by_url(db: Session, url: str):
    return db.query(models.Article).filter(models.Article.url == url).first()


def get_article_by_title(db: Session, title: str):
    return db.query(models.Article).filter(models.Article.title == title).all()


def get_articles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Article).offset(skip).limit(limit).all()


def create_article(db: Session, article: schemas.ArticleCreate):
    db_article = models.Article(
        title=article.title,
        url=article.url,
        time_published=article.time_published,
        summary=article.summary,
        banner_icon=article.banner_icon,
        source=article.source,
        category_within_source=article.category_within_source,
        source_domain=article.source_domain,
        overall_sentiment_score=article.overall_sentiment_score,
        overall_sentiment_label=article.overall_sentiment_label,
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_article_author(db: Session, author: schemas.AuthorCreate, article_id: int):
    db_author = models.Author(**author.model_dump(), article_id=article_id)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_topics(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Topic).offset(skip).limit(limit).all()


def create_article_topic(db: Session, topic: schemas.TopicCreate, article_id: int):
    db_topic = models.Topic(**topic.model_dump(), article_id=article_id)
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic


def get_tickers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ticker).offset(skip).limit(limit).all()


def create_article_ticker(db: Session, ticker: schemas.TickerCreate, article_id: int):
    db_ticker = models.Ticker(**ticker.model_dump(), article_id=article_id)
    db.add(db_ticker)
    db.commit()
    db.refresh(db_ticker)
    return db_ticker
