import database
import models
import json
from typing import Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('./'),
    autoescape=select_autoescape(['html']),
)


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
            'statusCode': 405,
            'headers': {
                'Content-Type': 'application/json; charset=utf-8',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps('User already exists')
        }

    db_user.is_subscribed = True
    db.commit()
    db.refresh(db_user)

    subscription_template = env.get_template("subscription.html")

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json; charset=utf-8',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': subscription_template.render(user_id=user_id)
    }
