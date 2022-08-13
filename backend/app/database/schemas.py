from typing import List, Union, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class BlogBase(BaseModel):
    id: str


class BlogCreate(BlogBase):
    pass


class Blog(BlogBase):
    users: Dict
    profile_img: str
    created_at: datetime
    updated_at: datetime
    last_uploaded_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    id: int
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    blogs: Dict
    archive: Dict
    profile_img: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
