from brain.gemini import GeminiBrain
from brain.prompts import SYSTEM_PROMPT
from memory.manager import MemoryManager
from core.orchestrator import Orchestrator
from core.tool_setup import create_tool_registry


class MahoragaAgent:

    def __init__(self):

        self.brain = GeminiBrain()

        self.conversation = []

        self.tools = create_tool_registry()

        self.memory = MemoryManager()

        self.orchestrator = Orchestrator(
            brain=self.brain,
            tools=self.tools,
            memory=self.memory
        )

    def ask(self, user_input: str):

        self.conversation.append({
            "role": "user",
            "content": user_input
        })

        response = self.orchestrator.run(
            user_input
        )

        # Gemini's final response may be a
        # GenerateContentResponse object.
        if hasattr(response, "text"):

            response_text = response.text

        else:

            response_text = str(response)

        self.conversation.append({
            "role": "assistant",
            "content": response_text
        })

        return response_text

    def build_prompt(self):

        conversation_text = ""

        for message in self.conversation:

            role = message["role"]

            content = message["content"]

            conversation_text += (
                f"{role.upper()}: {content}\n"
            )

        return (
            f"{SYSTEM_PROMPT}\n"
            f"Conversation:\n"
            f"{conversation_text}\n"
            f"Respond to the latest user message."
        )

    def remember(self, content):

        self.memory.remember(
            category="user",
            content=content,
            importance=0.8
        )

        return "Memory Stored"

    def recall(self):

        return self.memory.recall()

    def ask_with_tools(self, user_input):

        return self.orchestrator.run(
            user_input
        )