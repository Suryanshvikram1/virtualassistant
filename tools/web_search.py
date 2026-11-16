from ddgs import DDGS
def search_web(query, max_results=5):
    try:
        results = list(DDGS().text(query, max_results=max_results))
        if not results:
            return "No search results found."
        return "Search results: " + " ".join(
            f"{i}. {r.get('title','')} — {r.get('body','')} Link: {r.get('href','')}"
            for i, r in enumerate(results, 1)
        )
    except Exception as exc:
        print(f"Web search error: {exc}")
        return "Web search is unavailable right now."
