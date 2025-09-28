from langchain_core.tools import tool
import httpx


@tool
def fetch_top_ai_posts():
    """
        Fetches the top 5 AI-related posts from the LocalLLaMA subreddit on Reddit.
        This function makes an HTTP GET request to retrieve the 
        hottest posts from r/LocalLLaMA subreddit. It limits the results to 5 posts
        and extracts key information.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )}
    url = "https://www.reddit.com/r/LocalLLaMA.json"
    params = {"limit": 5}

    with httpx.Client(headers=headers, params=params) as client:
        resp = client.get(url=url)
        resp.raise_for_status()
        data = resp.json()

    posts = []
    for child in data["data"]["children"]:
        post = child["data"]

        if post.get("stickied") or post.get("promoted") or post.get("pinned"):
            continue

        posts.append({
            "title": post["title"],
            "url": post["url"],
            "score": post["score"],
            "author": post["author"],
            "permalink": f"https://reddit.com{post['permalink']}",
        })
    return posts
