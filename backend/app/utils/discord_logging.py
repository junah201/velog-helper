"""
디스코드 채널에 웹훅을 이용해서 로깅
"""

from discord import Webhook, Embed, Color
import aiohttp, datetime
from app.common.config import DISCORD_WEBHOOKS_NEW_POST_UPLOAD_LOG, DISCORD_WEBHOOKS_POST_UPDATE_LOG

async def logging_new_post_upload(total_updated_blog_cnt, total_updated_post_cnt):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(
            url=DISCORD_WEBHOOKS_NEW_POST_UPLOAD_LOG,
            session=session
            )

        embed = Embed(
            title="새 글 업데이트 로그", description=f"블로그 : `{total_updated_blog_cnt}`개\n포스트 : `{total_updated_post_cnt}`개", color=Color.green())
        embed.set_footer(
            text=f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        await webhook.send(embed=embed)

async def logging_post_update(total_edited_blog_cnt, total_edited_post_cnt):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(
            url=DISCORD_WEBHOOKS_POST_UPDATE_LOG,
            session=session
            )

        embed = Embed(
            title="수정된 글 업데이트 로그", description=f"블로그 : `{total_edited_blog_cnt}`개\n포스트 : `{total_edited_post_cnt}`개", color=Color.green())
        embed.set_footer(
            text=f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        await webhook.send(embed=embed)