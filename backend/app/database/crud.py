from sqlalchemy.orm import Session
from app.database import models, schemas
import datetime

import requests
from bs4 import BeautifulSoup as bs

from app.errors.exceptions import AlreadyBookmarkedBlog, NotFoundBlog, NotFoundUser, NotBookmarkedBlog, AlreadyRegistedUser


def create_blog(db: Session, blog: schemas.BlogCreate):
    now = datetime.datetime.now()
    db_blog = models.Blog(
        id=blog.id,
        users={"users": []},
        profile_img=get_profile_img_by_id(id=blog.id),
        created_at=now,
        updated_at=now,
        last_uploaded_at=now
    )
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog


def get_blogs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Blog).offset(skip).limit(limit).all()


def get_blog_by_id(db: Session, blog_id: str, error: bool = True):
    db_blog = db.query(models.Blog).filter(
        models.Blog.id == blog_id).first()
    if(db_blog == None and error):
        raise NotFoundBlog(blog_id=blog_id)
    return db_blog


def create_user(db: Session, user: schemas.UserCreate):
    now = datetime.datetime.now()
    if db.query(models.User).filter(models.User.id == user.id).first() != None:
        raise AlreadyRegistedUser(user_id=user.id)
    db_user = models.User(
        id=user.id,
        email=user.email,
        blogs={"blogs": []},
        archive={"archive": []},
        profile_img="tmp",
        created_at=now,
        updated_at=now,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: str):
    db_user = db.query(models.User).filter(
        models.User.id == user_id).first()
    if(db_user == None):
        raise NotFoundUser(user_id=user_id)
    return db_user


def get_profile_img_by_id(id: str) -> str:
    response = requests.get(f"https://velog.io/@{id}")
    soup = bs(response.text, "html.parser")
    element = soup.select_one('div > a > img')

    if element == None:
        raise NotFoundBlog(blog_id=id)

    return element["src"]


def add_bookmark_blog(db: Session, user_id: str, blog_id: str):
    now = datetime.datetime.now()

    instance = db.query(models.Blog).filter(models.Blog.id == blog_id)
    # 이미 등록된 블로그가 없으면 새로 등록
    if instance.first() == None:
        create_blog(db, schemas.BlogCreate(id=blog_id))
    data = instance.first().users
    if user_id in data["users"]:
        raise AlreadyBookmarkedBlog(user_id=user_id, blog_id=blog_id)
    data["users"].append(user_id)
    instance.update({"users": data, "updated_at": now})

    instance = db.query(models.User).filter(models.User.id == user_id)
    data = instance.first().blogs
    if blog_id in data["blogs"]:
        raise AlreadyBookmarkedBlog(user_id=user_id, blog_id=blog_id)
    data["blogs"].append(blog_id)
    instance.update({"blogs": data, "updated_at": now})

    db.commit()

    return instance.first()


def delete_bookmark_blog(db: Session, user_id: str, blog_id: str):
    now = datetime.datetime.now()

    instance = db.query(models.Blog).filter(models.Blog.id == blog_id)
    data = instance.first().users
    if user_id not in data["users"]:
        raise NotBookmarkedBlog(user_id=user_id, blog_id=blog_id)
    data["users"].remove(user_id)
    instance.update({"users": data, "updated_at": now})

    instance = db.query(models.User).filter(models.User.id == user_id)
    data = instance.first().blogs
    if blog_id not in data["blogs"]:
        raise NotBookmarkedBlog(user_id=user_id, blog_id=blog_id)
    data["blogs"].remove(blog_id)
    instance.update({"blogs": data, "updated_at": now})

    db.commit()

    return instance.first()


def get_archive_by_id(db: Session, user_id: str) -> dict:
    db_user = get_user_by_id(db, user_id=user_id)
    return db_user.archive
