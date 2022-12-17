import datetime
from sqlalchemy.orm import Session
from app.database import models
from app.utils.crawler import get_new_posts
from app.common.consts import VELOG_DEFAULT_PROFILE_IMG
from app.utils import mail
from app.utils.time_utils import UTC_to_KST, remove_milliseconds
from app.utils import crawler


async def update_new_post_by_blog(db: Session, blog: models.Blog, limit: int = 10, is_init: bool = False) -> None:
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


async def update_new_post(db: Session) -> None:
    db_blogs = db.query(models.Blog).all()
    for blog in db_blogs:
        await update_new_post_by_blog(db=db, blog=blog, limit=10)


async def update_edited_post(db: Session) -> None:
    # * : 수정 알림 기능은 일부 블로그에 한하여 제공함 (베타 기능)
    # * : 최근 3개월 이내 10개 글에 한하여 제공함
    # target_blog : mowinckel, velog test blog
    target_blog = ["mowinckel", "fdsfdafdsf"]
    # target_user : Junah201, roeniss2
    target_user = ["117995910119600379975", "108276358765267408445"]

    db_blogs = db.query(models.Blog).filter(
        models.Blog.id.in_(target_blog)).all()

    for db_blog in db_blogs:
        print("edit check", db_blog.id)

        db_posts = db.query(models.Post).filter(
            models.Post.user == db_blog.id and models.Post.updated_at > datetime.datetime.now() - datetime.datetime(month=3)).limit(10).all()

        if not db_posts:
            continue

        new_posts = await crawler.get_post_body_by_user(db_blog.id)

        for db_post in db_posts:
            print("수정 확인 중... ", db_post.title)

            # 삭제된 포스트
            if db_post.id not in new_posts.keys():
                continue

            # 만약 body의 해쉬값이 저장 안되어 있으면
            if not db_post.body_hash:
                db_post.body_hash = new_posts[db_post.id]["body_hash"]
                db.add(db_post)
                db.commit()
                db.refresh(db_post)
                continue

            # 만약 body의 해쉬값이 같으면
            if str(db_post.body_hash) == str(new_posts[db_post.id]["body_hash"]):
                continue

            print("수정됨... ", db_post.title)

            db_post.updated_at = new_posts[db_post.id]["updated_at"]
            db_post.title = new_posts[db_post.id]["title"]
            db_post.body_hash = new_posts[db_post.id]["body_hash"]

            db.add(db_post)
            db.commit()
            db.refresh(db_post)

            # 수정 안내 이메일 전송
            db_bookmarks = db.query(models.Bookmark).filter(
                models.Bookmark.blog == db_post.user and models.Bookmark.user.in_(target_user)).all()

            db_users = db.query(models.User).filter(
                models.User.id.in_([i.user for i in db_bookmarks])).all()

            for db_user in db_users:
                if not db_user.email:
                    continue
                if db_user.is_subscribed:
                    mail.send_edited_post_notice_email(
                        receiver_address=db_user.email, post=db_post, user_id=db_user.id)
