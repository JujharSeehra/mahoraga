from pathlib import Path

from core.config import config


class WorkspaceManager:

    def __init__(self):

        self.workspace = (config.WORKSPACE.resolve())

    def resolve(self, path):

        candidate = (self.workspace / path).resolve()

        try:
            candidate.relative_to(self.workspace)
        except ValueError:
            raise PermissionError("Path is outside Mahoraga's workspace.")

        return candidate