import os

from google import genai
from google.genai import types
from core.config import config


class GeminiBrain:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")

        self.client = genai.Client(api_key=api_key)

        self.model = config.GEMINI_MODEL
    def think(self, prompt: str) -> str:

        response = self.chat.send_message(prompt)
        return response.text
    def think_with_tools(self, contents, tool_declarations,):
        config = types.GenerateContentConfig(tools = [types.Tool(function_declarations = [types.FunctionDeclaration(name = tool["name"], description = tool["description"], parameters = tool["parameters"],) for tool in tool_declarations])])
        response = self.client.models.generate_content(model = self.model, contents = contents, config = config,)
        return response