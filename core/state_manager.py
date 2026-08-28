from PySide6.QtCore import QObject, Signal
from core.state import MahoragaState
class StateManager(QObject):
    state_changed = Signal(object)
    def __init__(self):
        super().__init__()
        self.state = (MahoragaState.IDLE)
    def set_state(self, state):
        if self.state == state:
            return
        self.state = state
        self.state_changed.emit(state)
    def get_state(self):
        return self.state