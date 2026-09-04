from google import genai
from google.genai import types
from core.config import config


class GeminiBrain:

    def __init__(self):
        if not config.GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY was not found in .env")

        self.client = genai.Client(api_key=config.GEMINI_API_KEY)

        self.model = config.GEMINI_MODEL

        self.chat = self.client.chats.create(model=self.model)

    def think(self, prompt: str) -> str:

        response = self.chat.send_message(prompt)
        return response.text
    def think_with_tools(self, contents, tool_declarations,):
        config = types.GenerateContentConfig(tools = [types.Tool(function_declarations = [types.FunctionDeclaration(name = tool["name"], description = tool["description"], parameters = tool["parameters"],) for tool in tool_declarations])])
        response = self.client.models.generate_content(model = self.model, contents = contents, config = config,)
        return response