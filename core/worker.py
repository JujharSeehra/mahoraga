from PySide6.QtCore import (QObject, Signal, Slot)

class AgentWorker(QObject):
    finished = Signal(str)
    error = Signal(str)
    def __init__(self, agent):
        super().__init__()
        self.agent = agent
    @Slot(str)
    def process(self, message):
        try:
            response = self.agent.ask(message)

            self.finished.emit(response)
        except Exception as errors:
            self.error.emit(str(errors))