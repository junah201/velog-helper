import datetime
from sqlalchemy.orm import Session
from app.database import models
from app.utils.crawler import get_new_posts
from app.utils.mail import send_post_notice_email


async def update_new_post_by_blog(db: Session, blog: models.Blog, limit: int = 10, is_init: bool = False) -> None:
    posts = await get_new_posts(username=blog.id, limit=limit)
    if is_init:
        last_uploaded_at = datetime.datetime(2005, 2, 1)
    else:
        last_uploaded_at = datetime.datetime.strptime(
            posts[0]["released_at"][:19], "%Y-%m-%dT%H:%M:%S")
    for post in reversed(posts):
        post_upload_time = datetime.datetime.strptime(
            post["released_at"][:19], "%Y-%m-%dT%H:%M:%S")
        if post_upload_time <= blog.last_uploaded_at:
            continue

        # DB에 추가
        db_post = models.Post(
            id=post["id"],
            title=post["title"],
            user=post["user"]["username"],
            user_img=post["user"]["profile"]["thumbnail"],
            link=post["url_slug"],
            created_at=post_upload_time,
            updated_at=datetime.datetime.strptime(
                post["updated_at"][:19], "%Y-%m-%dT%H:%M:%S"),
        )

        db.add(db_post)
        db.commit()
        db.refresh(db_post)

        # TODO : 유저별로 이메일 전송 코드 작성
        db_users = db.query(models.Bookmark).filter(
            models.Bookmark.blog == db_post.user).all()
        print(db_users)
        for bookmarked_user in db_users:
            print(bookmarked_user)
            if bookmarked_user.email == None or bookmarked_user.email == "":
                continue
            print(1)
            send_post_notice_email(
                receiver_address=bookmarked_user.email, post=db_post)

    db.query(models.Blog).filter(
        models.Blog.id == blog.id).update(
            {"last_uploaded_at": last_uploaded_at, "updated_at": str(datetime.datetime.now())})
    db.commit()


async def update_new_post(db: Session) -> None:
    db_blogs = db.query(models.Blog).all()
    for blog in db_blogs:
        await update_new_post_by_blog(db=db, blog=blog, limit=10)
