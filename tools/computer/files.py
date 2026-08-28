from tools.base import Tool
from tools.computer.path_manager import (WorkspaceManager)


class SearchFilesTool(Tool):

    name = "search_files"
    description = ("Searches files inside the Mahoraga workspace for a filename or text pattern.")
    parameters = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": ("Filename or text to search for."),
            },
            "required": ["query"],
        }
    }
    def __init__(self):
        self.workspace = (WorkspaceManager())

    def execute(self, query):
        results = []
        query = query.lower()
        for path in self.workspace.workspace.rglob("*"):

            if not path.is_file():
                continue
            if query in path.name.lower():
                relative = path.relative_to(self.workspace.workspace)
                results.append(str(relative))

        return results[:50]
class ReadFileTool(Tool):
    name = "read_file"
    description = ("Reads a text file inside the Mahoraga workspace.")
    parameters = {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": (
                    "Path relative to the workspace."
                )
            }
        },
        "required": ["path"]
    }
    def __init__(self):
        self.workspace = (WorkspaceManager())

    def execute(self, path):
        file_path = (self.workspace.resolve(path))

        if not file_path.is_file():
            raise FileNotFoundError(f"File not found: {path}")

        return file_path.read_text(encoding="utf-8")