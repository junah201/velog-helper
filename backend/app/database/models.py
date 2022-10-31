from sqlalchemy import Column, String, DateTime, func, Boolean

from app.database.database import Base


class BaseMixin:
    id = Column(String(100), primary_key=True, index=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    updated_at = Column(DateTime, nullable=False,
                        default=func.utc_timestamp(), onupdate=func.utc_timestamp())


class User(Base, BaseMixin):
    __tablename__ = "users"

    email = Column(String(100), nullable=True)
    is_subscribed = Column(Boolean, nullable=False)


class Blog(Base, BaseMixin):
    __tablename__ = "blogs"

    profile_img = Column(String(200), nullable=False)
    last_uploaded_at = Column(DateTime, nullable=False,
                              default=func.utc_timestamp(), onupdate=func.utc_timestamp())


class Post(Base, BaseMixin):
    __tablename__ = "posts"

    title = Column(String(100), nullable=False)
    user = Column(String(100), nullable=False)
    user_img = Column(String(200), nullable=False)
    link = Column(String(100), nullable=False)


class Bookmark(Base, BaseMixin):
    __tablename__ = "bookmarks"

    user = Column(String(100), nullable=False)
    blog = Column(String(100), nullable=False)
