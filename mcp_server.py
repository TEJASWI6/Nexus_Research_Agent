import os
from mcp.server.fastmcp import FastMCP

from ddgs import DDGS

mcp = FastMCP("Dino-Research-Server")

@mcp.tool()
def read_local_research(keyword: str) -> str:
    """Searches local files for company info. Best with short keywords."""
    path = "./knowledge_base"
    if not os.path.exists(path): return "Error: knowledge_base folder missing."
    
    results = []
    # ADVANCED NORMALIZATION: Remove common 'noise' words that LLMs add
    noise = ['internal', 'the', 'our', 'what', 'is', 'policy', 'rules', 'check', 'my']
    search_words = [w.lower() for w in keyword.split() if w.lower() not in noise]
    
    # Fallback: if cleaning removes everything, use the original keyword
    if not search_words: search_words = keyword.lower().split()

    for file in os.listdir(path):
        if file.endswith(".txt"):
            with open(os.path.join(path, file), "r", encoding="utf-8") as f:
                content = f.read().lower()
                # Check if any significant word exists in the file
                if any(word in content for word in search_words if len(word) > 2):
                    results.append(f"SOURCE [{file}]: {content}")
    
    return "\n---\n".join(results) if results else "No local data found matching your query."

@mcp.tool()
def web_research(query: str) -> str:
    """
    Searches the live web using DuckDuckGo.
    Returns summarized search snippets for the LLM.
    Optimized for stability and clean agent responses.
    """

    
    from ddgs import DDGS

    try:
        # Basic query cleanup (safe normalization)
        clean_query = " ".join(query.strip().split())

        with DDGS() as ddgs:
            results = list(
                ddgs.text(
                    clean_query,
                    region="wt-wt",      # worldwide results
                    safesearch="moderate",
                    max_results=5
                )
            )

        if not results:
            return f"No relevant web results found for: '{clean_query}'."

        output = []

        for idx, r in enumerate(results, start=1):
            title = r.get("title", "No Title")
            snippet = r.get("body", r.get("description", "No description available"))
            link = r.get("href", r.get("link", "No link available"))

            output.append(
                f"[Result {idx}]\n"
                f"Title: {title}\n"
                f"Info: {snippet}\n"
                f"Source: {link}"
            )

        return "\n\n---\n\n".join(output)

    except Exception as e:
        return f"Web Search Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()