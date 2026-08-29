from PySide6.QtCore import QObject, Signal, Slot


class AgentWorker(QObject):

    finished = Signal(str)
    error = Signal(str)

    def __init__(self):
        super().__init__()

        self.agent = None

    @Slot()
    def initialize(self):

        try:

            # Import here so the agent is created
            # inside the worker thread.
            from core.agent import MahoragaAgent

            self.agent = MahoragaAgent()

        except Exception as errors:

            self.error.emit(
                str(errors)
            )

    @Slot(str)
    def process(self, message):

        try:

            if self.agent is None:

                raise RuntimeError(
                    "Mahoraga agent has not initialized."
                )

            response = self.agent.ask(
                message
            )

            self.finished.emit(
                response
            )

        except Exception as errors:

            self.error.emit(
                str(errors)
            )