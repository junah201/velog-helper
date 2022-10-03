from datetime import datetime
from pydantic import BaseModel


class BlogBase(BaseModel):
    id: str


class BlogCreate(BlogBase):
    pass


class Blog(BlogBase):
    profile_img: str
    created_at: datetime
    updated_at: datetime
    last_uploaded_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    id: str
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    id: str
    title: str
    user: str
    user_img: str
    link: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class BookmarkBase(BaseModel):
    id: str
    user: str
    blog: str


class BookmarkCreate(BookmarkBase):
    pass


class Bookmark(BookmarkBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
