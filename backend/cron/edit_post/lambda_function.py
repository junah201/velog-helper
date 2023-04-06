import new_post
import asyncio


def lambda_handler(event, context):
    asyncio.run(new_post.update_new_post())

    return {
        'statusCode': 200,
        'body': "Success"
    }
