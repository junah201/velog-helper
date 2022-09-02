import asyncio
import aiohttp
import json
from app.common.consts import VELOG_API_URL

query = """
query Posts($cursor: ID, $username: String, $temp_only: Boolean, $limit: Int) {
    posts(cursor: $cursor, username: $username, temp_only: $temp_only, limit: $limit) {
        id
        title
        short_description
        thumbnail
        user {
        username
        profile {
            thumbnail
        }
        }
        url_slug
        released_at
        updated_at
        comments_count
        tags
        likes
    }
}
"""

query = """
query Posts($cursor: ID, $username: String, $temp_only: Boolean, $limit: Int) {
    posts(cursor: $cursor, username: $username, temp_only: $temp_only, limit: $limit) {
        id
        title
        user {
        username
        profile {
            thumbnail
        }
        }
        url_slug
        released_at
        updated_at
    }
}
"""


async def get_new_posts(username: str, limit: int = 10):
    async with aiohttp.ClientSession() as session:
        async with session.post(VELOG_API_URL, json={"query": query, "variables": {"username": username, "limit": limit}}) as resp:
            assert resp.status == 200
            data = await resp.json()
            return data["data"]["posts"]
