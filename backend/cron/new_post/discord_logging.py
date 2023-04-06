"""
디스코드 채널에 웹훅을 이용해서 로깅
"""

from typing import List
import aiohttp
import datetime
import os

DISCORD_WEBHOOKS_NEW_POST_UPLOAD_LOG = os.environ.get(
    "DISCORD_WEBHOOKS_NEW_POST_UPLOAD_LOG")


color = {
    "green": 0x2ECC71,
}


async def logging_new_post_upload(total_updated_blog_cnt: int, total_updated_posts: List[str]):
    async with aiohttp.ClientSession() as session:
        data = {
            "content": "",
            "embeds": [
                {
                    "title": "새 글 업데이트 로그",
                    "description": f"블로그 : `{total_updated_blog_cnt}`개\n포스트 : `{len(total_updated_posts)}`개",
                    "color": color["green"],
                    "footer": {
                        "text": f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    }
                }
            ]
        }

        if total_updated_posts:
            tmp = ""
            print(total_updated_posts)
            for post in total_updated_posts:
                tmp += post
            data["embeds"][0]["description"] += f"\n\n```{tmp}```"

        await session.post(
            url=DISCORD_WEBHOOKS_NEW_POST_UPLOAD_LOG,
            json=data
        )
