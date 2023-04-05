from sqlalchemy import Column, String, DateTime, func, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
VELOG_DEFAULT_PROFILE_IMG = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAASbSURBVHgB7Z0tTytBFIYP914BDiQ4cIADB0EhwYFE8ifq7g/hJ2CRSCQ4kOCobF3ruHk3maS5aSnbdnfPOe/7JE0oCTvTnmc+dvbMsNbr9b5M0PLLBDUSgBwJQI4EIEcCkCMByJEA5EgAciQAORKAHAlAjgQgRwKQIwHIkQDkSAByJAA5EoAcCUCOBCBHApAjAciRAORIAHIkADkSgBwJQI4EIEcCkCMByJEA5EgAciQAOX+MhPX1dTs+Prbt7W3b3d21jY2N6ndgPB7bYDCw4XBor6+v9vHxUb1nIL0Ae3t7dn5+XgV9FhABYuC1v79f/Q4SPD8/28vLi2UmrQA/Cfx34O/wwjXu7u7S9gi/z87O/loyELTr62vb2tqyZcFQcXp6Wv2MXiEb6SaBCDwEWDVFqmykEgABOjo6sqbAtbNJkEaAi4uLRoNfQBmXl5eWhRQCIChlnG6Dk5OTVstrkvACYKLXxJg/D5RZ1hEiE14ABGIVs/26IPgZeoHQAiDwbYz7s4AA0XuB0AIsusizKsrycmRCC+Dhyz84OLDIhBUAra/rHgCgDpGHgbAC7OzsmBc81aUuYQXY3Nw0L3iqS13CCtDFrd8sPNWlLsoIIkcCkBNWAE8JGpGTRcIKgPw9L3iqS13CCvD5+Wle8FSXuoQVAJm8HlK0UAfUJSqhJ4Fvb2/WNcgcjkxoAfDld936oieKhhYAwX96erKuwJ6B6Oni4dcBIEAXvQAC//j4aNEJLwCC30UgUGaGzSIpVgLRC7Q5FKCsLFvG0iwFPzw8tBIUlIGyspDqWcD9/X2jEuDaKCMT6R4GIUBNzAlwzWzBByl3ByNYaK23t7dLP6vHfT6u9/7+bhlZ6/V6X5YYpI0jebRu/mD2wBfSHxCBngAv9ASQ4PDwsErhwvvJE0JGo1EV9H6/72KFsS1SCDAZyFngnh2vVUwSUV4WQUILULZnlR06aMGYqDW1QDN56khZho6+Ghh2DoBgXF1dTZ3koZWvcqWubECdtg0NZUQ+QiakAGjxOA9gHhABj4wXeWyMHgX5/j85Zwi9AXoeD4+n6xJOAASk7nbwkjyCGT0meXg/mcWDYOMsIJwShtaO3mWRHT/odaINCaHmAIsEHyCQOP6tHAHXFKVukSQIsxK4aPDbBnWMdG5ACAHwhUYIfgHzEwwjEXAvQFdHwCzLzc1NiC1jrgXA2I31/Ijbr1HnCEfKuRagq/N/VgXuJLzPB9wKgMBnOITJu8RuBUDXnwHvQ4FLAbDkGrnr/x8MBV7vClwKEHHWPw+vn8mdANlaf8FrL+BOgIytv+Dxs7kSAC0kY+sveOwFXAnQ5bGvbdH0A6m6uBLAw8GPTePtaFk3AmTv/gtYF/A0DLgRgKH1Fzx9VjcCIBuHBU89nRsBkKrFgqfNJm5SwpBGVc7fz/CvWKZRUsk9bS1PvzVMfI+OiiVHApAjAciRAORIAHIkADkSgBwJQI4EIEcCkCMByJEA5EgAciQAORKAHAlAjgQgRwKQIwHIkQDkSAByJAA5EoAcCUCOBCBHApAjAciRAORIAHIkADkSgBwJQI4EIOcfGjV2tEfztqEAAAAASUVORK5CYII="


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Column(
        String(100),
        primary_key=True,
        unique=True,
        nullable=False,
        comment="유저 고유 번호",
    )
    email = Column(
        String(100),
        nullable=True,
        comment="이메일",
    )
    bookmarks = relationship("Bookmark", back_populates="user")
    is_subscribed = Column(
        Boolean,
        nullable=False,
        default=True,
        comment="이메일 구독 여부",
    )
    created_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        comment="생성 시점",
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
        comment="마지막 수정 시점"
    )

    class Config:
        orm_mode = True


class Blog(Base):
    __tablename__ = "blogs"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Column(
        String(100),
        primary_key=True,
        unique=True,
        nullable=False,
        comment="블로그 고유 번호",
    )
    profile_img = Column(
        String(200),
        nullable=False,
        default=VELOG_DEFAULT_PROFILE_IMG,
        comment="프로필 이미지 링크",
    )
    bookmarks = relationship("Bookmark", back_populates="blog")
    posts = relationship("Post", back_populates="blog")
    last_uploaded_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
        comment="마지막 포스트 업로드 시점"
    )
    created_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        comment="생성 시점",
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
        comment="마지막 수정 시점"
    )


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Column(
        String(100),
        primary_key=True,
        unique=True,
        nullable=False,
        comment="포스트 고유 번호",
    )
    title = Column(
        String(100),
        nullable=False,
        comment="포스트 제목",
    )
    blog_id = Column(
        String(100),
        ForeignKey("blogs.id")
    )
    blog = relationship("Blog", back_populates="posts")
    blog_img = Column(
        String(200),
        nullable=False
    )
    link = Column(
        String(100),
        nullable=False
    )
    short_description = Column(
        String(200),
        nullable=True,
        default=None
    )
    body_hash = Column(
        String(100),
        nullable=True,
        default=None
    )
    created_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        comment="생성 시점",
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
        comment="마지막 수정 시점"
    )


class Bookmark(Base):
    __tablename__ = "bookmarks"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Column(
        Integer,
        primary_key=True,
        unique=True,
        nullable=False,
        comment="북마크 고유 번호",
    )
    user_id = Column(String(100), ForeignKey("users.id"))
    user = relationship("User", back_populates="bookmarks")
    blog_id = Column(String(100), ForeignKey("blogs.id"))
    blog = relationship("Blog", back_populates="bookmarks")
    created_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        comment="생성 시점",
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
        comment="마지막 수정 시점"
    )
