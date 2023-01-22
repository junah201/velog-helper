import aiohttp
from app.database.schemas import SearchResults, SearchResult
from app.common.config import GOOGLE_API_KEY, GOOGLE_SEARCH_ENGINE_ID


async def google_search(query: str, page: int = 1):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={GOOGLE_SEARCH_ENGINE_ID}&q={query}&start={page}") as resp:
            row_data = await resp.json()
            if row_data.get("error"):
                raise Exception(row_data["error"]["message"])

            print(row_data)

            results = SearchResults(
                total=int(row_data["searchInformation"]["totalResults"])
            )
            for item in row_data["items"]:
                results.results.append(
                    SearchResult(
                        title=item["title"],
                        html_title=item["htmlTitle"],
                        link=item["link"],
                        snippet=item["snippet"],
                        html_snippet=item["htmlSnippet"],
                        thumbnail_link=item["pagemap"]["cse_image"][0]["src"] or item["pagemap"][
                            "cse_thumbnail"][0]["src"] or item["pagemap"]["metatags"][0]["og:image"],
                    )
                )
            return results
