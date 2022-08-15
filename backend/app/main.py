

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger
from fastapi_utils.session import FastAPISessionMaker
from fastapi_utils.tasks import repeat_every

from sqlalchemy.orm import Session

import logging
import datetime
from copy import deepcopy
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


@app.post("/{user_id}/blog", response_model=schemas.User)
async def add_bookmark_blog(user_id: str, blog_id: str, db: Session = Depends(get_db)):
    return crud.add_bookmark_blog(db, user_id=user_id, blog_id=blog_id)


@app.delete("/{user_id}/blog")
async def delete_bookmark_blog(user_id: str, blog_id: str, db: Session = Depends(get_db)):
    return crud.delete_bookmark_blog(db, user_id=user_id, blog_id=blog_id)


@app.get("/{user_id}/archive", response_model=dict)
async def read_archive(user_id: str, db: Session = Depends(get_db)):
    return crud.get_archive_by_id(db, user_id=user_id)


@app.get("/{user_id}/is_bookmarked", response_model=dict)
async def is_bookmarked(user_id: str, blog_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    return {"is_bookmarked": blog_id in db_user.blogs["blogs"]}


@app.on_event("startup")
@repeat_every(seconds=60 * 2)  # 2 min
async def update_new_post() -> None:
    logger.info("update new post start")
    with sessionmaker.context_session() as db:
        blogs = deepcopy(crud.get_blogs(db))
    with sessionmaker.context_session() as db:
        await tasks.update_new_post(db, blogs)
    logger.info("update new post done")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
