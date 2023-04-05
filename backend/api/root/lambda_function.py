import json
import datetime


def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps(f"Notification API (UTC: {datetime.datetime.utcnow().strftime('%Y.%m.%d %H:%M:%S')})")
    }
