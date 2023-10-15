from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/articles/", response_model=schemas.Article)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    db_article = crud.get_article_by_url(db, url=article.url)
    if db_article:
        raise HTTPException(status_code=400, detail="URL already written")
    return crud.create_article(db=db, article=article)


@app.get("/articles/", response_model=list[schemas.Article])
def read_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    articles = crud.get_articles(db, skip=skip, limit=limit)
    return articles


@app.get("/articles/{article_id}", response_model=schemas.Article)
def read_article(article_id: int, db: Session = Depends(get_db)):
    db_article = crud.get_article(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article


@app.post("/articles/{article_id}/authors/", response_model=schemas.Author)
def create_author_for_article(
    article_id: int, author: schemas.AuthorCreate, db: Session = Depends(get_db)
):
    return crud.create_article_author(db=db, author=author, article_id=article_id)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


app.post("/articles/{article_id}/topics/", response_model=schemas.Topic)
def create_topic_for_article(
    article_id: int, topic: schemas.TopicCreate, db: Session = Depends(get_db)
):
    return crud.create_article_topic(db=db, topic=topic, article_id=article_id)


@app.get("/topics/", response_model=list[schemas.Topic])
def read_topics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    topics = crud.get_topics(db, skip=skip, limit=limit)
    return topics


app.post("/articles/{article_id}/tickers/", response_model=schemas.Ticker)
def create_ticker_for_article(
    article_id: int, ticker: schemas.TickerCreate, db: Session = Depends(get_db)
):
    return crud.create_article_ticker(db=db, ticker=ticker, article_id=article_id)


@app.get("/tickers/", response_model=list[schemas.Ticker])
def read_tickers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tickers = crud.get_tickers(db, skip=skip, limit=limit)
    return tickers
