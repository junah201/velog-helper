import database
import models
import json
from typing import Optional


def lambda_handler(event, context):
    blog_id = event.get("pathParameters", {}).get("blog_id", None)

    if blog_id is None:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json; charset=utf-8',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps('Missing blog_id')
        }

    db = next(database.get_db())

    db_blog: Optional[models.Blog] = db.query(
        models.Blog).filter(models.Blog.id == blog_id).first()

    if db_blog is None:
        return {
            'statusCode': 404,
            'headers': {
                'Content-Type': 'application/json; charset=utf-8',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps('Blog not found')
        }

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json; charset=utf-8',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': len(db_blog.bookmarks)
    }
