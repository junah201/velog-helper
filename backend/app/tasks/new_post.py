import datetime
from sqlalchemy.orm import Session
from app.database import models
from app.utils.crawler import get_new_posts
from app.common.consts import VELOG_DEFAULT_PROFILE_IMG
from app.utils import mail, discord_logging
from app.utils.time_utils import UTC_to_KST


async def update_new_post_by_blog(db: Session, blog: models.Blog, limit: int = 10, is_init: bool = False) -> int:
    updated_post_cnt: int = 0

    posts = await get_new_posts(username=blog.id, limit=limit, return_type="List")

    if is_init:
        blog.last_uploaded_at = datetime.datetime(2005, 2, 1)

    for post in reversed(posts):
        post_uploaded_at = UTC_to_KST(datetime.datetime.strptime(
            post["released_at"][:19], "%Y-%m-%dT%H:%M:%S"))

        if post_uploaded_at <= blog.last_uploaded_at:
            continue

        if db.query(models.Post).filter(models.Post.id == post["id"]).first():
            continue

        updated_post_cnt += 1

        # DB에 추가
        db_post = models.Post(
            id=post["id"],
            title=post["title"],
            user=post["user"]["username"],
            user_img=post["user"]["profile"]["thumbnail"] if post["user"]["profile"]["thumbnail"] else VELOG_DEFAULT_PROFILE_IMG,
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
            models.Bookmark.blog == db_post.user).all()

        for bookmarked_user in db_users:
            db_user = db.query(models.User).filter(
                models.User.id == bookmarked_user.user).first()
            if not db_user.email:
                continue

            if db_user.is_subscribed and not is_init:
                mail.send_new_post_notice_email(receiver_address=db_user.email, post=db_post, user_id=db_user.id)

    last_uploaded_at = datetime.datetime.now()
    if posts:
        last_uploaded_at = UTC_to_KST(datetime.datetime.strptime(
            posts[0]["released_at"][:19], "%Y-%m-%dT%H:%M:%S"))

    db.query(models.Blog).filter(
        models.Blog.id == blog.id).update(
            {"last_uploaded_at": last_uploaded_at,
             "updated_at": str(datetime.datetime.now())})
    db.commit()

    return updated_post_cnt


async def update_new_post(db: Session) -> None:
    total_updated_blog_cnt: int = 0
    total_updated_post_cnt: int = 0
    db_blogs = db.query(models.Blog).all()
    for blog in db_blogs:
        updated_post_cnt = await update_new_post_by_blog(db=db, blog=blog, limit=10)
        if updated_post_cnt:
            total_updated_blog_cnt += 1
            total_updated_post_cnt += updated_post_cnt

    await discord_logging.logging_new_post_upload(total_updated_blog_cnt, total_updated_post_cnt)
