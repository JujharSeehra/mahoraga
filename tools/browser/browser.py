from tools.base import Tool


class OpenURLTool(Tool):

    def __init__(self, browser_manager):

        self.browser = browser_manager

    @property
    def name(self):

        return "open_url"

    @property
    def description(self):

        return (
            "Open a website URL in Mahoraga's "
            "browser."
        )

    def declaration(self):

        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": (
                            "The complete website URL "
                            "to open."
                        )
                    }
                },
                "required": ["url"]
            }
        }

    def execute(self, url):

        page = self.browser.ensure_started()

        page.goto(
            url,
            wait_until="domcontentloaded"
        )

        return {
            "url": page.url,
            "title": page.title()
        }


class GetPageTextTool(Tool):

    def __init__(self, browser_manager):

        self.browser = browser_manager

    @property
    def name(self):

        return "get_page_text"

    @property
    def description(self):

        return (
            "Read the visible text from the "
            "currently open browser page."
        )

    def declaration(self):

        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }

    def execute(self):

        page = self.browser.ensure_started()

        text = (
            page
            .locator("body")
            .inner_text()
        )

        return {
            "url": page.url,
            "title": page.title(),
            "text": text[:30000]
        }


class ClickLinkTool(Tool):

    def __init__(self, browser_manager):

        self.browser = browser_manager

    @property
    def name(self):

        return "click_link"

    @property
    def description(self):

        return (
            "Click a link on the current browser page "
            "using visible link text."
        )

    def declaration(self):

        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": (
                            "Visible text of the link "
                            "to click."
                        )
                    }
                },
                "required": ["text"]
            }
        }

    def execute(self, text):

        page = self.browser.ensure_started()

        page.get_by_role(
            "link",
            name=text
        ).first.click()

        page.wait_for_load_state(
            "domcontentloaded"
        )

        return {
            "url": page.url,
            "title": page.title()
        }


class BrowserBackTool(Tool):

    def __init__(self, browser_manager):

        self.browser = browser_manager

    @property
    def name(self):

        return "browser_back"

    @property
    def description(self):

        return (
            "Navigate back to the previous page "
            "in the browser."
        )

    def declaration(self):

        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }

    def execute(self):

        page = self.browser.ensure_started()

        page.go_back(
            wait_until="domcontentloaded"
        )

        return {
            "url": page.url,
            "title": page.title()
        }