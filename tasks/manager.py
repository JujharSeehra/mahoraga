import json
from pathlib import Path
from datetime import datetime

class TaskManager:
    def __init__(self, config_path = None):
        if config_path is None:
            config_path = Path(__file__).resolve().parent.parent/"config"/"tasks.json"
        self.config_path = Path(config_path)
        self.config_path.parent.mkdir(parents = True, exist_ok=True)
        self.tasks = []
        self.load()
        