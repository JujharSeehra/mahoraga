from brain.gemini import GeminiBrain
from brain.prompts import SYSTEM_PROMPT


class MahoragaAgent:

    def __init__(self):
        self.brain = GeminiBrain()

    def ask(self, user_input: str) -> str:

        prompt = f""" {SYSTEM_PROMPT}

USER: {user_input}

Respond to the user. """

        return self.brain.think(prompt)