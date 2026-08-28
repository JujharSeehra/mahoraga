from brain.gemini import GeminiBrain
from brain.prompts import SYSTEM_PROMPT
from tools.defaults import (create_default_registry)
from memory.manager import (MemoryManager)


class MahoragaAgent:
    def __init__(self):
        self.brain = GeminiBrain()
        self.conversation = []
        self.tools = create_default_registry()
        self.memory = MemoryManager()

    def ask(self, user_input: str):
        self.conversation.append({"role": "user",
                                  "content": user_input})
        prompt = self.build_prompt()
        response = self.brain.think(prompt)
        self.conversation.append({"role": "assistant",
                                  "content": response})
        return response

    def build_prompt(self):
        conversation_text = ""
        for message in self.conversation:
            role = message["role"]
            content = message["content"]
            conversation_text += (f"{role.upper()}: {content}\n")
        return f"{SYSTEM_PROMPT}    \nConversation: {conversation_text} \nRespond to the latest user message"
    def remember(self, content):
        self.memory.remember(category = "user", content = content, importance = 0.8)
        return "Memory Stored"
    def recall(self):
        return self.memory.recall()