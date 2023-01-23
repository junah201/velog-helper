from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.session import FastAPISessionMaker
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from mangum import Mangum
import datetime
from typing import List, Dict
from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.database import models, schemas, crud
from app.database.database import SessionLocal, engine
from app.common.config import SQLALCHEMY_DATABASE_URL
from app.utils.search import google_search

models.Base.metadata.create_all(bind=engine)

sessionmaker = FastAPISessionMaker(SQLALCHEMY_DATABASE_URL)

app = FastAPI()

app.mount("/static", StaticFiles(directory="./app/static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

env = Environment(
    loader=FileSystemLoader('app/templates/'),
    autoescape=select_autoescape(['html']),
)


def get_db():
    """
    Dependency to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def index():
    return f"Notification API (UTC: {datetime.datetime.utcnow().strftime('%Y.%m.%d %H:%M:%S')})"


@app.post("/blog", response_model=schemas.Blog)
async def create_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db)):
    return crud.create_blog(db, blog)


@app.get("/blog", response_model=schemas.Blog)
async def read_blog(blog_id: str, db: Session = Depends(get_db)):
    return crud.get_blog_by_id(db, blog_id)


@app.get("/blogs", response_model=List[schemas.Blog])
async def read_blogs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    blogs = crud.get_blogs(db, skip=skip, limit=limit)
    return blogs


@app.get("/user", response_model=schemas.User)
async def read_user(user_id: str, db: Session = Depends(get_db)):
    return crud.get_user_by_id(db, user_id)


@app.post("/user", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@app.get("/users", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@app.get("/{user_id}/blogs", response_model=Dict)
async def read_blogs_by_user(user_id: str, db: Session = Depends(get_db)):
    return {"blogs": crud.get_bookmarked_blogs_by_user_id(db, user_id=user_id)}


@app.post("/{user_id}/blog", response_model=schemas.Bookmark)
async def add_bookmark_blog(user_id: str, blog_id: str, db: Session = Depends(get_db)):
    return await crud.add_bookmark_blog(db, user_id=user_id, blog_id=blog_id)


@app.delete("/{user_id}/blog")
async def delete_bookmark_blog(user_id: str, blog_id: str, db: Session = Depends(get_db)):
    return crud.delete_bookmark_blog(db, user_id=user_id, blog_id=blog_id)


@app.get("/{user_id}/archive", response_model=List[schemas.Post])
async def read_archive(user_id: str, skip: int = 0, limit: int = 15, db: Session = Depends(get_db)):
    return crud.get_archive_by_id(db, user_id=user_id, skip=skip, limit=limit)


@app.get("/{user_id}/is_bookmarked", response_model=Dict)
async def is_bookmarked(user_id: str, blog_id: str, db: Session = Depends(get_db)):
    return {"is_bookmarked": crud.is_bookmarked(db, user_id=user_id, blog_id=blog_id)}


@app.post("/{user_id}/email", response_model=Dict)
async def edit_email(user_id: str, email: str, db: Session = Depends(get_db)):
    return {"status": crud.edit_email(db, user_id=user_id, email=email)}


@app.get("/{blog_id}/followers")
async def get_followers(blog_id: str, db: Session = Depends(get_db)) -> int:
    return crud.get_followers(db, blog_id=blog_id)


@app.get("/guide", response_class=HTMLResponse)
async def get_guide():
    guide_template = env.get_template("guide.html")
    return HTMLResponse(content=guide_template.render(), status_code=200)


@app.get("/subscription/{user_id}", response_class=HTMLResponse)
async def set_subscription(user_id: str, is_subscribe: bool, db: Session = Depends(get_db)):
    crud.set_subscription(db, user_id=user_id, is_subscription=is_subscribe)

    if is_subscribe:
        subscription_template = env.get_template("subscription.html")
        return HTMLResponse(content=subscription_template.render(user_id=user_id), status_code=200)
    else:
        unsubscription_template = env.get_template("unsubscription.html")
        return HTMLResponse(content=unsubscription_template.render(user_id=user_id), status_code=200)


@app.get("/search", response_model=schemas.SearchResults)
async def search_post_using_google(query: str, page: int = 1):
    return await google_search(query, page)


lambda_handler = Mangum(app, lifespan="off")  # do not change lifespan to on
