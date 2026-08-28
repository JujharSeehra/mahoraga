from abc import ABC, abstractmethod

class Tool(ABC):
    name = ""
    description = ""

    parameters = {
        "type": "object",
        "properties": {},
    }

    requiresConfirmation = False

    @abstractmethod
    def execute(self, **kwargs):
        pass
    def declaration(self):
        return {
            "type": "function",
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }