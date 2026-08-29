from playwright.sync_api import sync_playwright


class BrowserManager:

    def __init__(self):

        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self):

        if self.browser is not None:
            return

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=False
        )

        self.context = self.browser.new_context()

        self.page = self.context.new_page()

    def stop(self):

        if self.browser is not None:
            self.browser.close()

        if self.playwright is not None:
            self.playwright.stop()

        self.browser = None
        self.context = None
        self.playwright = None
        self.page = None

    def ensure_started(self):

        if self.browser is None:
            self.start()

        return self.page