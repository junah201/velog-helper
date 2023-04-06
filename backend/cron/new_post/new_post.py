from sqlalchemy.orm import Session
import models
import database
from crawler import get_new_posts
from typing import List, Tuple
import discord_logging
import datetime
import mail

VELOG_DEFAULT_PROFILE_IMG = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAASbSURBVHgB7Z0tTytBFIYP914BDiQ4cIADB0EhwYFE8ifq7g/hJ2CRSCQ4kOCobF3ruHk3maS5aSnbdnfPOe/7JE0oCTvTnmc+dvbMsNbr9b5M0PLLBDUSgBwJQI4EIEcCkCMByJEA5EgAciQAORKAHAlAjgQgRwKQIwHIkQDkSAByJAA5EoAcCUCOBCBHApAjAciRAORIAHIkADkSgBwJQI4EIEcCkCMByJEA5EgAciQAOX+MhPX1dTs+Prbt7W3b3d21jY2N6ndgPB7bYDCw4XBor6+v9vHxUb1nIL0Ae3t7dn5+XgV9FhABYuC1v79f/Q4SPD8/28vLi2UmrQA/Cfx34O/wwjXu7u7S9gi/z87O/loyELTr62vb2tqyZcFQcXp6Wv2MXiEb6SaBCDwEWDVFqmykEgABOjo6sqbAtbNJkEaAi4uLRoNfQBmXl5eWhRQCIChlnG6Dk5OTVstrkvACYKLXxJg/D5RZ1hEiE14ABGIVs/26IPgZeoHQAiDwbYz7s4AA0XuB0AIsusizKsrycmRCC+Dhyz84OLDIhBUAra/rHgCgDpGHgbAC7OzsmBc81aUuYQXY3Nw0L3iqS13CCtDFrd8sPNWlLsoIIkcCkBNWAE8JGpGTRcIKgPw9L3iqS13CCvD5+Wle8FSXuoQVAJm8HlK0UAfUJSqhJ4Fvb2/WNcgcjkxoAfDld936oieKhhYAwX96erKuwJ6B6Oni4dcBIEAXvQAC//j4aNEJLwCC30UgUGaGzSIpVgLRC7Q5FKCsLFvG0iwFPzw8tBIUlIGyspDqWcD9/X2jEuDaKCMT6R4GIUBNzAlwzWzBByl3ByNYaK23t7dLP6vHfT6u9/7+bhlZ6/V6X5YYpI0jebRu/mD2wBfSHxCBngAv9ASQ4PDwsErhwvvJE0JGo1EV9H6/72KFsS1SCDAZyFngnh2vVUwSUV4WQUILULZnlR06aMGYqDW1QDN56khZho6+Ghh2DoBgXF1dTZ3koZWvcqWubECdtg0NZUQ+QiakAGjxOA9gHhABj4wXeWyMHgX5/j85Zwi9AXoeD4+n6xJOAASk7nbwkjyCGT0meXg/mcWDYOMsIJwShtaO3mWRHT/odaINCaHmAIsEHyCQOP6tHAHXFKVukSQIsxK4aPDbBnWMdG5ACAHwhUYIfgHzEwwjEXAvQFdHwCzLzc1NiC1jrgXA2I31/Ijbr1HnCEfKuRagq/N/VgXuJLzPB9wKgMBnOITJu8RuBUDXnwHvQ4FLAbDkGrnr/x8MBV7vClwKEHHWPw+vn8mdANlaf8FrL+BOgIytv+Dxs7kSAC0kY+sveOwFXAnQ5bGvbdH0A6m6uBLAw8GPTePtaFk3AmTv/gtYF/A0DLgRgKH1Fzx9VjcCIBuHBU89nRsBkKrFgqfNJm5SwpBGVc7fz/CvWKZRUsk9bS1PvzVMfI+OiiVHApAjAciRAORIAHIkADkSgBwJQI4EIEcCkCMByJEA5EgAciQAORKAHAlAjgQgRwKQIwHIkQDkSAByJAA5EoAcCUCOBCBHApAjAciRAORIAHIkADkSgBwJQI4EIOcfGjV2tEfztqEAAAAASUVORK5CYII="
TZ_KST = datetime.timezone(datetime.timedelta(hours=9))


def UTC_to_KST(utc_time: datetime.datetime) -> datetime.datetime:
    kst_time = utc_time + datetime.timedelta(hours=9)
    # kst_time = kst_time.replace(tzinfo=TZ_KST)
    return kst_time


async def update_new_post_by_blog(db: Session, blog: models.Blog, limit: int = 10, is_init: bool = False) -> List[str]:
    updated_posts: List[str] = list()

    posts = await get_new_posts(username=blog.id, limit=limit, return_type="List")

    if is_init:
        blog.last_uploaded_at = datetime.datetime(2005, 2, 1)

    for post in reversed(posts):
        post_uploaded_at = UTC_to_KST(datetime.datetime.strptime(
            post["released_at"][:19], "%Y-%m-%dT%H:%M:%S"))

        print(post_uploaded_at, blog.last_uploaded_at)
        if post_uploaded_at <= blog.last_uploaded_at:
            continue

        if db.query(models.Post).filter(models.Post.id == post["id"]).first():
            continue

        updated_posts.append(f"{blog.id} - {post['title']}")

        # DB에 추가
        db_post = models.Post(
            id=post["id"],
            title=post["title"],
            blog_id=post["user"]["username"],
            blog_img=post["user"]["profile"]["thumbnail"] if post["user"]["profile"]["thumbnail"] else VELOG_DEFAULT_PROFILE_IMG,
            link=post["url_slug"],
            short_description=post["short_description"],
            created_at=post_uploaded_at,
            updated_at=UTC_to_KST(datetime.datetime.strptime(
                post["updated_at"][:19], "%Y-%m-%dT%H:%M:%S")),
        )

        db.add(db_post)
        db.commit()
        db.refresh(db_post)

        db_users = db.query(models.Bookmark).filter(
            models.Bookmark.blog_id == db_post.blog_id).all()

        for bookmarked_user in db_users:
            db_user = db.query(models.User).filter(
                models.User.id == bookmarked_user.user_id).first()
            if not db_user.email:
                continue

            if db_user.is_subscribed and not is_init:
                mail.send_new_post_notice_email(
                    receiver_address=db_user.email, post=db_post, user_id=db_user.id)

    last_uploaded_at = datetime.datetime.now()
    if posts:
        last_uploaded_at = UTC_to_KST(datetime.datetime.strptime(
            posts[0]["released_at"][:19], "%Y-%m-%dT%H:%M:%S"))

    db.query(models.Blog).filter(
        models.Blog.id == blog.id).update(
            {"last_uploaded_at": last_uploaded_at,
             "updated_at": str(datetime.datetime.now())})
    db.commit()

    return updated_posts


async def update_new_post() -> None:
    db = next(database.get_db())

    total_updated_blog_cnt: int = 0
    total_updated_posts: List[str] = list()

    db_blogs = db.query(models.Blog).all()
    for blog in db_blogs:
        updated_posts = await update_new_post_by_blog(db=db, blog=blog, limit=10)
        if updated_posts:
            total_updated_blog_cnt += 1
            total_updated_posts.extend(updated_posts)

    await discord_logging.logging_new_post_upload(total_updated_blog_cnt, total_updated_posts)
