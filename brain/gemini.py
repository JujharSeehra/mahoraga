from google import genai

from core.config import config


class GeminiBrain:

    def __init__(self):
        if not config.GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY was not found in .env"
            )

        self.client = genai.Client(
            api_key=config.GEMINI_API_KEY
        )

        self.model = config.GEMINI_MODEL

        self.chat = self.client.chats.create(
            model=self.model
        )

    def think(self, prompt: str) -> str:

        response = self.chat.send_message(
            prompt
        )

        return response.text