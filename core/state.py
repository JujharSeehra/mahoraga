from enum import Enum

class MahoragaState(Enum):
    OFFLINE = "offline"
    IDLE = "idle"
    THINKING = "thinking"
    USING_TOOL = "using_tool"
    LEARNING = "learning"
    ERROR = "error"