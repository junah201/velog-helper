import database
import models
import json
from typing import Optional


def lambda_handler(event, context):
    user_id = event.get("pathParameters", {}).get("user_id", None)
    email = event.get("body", {}).get("email", None)

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

    db = next(database.get_db())

    db_user: Optional[models.User] = db.query(
        models.User).filter(models.User.id == user_id).first()

    if db_user:
        return {
            'statusCode': 405,
            'headers': {
                'Content-Type': 'application/json; charset=utf-8',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps('User already exists')
        }

    db_user.email = email
    db.commit()
    db.refresh(db_user)

    return {
        'statusCode': 204,
        'headers': {
            'Content-Type': 'application/json; charset=utf-8',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': ""
    }
