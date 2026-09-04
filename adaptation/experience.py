from dataclasses import dataclass


@dataclass
class Experience:
    task: str
    action: str
    result: str
    success: bool
    lesson: str
    confidence: float = 0.5