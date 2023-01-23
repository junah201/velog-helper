from sqlalchemy.orm import Session
from app.database import models, schemas
from app.utils import crawler
from app.tasks.new_post import update_new_post_by_blog
import datetime
from typing import List

from app.errors.exceptions import AlreadyBookmarkedBlog, NotFoundBlog, NotFoundUser, NotBookmarkedBlog, AlreadyRegistedUser, NotFoundBookmark


async def create_blog(db: Session, blog: schemas.BlogCreate) -> models.Blog:
    # 블로그 생성
    now = datetime.datetime.now()
    db_blog = models.Blog(
        id=blog.id,
        profile_img=await crawler.get_user_profile(username=blog.id),
        created_at=now,
        updated_at=now,
        last_uploaded_at=now
    )
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)

    # 새 글 목록 추가
    await update_new_post_by_blog(db, db_blog, limit=25, is_init=True)

    return db_blog


def get_blogs(db: Session, skip: int = 0, limit: int = 100) -> List[models.Blog]:
    return db.query(models.Blog).offset(skip).limit(limit).all()


def get_blog_by_id(db: Session, blog_id: str, error: bool = True) -> models.Blog:
    db_blog = db.query(models.Blog).filter(
        models.Blog.id == blog_id).first()
    if (db_blog == None and error):
        raise NotFoundBlog(blog_id=blog_id)
    return db_blog


def get_bookmarked_blogs_by_user_id(db: Session, user_id: int) -> List[models.Blog]:
    db_user: models.User = db.query(models.User).filter(
        models.User.id == user_id).first()
    bookmarked_blogs = []
    for bookmark in db_user.bookmarks:
        bookmarked_blogs.append(bookmark.blog)
    return bookmarked_blogs


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    now = datetime.datetime.now()
    if db.query(models.User).filter(models.User.id == user.id).first() != None:
        raise AlreadyRegistedUser(user_id=user.id)
    db_user = models.User(
        id=user.id,
        email=user.email,
        is_subscribed=True,
        created_at=now,
        updated_at=now,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: str) -> models.User:
    db_user = db.query(models.User).filter(
        models.User.id == user_id).first()
    if (db_user == None):
        raise NotFoundUser(user_id=user_id)
    return db_user


async def add_bookmark_blog(db: Session, user_id: str, blog_id: str) -> models.Bookmark:
    now = datetime.datetime.now()

    db_blog = db.query(models.Blog).filter(
        models.Blog.id == blog_id).first()
    if db_blog == None:
        await create_blog(db, schemas.BlogBase(id=blog_id))

    db_bookmark = models.Bookmark(
        user_id=user_id,
        blog_id=blog_id,
        created_at=now,
        updated_at=now,
    )
    db.add(db_bookmark)
    db.commit()
    db.refresh(db_bookmark)

    return db_bookmark


def delete_bookmark_blog(db: Session, user_id: str, blog_id: str) -> models.Bookmark:
    db_bookmark = db.query(models.Bookmark).filter(
        models.Bookmark.user_id == user_id, models.Bookmark.blog_id == blog_id)
    if db_bookmark.first() == None:
        raise NotFoundBookmark(user_id=user_id, blog_id=blog_id)
    db_bookmark.delete()
    db.commit()

    return db_bookmark.first()


def get_archive_by_id(db: Session, user_id: str, skip: int = 0, limit: int = 15) -> List[models.Post]:
    db_bookmarks = db.query(models.Bookmark).filter(
        models.Bookmark.user_id == user_id).all()

    bookmarked_blogs = [
        bookmark.blog.id for bookmark in db_bookmarks]

    if not bookmarked_blogs:
        return []

    db_posts = db.query(models.Post).filter(
        models.Post.blog_id.in_(bookmarked_blogs)).order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all()
    return db_posts


def is_bookmarked(db: Session, user_id: str, blog_id: str):
    db_bookmarked_blogs = db.query(models.Bookmark).filter(
        models.Bookmark.user_id == user_id, models.Bookmark.blog_id == blog_id)

    return db_bookmarked_blogs.first() != None


def set_subscription(db: Session, user_id: str, is_subscription: bool) -> None:
    db.query(models.User).filter(
        models.User.id == user_id).update(
            {"is_subscribed": is_subscription, "updated_at": str(datetime.datetime.now())})
    db.commit()


def edit_email(db: Session, user_id: str, email: str) -> bool:
    get_user_by_id(db=db, user_id=user_id)
    db.query(models.User).filter(
        models.User.id == user_id).update({"email": email})
    db.commit()
