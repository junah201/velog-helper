import database
import models
import json
from typing import Optional


def lambda_handler(event, context):
    user_id = event.get("pathParameters", {}).get("user_id", None)
    blog_id = event.get("pathParameters", {}).get("blog_id", None)

    if user_id is None:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing user_id')
        }

    if blog_id is None:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing blog_id')
        }

    db = next(database.get_db())

    db_bookmark: Optional[models.Bookmark] = db.query(
        models.Bookmark).filter(models.Bookmark.user_id == user_id).filter(models.Bookmark.blog_id == blog_id).first()

    if db_bookmark is None:
        return {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json; charset=utf-8', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps('Bookmark not found')
        }

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json; charset=utf-8', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(
            {
                "id": db_bookmark.id,
                "user_id": db_bookmark.user_id,
                "blog_id": db_bookmark.blog_id,
            }
        )
    }
