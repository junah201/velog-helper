import database
import models
import json
from typing import Optional


def lambda_handler(event, context):
    user_id = event.get("pathParameters", {}).get("user_id", None)
    skip = event.get("queryStringParameters", {}).get("skip", 0)
    limit = event.get("queryStringParameters", {}).get("limit", 15)

    if user_id is None:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing user_id')
        }

    db = next(database.get_db())

    db_user: Optional[models.User] = db.query(
        models.User).filter(models.User.id == user_id).first()

    if db_user is None:
        return {
            'statusCode': 404,
            'headers': {
                'Content-Type': 'application/json; charset=utf-8',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps('User not found')
        }

    bookmarked_blogs = [
        bookmark.blog_id for bookmark in db_user.bookmarks]

    db_posts = db.query(models.Post).filter(
        models.Post.blog_id.in_(bookmarked_blogs)).order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all()

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json; charset=utf-8',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(
            [
                {
                    "id": post.id,
                    "title": post.title,
                    "blog_id": post.blog_id,
                    "blog_img": post.blog_img,
                    "link": post.link,
                    "short_description": post.short_description,
                    "created_at": post.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": post.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for post in db_posts
            ]
        )
    }
