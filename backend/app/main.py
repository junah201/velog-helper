from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger
from fastapi_utils.session import FastAPISessionMaker
from fastapi_utils.tasks import repeat_every

from sqlalchemy.orm import Session

import logging
import datetime
from typing import List, Dict
import uvicorn

from app.database import models, schemas, crud
from app.database.database import SessionLocal, engine
from app.common.config import SQLALCHEMY_DATABASE_URL
from app.tasks import tasks

logger.setLevel(logging.INFO)

models.Base.metadata.create_all(bind=engine)

sessionmaker = FastAPISessionMaker(SQLALCHEMY_DATABASE_URL)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

is_task_runing = False

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def index():
    return f"Notification API (UTC: {datetime.datetime.utcnow().strftime('%Y.%m.%d %H:%M:%S')})"


@app.post("/blog/", response_model=schemas.Blog)
async def create_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db)):
    return crud.create_blog(db, blog)


@app.get("/blog/", response_model=schemas.Blog)
async def read_blog(blog_id: str, db: Session = Depends(get_db)):
    return crud.get_blog_by_id(db, blog_id)


@app.get("/blogs/", response_model=List[schemas.Blog])
async def read_blogs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    blogs = crud.get_blogs(db, skip=skip, limit=limit)
    return blogs


@app.get("/user", response_model=schemas.User)
async def read_user(user_id: str, db: Session = Depends(get_db)):
    return crud.get_user_by_id(db, user_id)


@app.post("/user", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@app.get("/users/", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@app.get("/{user_id}/blogs", response_model=Dict)
async def read_blogs_by_user(user_id: str, db: Session = Depends(get_db)):
    return {"blogs": crud.get_bookmarked_blogs_by_user(db, user_id=user_id)}


@app.post("/{user_id}/blog", response_model=schemas.Bookmark)
async def add_bookmark_blog(user_id: str, blog_id: str, db: Session = Depends(get_db)):
    return await crud.add_bookmark_blog(db, user_id=user_id, blog_id=blog_id)


@app.delete("/{user_id}/blog")
async def delete_bookmark_blog(user_id: str, blog_id: str, db: Session = Depends(get_db)):
    return crud.delete_bookmark_blog(db, user_id=user_id, blog_id=blog_id)


@app.get("/{user_id}/archive", response_model=List[schemas.Post])
async def read_archive(user_id: str, skip: int = 0, limit: int = 15, db: Session = Depends(get_db)):
    return crud.get_archive_by_id(db, user_id=user_id, skip=skip, limit=limit)


@app.get("/{user_id}/is_bookmarked", response_model=dict)
async def is_bookmarked(user_id: str, blog_id: str, db: Session = Depends(get_db)):
    return {"is_bookmarked": crud.is_bookmarked(db, user_id=user_id, blog_id=blog_id)}


@app.get("/subscription/{user_id}")
async def set_subscription(user_id: str, is_subscribe: bool, db: Session = Depends(get_db)):
    crud.set_subscription(db, user_id=user_id, is_subscription=is_subscribe)
    if is_subscribe:
        return "You are subscribed"
    else:
        return "You are unsubscribed"


@app.on_event("startup")
@repeat_every(seconds=60 * 15)  # 15 min
async def update_new_post() -> None:
    logger.info("update new post start")
    print("update new post start")
    with sessionmaker.context_session() as db:
        await tasks.update_new_post(db)
    print("update new post done")
    logger.info("update new post done")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=False)
