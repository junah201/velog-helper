from sqlalchemy import Column, String, DateTime, func, JSON

from app.database.database import Base


class BaseMixin:
    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    updated_at = Column(DateTime, nullable=False,
                        default=func.utc_timestamp(), onupdate=func.utc_timestamp())


class User(Base, BaseMixin):
    __tablename__ = "users"

    email = Column(String, nullable=True)


class Blog(Base, BaseMixin):
    __tablename__ = "blogs"

    profile_img = Column(String)
    last_uploaded_at = Column(DateTime, nullable=False,
                              default=func.utc_timestamp(), onupdate=func.utc_timestamp())


class Post(Base, BaseMixin):
    __tablename__ = "posts"

    title = Column(String, nullable=False)
    user = Column(String, nullable=False)
    user_img = Column(String, nullable=False)
    link = Column(String, nullable=False)


class Bookmark(Base, BaseMixin):
    __tablename__ = "bookmarks"

    user = Column(String, nullable=False)
    blog = Column(String, nullable=False)
