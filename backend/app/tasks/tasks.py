from dataclasses import asdict
from sqlalchemy.orm import Session
from app.database import models, schemas
from app.connom.consts import VELOG_RSS_URL
from app.utils.crawler import get_new_posts
import feedparser
import datetime


async def update_new_post(db: Session, blogs) -> None:
    for blog in blogs:
        if not blog.users["users"]:
            break
        posts = await get_new_posts(username=blog.id, limit=10)
        last_uploaded_at = datetime.datetime.strptime(
            posts[0]["released_at"][:19], "%Y-%m-%dT%H:%M:%S")
        for post in posts:
            post_upload_time = datetime.datetime.strptime(
                post["released_at"][:19], "%Y-%m-%dT%H:%M:%S")
            if post_upload_time <= blog.last_uploaded_at:
                continue
            now = datetime.datetime.now()
            add_data = {
                "title": post["title"],
                "link": post["url_slug"],
                "date": str(post_upload_time),
                "img": post["thumbnail"]
            }

            for user_id in blog.users["users"]:
                db_user = db.query(models.User).filter(
                    models.User.id == user_id)
                origin_data = db_user.first().archive
                origin_data["archive"].append(add_data)
                db.query(models.User).filter(
                    models.User.id == user_id).update(
                    {"archive": origin_data, "updated_at": now})

        db.query(models.Blog).filter(
            models.Blog.id == blog.id).update(
            {"last_uploaded_at": last_uploaded_at})

    db.commit()
    print("update new post")
