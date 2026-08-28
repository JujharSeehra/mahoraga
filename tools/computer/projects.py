from pathlib import Path

from tools.base import Tool
from tools.computer.path_manager import (WorkspaceManager)


class ListProjectsTool(Tool):
    name = "list_projects"
    description = ("Lists projects inside the Mahoraga workspace.")

    def __init__(self):
        self.workspace = (WorkspaceManager())

    def execute(self):
        projects = []
        for path in (self.workspace.workspace.iterdir()):
            if path.is_dir():
                projects.append(path.name)
        return projects