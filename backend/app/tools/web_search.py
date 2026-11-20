
from ddgs import DDGS


def web_search(query: str) -> dict:
    queries = [
        query,
        f"{query} Retrieval Augmented Generation",
        f"{query} AI agents tools workflows",
    ]

    all_results = []
    seen_urls = set()
    errors = []

    for search_query in queries:
        try:
            results = DDGS().text(
                search_query,
                max_results=5
            )

            for result in results:
                url = result.get("href", "")

                if url and url not in seen_urls:
                    seen_urls.add(url)

                    all_results.append({
                        "title": result.get("title", ""),
                        "body": result.get("body", ""),
                        "href": url,
                    })

            if len(all_results) >= 5:
                break

        except Exception as exc:
            errors.append({
                "query": search_query,
                "error": str(exc)
            })

    return {
        "tool": "web_search",
        "query": query,
        "results": all_results[:5],
        "errors": errors,
    }
