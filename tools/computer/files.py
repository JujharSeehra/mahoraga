from tools.base import Tool


class SearchFilesTool(Tool):

    def __init__(self, workspace_manager):

        self.workspace_manager = (
            workspace_manager
        )

    @property
    def name(self):

        return "search_files"

    @property
    def description(self):

        return (
            "Search for files by filename "
            "inside an approved workspace."
        )

    def declaration(self):

        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "workspace": {
                        "type": "string",
                        "description": (
                            "Name of the approved "
                            "workspace to search."
                        )
                    },
                    "query": {
                        "type": "string",
                        "description": (
                            "Filename text to search for."
                        )
                    }
                },
                "required": [
                    "workspace",
                    "query"
                ]
            }
        }

    def execute(
        self,
        workspace,
        query
    ):

        root = (
            self.workspace_manager
            .get_workspace(workspace)
        )

        if root is None:

            raise ValueError(
                f"Unknown workspace: {workspace}"
            )

        query = query.lower()

        results = []

        for path in root.rglob("*"):

            if not path.is_file():
                continue

            if query in path.name.lower():

                results.append(
                    str(
                        path.relative_to(root)
                    )
                )

        return {
            "workspace": workspace,
            "query": query,
            "results": results[:50]
        }


class ListFilesTool(Tool):

    def __init__(self, workspace_manager):

        self.workspace_manager = (
            workspace_manager
        )

    @property
    def name(self):

        return "list_files"

    @property
    def description(self):

        return (
            "List files inside an approved workspace."
        )

    def declaration(self):

        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "workspace": {
                        "type": "string",
                        "description": (
                            "Name of the approved "
                            "workspace."
                        )
                    }
                },
                "required": [
                    "workspace"
                ]
            }
        }

    def execute(self, workspace):

        root = (
            self.workspace_manager
            .get_workspace(workspace)
        )

        if root is None:

            raise ValueError(
                f"Unknown workspace: {workspace}"
            )

        results = []

        for path in root.rglob("*"):

            if path.is_file():

                results.append(
                    str(
                        path.relative_to(root)
                    )
                )

        return {
            "workspace": workspace,
            "files": results[:200]
        }


class ReadFileTool(Tool):

    def __init__(self, workspace_manager):

        self.workspace_manager = (
            workspace_manager
        )

    @property
    def name(self):

        return "read_file"

    @property
    def description(self):

        return (
            "Read the contents of a text file "
            "inside an approved workspace."
        )

    def declaration(self):

        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "workspace": {
                        "type": "string",
                        "description": (
                            "Name of the approved "
                            "workspace."
                        )
                    },
                    "path": {
                        "type": "string",
                        "description": (
                            "Path to the file relative "
                            "to the workspace."
                        )
                    }
                },
                "required": [
                    "workspace",
                    "path"
                ]
            }
        }

    def execute(
        self,
        workspace,
        path
    ):

        root = (
            self.workspace_manager
            .get_workspace(workspace)
        )

        if root is None:

            raise ValueError(
                f"Unknown workspace: {workspace}"
            )

        target = (
            root / path
        ).resolve()

        try:

            target.relative_to(root)

        except ValueError:

            raise ValueError(
                "Access outside the workspace "
                "is not allowed."
            )

        if not target.exists():

            raise FileNotFoundError(
                f"File not found: {path}"
            )

        if not target.is_file():

            raise ValueError(
                "Target is not a file."
            )

        content = target.read_text(
            encoding="utf-8",
            errors="replace"
        )

        return {
            "workspace": workspace,
            "path": path,
            "content": content[:30000]
        }