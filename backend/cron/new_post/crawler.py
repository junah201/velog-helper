import aiohttp
from typing import List

VELOG_API_URL = "https://v2.velog.io/graphql"

get_new_posts_query = """
query Posts($cursor: ID, $username: String, $temp_only: Boolean, $limit: Int) {
    posts(cursor: $cursor, username: $username, temp_only: $temp_only, limit: $limit) {
        id
        title
        short_description
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


async def get_new_posts(username: str, limit: int = 10, return_type: str = "List") -> List[dict]:
    async with aiohttp.ClientSession() as session:
        async with session.post(VELOG_API_URL, json={"query": get_new_posts_query, "variables": {"username": username, "limit": limit}}) as resp:
            assert resp.status == 200
            data = await resp.json()

            if return_type == "List":
                return data["data"]["posts"]

            if return_type == "Dict":
                result = {}

                for post in data["data"]["posts"]:
                    result[post["id"]] = post

                return result

            return data["data"]["posts"]
