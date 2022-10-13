import datetime
from sqlalchemy.orm import Session
from app.database import models
from app.utils.crawler import get_new_posts
from app.common.consts import VELOG_DEFAULT_PROFILE_IMG


async def update_new_post(db: Session) -> None:
    db_blogs = db.query(models.Blog).all()
    for blog in db_blogs:
        posts = await get_new_posts(username=blog.id, limit=10)
        last_uploaded_at = datetime.datetime.strptime(
            posts[0]["released_at"][:19], "%Y-%m-%dT%H:%M:%S")
        for post in reversed(posts):
            post_upload_time = datetime.datetime.strptime(
                post["released_at"][:19], "%Y-%m-%dT%H:%M:%S")
            if post_upload_time <= blog.last_uploaded_at:
                continue

            print(post)

            db_post = models.Post(
                id=post["id"],
                title=post["title"],
                user=post["user"]["username"],
                user_img=post["user"]["profile"]["thumbnail"] if post["user"]["profile"]["thumbnail"] else VELOG_DEFAULT_PROFILE_IMG,
                link=post["url_slug"],
                created_at=post_upload_time,
                updated_at=datetime.datetime.strptime(
                    post["updated_at"][:19], "%Y-%m-%dT%H:%M:%S"),
            )

            db.add(db_post)
            db.commit()
            db.refresh(db_post)

        db.query(models.Blog).filter(
            models.Blog.id == blog.id).update(
                {"last_uploaded_at": last_uploaded_at, "updated_at": str(datetime.datetime.now())})
        db.commit()
