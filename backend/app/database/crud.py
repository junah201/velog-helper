from sqlalchemy.orm import Session
from app.database import models, schemas
import datetime

import requests
from bs4 import BeautifulSoup as bs

from app.errors.exceptions import AlreadyBookmarkedBlog, NotFoundBlog, NotFoundUser, NotBookmarkedBlog, AlreadyRegistedUser, NotFoundBookmark


def create_blog(db: Session, blog: schemas.BlogCreate):
    now = datetime.datetime.now()
    db_blog = models.Blog(
        id=blog.id,
        profile_img=get_profile_img_by_id(id=blog.id),
        created_at=now,
        updated_at=now,
        last_uploaded_at=datetime.date(2005, 2, 1)
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


def get_bookmarked_blogs_by_user(db: Session, user_id: int):
    db_bookmark = db.query(models.Bookmark).filter(
        models.Bookmark.user == user_id).all()
    result = []
    for bookmark in db_bookmark:
        result.append(get_blog_by_id(db, blog_id=bookmark.blog))
    return result


def create_user(db: Session, user: schemas.UserCreate):
    now = datetime.datetime.now()
    if db.query(models.User).filter(models.User.id == user.id).first() != None:
        raise AlreadyRegistedUser(user_id=user.id)
    db_user = models.User(
        id=user.id,
        email=user.email,
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

    db_bookmark = models.Bookmark(
        id=user_id + blog_id,
        user=user_id,
        blog=blog_id,
        created_at=now,
        updated_at=now,
    )
    db.add(db_bookmark)
    db.commit()
    db.refresh(db_bookmark)

    return db_bookmark


def delete_bookmark_blog(db: Session, user_id: str, blog_id: str):
    db_bookmark = db.query(models.Bookmark).filter(
        models.Bookmark.user == user_id, models.Bookmark.blog == blog_id)
    if db_bookmark.first() == None:
        raise NotFoundBookmark(user_id=user_id, blog_id=blog_id)
    db_bookmark.delete()
    db.commit()

    return db_bookmark.first()


def get_archive_by_id(db: Session, user_id: str) -> dict:
    db_bookmarked_blogs = db.query(models.Bookmark).filter(
        models.Bookmark.user == user_id)
    bookmarked_blogs = [
        bookmark.blog for bookmark in db_bookmarked_blogs.all()]
    db_posts = db.query(models.Post).filter(
        models.Post.user.in_(bookmarked_blogs)).all()
    return db_posts


def is_bookmarked(db: Session, user_id: str, blog_id: str):
    db_bookmarked_blogs = db.query(models.Bookmark).filter(
        models.Bookmark.user == user_id, models.Bookmark.blog == blog_id)

    return db_bookmarked_blogs.first() != None
