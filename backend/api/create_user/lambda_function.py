import database
import models
import json
from typing import Optional
from datetime import datetime


def lambda_handler(event, context):
    user_id = event.get("body", {}).get("user_id", None)
    email = event.get("body", {}).get("email", None)

    if user_id is None:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing user_id')
        }

    db = next(database.get_db())

    db_user: Optional[models.User] = db.query(
        models.User).filter(models.User.id == user_id).first()

    if db_user:
        return {
            'statusCode': 405,
            'headers': {'Content-Type': 'application/json; charset=utf-8', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps('User already exists')
        }

    db_user = models.User(
        id=user_id,
        email=email,
        is_subscribed=True,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json; charset=utf-8', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(
            {
                "id": db_user.id,
                "email": db_user.email,
                "is_subscribed": db_user.is_subscribed,
            }
        )
    }
