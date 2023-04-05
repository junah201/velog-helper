import database
import models
import json
from typing import Optional


def lambda_handler(event, context):
    user_id = event.get("pathParameters", {}).get("user_id", None)

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
            'headers': {'Content-Type': 'application/json; charset=utf-8', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps('User not found')
        }

    bookmarked_blogs = []
    for bookmark in db_user.bookmarks:
        bookmarked_blogs.append(bookmark.blog)

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json; charset=utf-8', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(
            [
                {
                    "id": blog.id,
                    "profile_img": blog.profile_img,
                }
                for blog in bookmarked_blogs
            ]
        )
    }
