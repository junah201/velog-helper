from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


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
    is_subscribed: bool
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
    short_description: Optional[str]


class PostCreate(PostBase):
    pass


class Post(PostBase):
    created_at: datetime
    updated_at: datetime
    body_hash: Optional[str]

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


class SearchResult(BaseModel):
    title: str
    html_title: str
    link: str
    snippet: str
    html_snippet: str
    thumbnail_link: str


class SearchResults(BaseModel):
    total: int
    results: List[SearchResult] = []
