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
            'headers': {
                'Content-Type': 'application/json; charset=utf-8',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps('Missing user_id')
        }

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

    db_bookmark: Optional[models.Bookmark] = db.query(
        models.Bookmark).filter(models.Bookmark.user_id == user_id).filter(models.Bookmark.blog_id == blog_id).first()

    if db_bookmark is None:
        return {
            'statusCode': 404,
            'headers': {
                'Content-Type': 'application/json; charset=utf-8',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps('Bookmark not found')
        }

    db.delete(db_bookmark)
    db.commit()

    return {
        'statusCode': 204,
        'headers': {
            'Content-Type': 'application/json; charset=utf-8',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': ""
    }
