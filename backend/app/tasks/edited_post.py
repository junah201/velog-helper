import datetime
from sqlalchemy.orm import Session
from app.database import models
from app.utils import mail, discord_logging
from app.utils.crawler import get_post_body_by_user


async def update_edited_post_by_blog(db: Session, blog: models.Blog) -> int:
    edited_post_cnt: int = 0

    # target_user : Junah201, roeniss2
    target_user = ["117995910119600379975", "108276358765267408445"]

    db_posts = db.query(models.Post).filter(
        models.Post.user == blog.id and models.Post.updated_at > datetime.datetime.now() - datetime.datetime(month=3)).limit(10).all()

    if not db_posts:
        return edited_post_cnt

    new_posts = await get_post_body_by_user(blog.id)

    for db_post in db_posts:
        print("수정 확인 중... ", db_post.title)

        # 삭제된 포스트
        if db_post.id not in new_posts.keys():
            print(f"삭제된 포스트")
            continue

        # 만약 body의 해쉬값이 저장 안되어 있으면
        if not db_post.body_hash:
            db_post.body_hash = new_posts[db_post.id]["body_hash"]
            db.add(db_post)
            db.commit()
            db.refresh(db_post)
            print(f"해쉬값 저장 안됨 {db_post.body_hash}")
            continue

        # 만약 body의 해쉬값이 같으면
        if str(db_post.body_hash) == str(new_posts[db_post.id]["body_hash"]):
            continue

        print("수정됨... ", db_post.title)

        edited_post_cnt += 1

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
                mail.send_edited_post_notice_email(receiver_address=db_user.email, post=db_post, user_id=db_user.id)

    return edited_post_cnt


async def update_edited_post(db: Session) -> None:
    # * : 수정 알림 기능은 일부 블로그에 한하여 제공함 (베타 기능)
    # * : 최근 3개월 이내 10개 글에 한하여 제공함
    # target_blog : mowinckel, velog test blog
    target_blog = ["mowinckel", "fdsfdafdsf"]

    total_updated_blog_cnt: int = 0
    total_updated_post_cnt: int = 0

    db_blogs = db.query(models.Blog).filter(
        models.Blog.id.in_(target_blog)).all()

    for db_blog in db_blogs:
        edited_post: int = await update_edited_post_by_blog(db=db, blog=db_blog)

        if edited_post:
            total_updated_blog_cnt += 1
            total_updated_post_cnt += edited_post

    await discord_logging.logging_post_update(total_updated_blog_cnt, total_updated_post_cnt)
