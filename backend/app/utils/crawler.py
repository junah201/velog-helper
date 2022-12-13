import aiohttp
from app.common.consts import VELOG_API_URL, VELOG_DEFAULT_PROFILE_IMG
from typing import List

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


async def get_new_posts(username: str, limit: int = 10, return_type="List") -> List[dict]:
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

get_user_profile_query = """
query UserProfile($username: String!) {
    user(username: $username) {
        profile {
            thumbnail
        }
    }
}
"""


async def get_user_profile(username: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post(VELOG_API_URL, json={"query": get_user_profile_query, "variables": {"username": username}}) as resp:
            assert resp.status == 200
            data = await resp.json()
            if data["data"]["user"]["profile"]["thumbnail"] == None:
                return VELOG_DEFAULT_PROFILE_IMG
            return data["data"]["user"]["profile"]["thumbnail"]
