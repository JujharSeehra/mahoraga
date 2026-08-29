from tools.base import Tool


class SearchWebTool(Tool):

    def __init__(self, browser_manager):

        self.browser = browser_manager

    @property
    def name(self):

        return "search_web"

    @property
    def description(self):

        return (
            "Search the web using Mahoraga's browser "
            "and return relevant search results."
        )

    def declaration(self):

        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "The search query."
                        )
                    }
                },
                "required": ["query"]
            }
        }

    def execute(self, query):

        page = self.browser.ensure_started()

        search_url = (
            "https://www.google.com/search"
        )

        page.goto(
            search_url,
            wait_until="domcontentloaded"
        )

        page.locator(
            "textarea[name='q']"
        ).fill(query)

        page.locator(
            "textarea[name='q']"
        ).press("Enter")

        page.wait_for_load_state(
            "domcontentloaded"
        )

        results = []

        links = page.locator(
            "a"
        )

        count = links.count()

        for i in range(count):

            link = links.nth(i)

            try:

                title = link.inner_text(
                    timeout=500
                ).strip()

                href = link.get_attribute(
                    "href",
                    timeout=500
                )

            except Exception:

                continue

            if not title or not href:
                continue

            if not href.startswith("http"):
                continue

            if "google.com" in href:
                continue

            results.append({
                "title": title,
                "url": href
            })

            if len(results) >= 10:
                break

        return {
            "query": query,
            "results": results,
            "url": page.url,
            "title": page.title()
        }