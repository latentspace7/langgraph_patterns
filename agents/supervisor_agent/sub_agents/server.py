import re
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP

app = FastMCP("demo-stdio-mcp")


@app.tool()
def slugify(text: str) -> str:
    """
    Convert arbitrary text into a URL-friendly slug.
    Examples:
      "Hello, World!" -> "hello-world"
      "  Spaces & symbols %% " -> "spaces-symbols"
    """
    # lowercase
    s = text.lower()
    # replace non alphanum with hyphens
    s = re.sub(r"[^a-z0-9]+", "-", s)
    # collapse hyphens + strip
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or ""


@app.tool()
def word_count(text: str, unique: bool = False) -> Dict[str, Any]:
    """
    Count words in text. If unique=True, also return a per-word frequency map.
    """
    # tokenize words (letters/digits/underscore treated as word chars)
    words = re.findall(r"\w+", text.lower())
    total = len(words)
    result: Dict[str, Any] = {"total": total}
    if unique:
        freq: Dict[str, int] = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1
        result["unique"] = len(freq)
        result["freq"] = freq
    return result


if __name__ == "__main__":

    app.run()
