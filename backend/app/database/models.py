from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func, JSON
from sqlalchemy.orm import relationship

from app.database.database import Base
import json


class BaseMixin:
    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    updated_at = Column(DateTime, nullable=False,
                        default=func.utc_timestamp(), onupdate=func.utc_timestamp())


class User(Base, BaseMixin):
    __tablename__ = "users"

    email = Column(String, nullable=True)
    blogs = Column(JSON, default=json.dumps({"blogs": []}))
    archive = Column(JSON, default=json.dumps({"archive": []}))
    profile_img = Column(String)


class Blog(Base, BaseMixin):
    __tablename__ = "blogs"

    users = Column(JSON, default=json.dumps({"users": []}))
    profile_img = Column(String)
    last_uploaded_at = Column(DateTime, nullable=False,
                              default=func.utc_timestamp(), onupdate=func.utc_timestamp())
