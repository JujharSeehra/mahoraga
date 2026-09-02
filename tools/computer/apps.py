import subprocess

from tools.base import Tool


class OpenApplicationTool(Tool):

    @property
    def name(self):

        return "open_application"

    @property
    def description(self):

        return (
            "Open an installed macOS application "
            "by its name."
        )

    def declaration(self):

        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "application": {
                        "type": "string",
                        "description": (
                            "Name of the macOS application "
                            "to open."
                        )
                    }
                },
                "required": ["application"]
            }
        }

    def execute(self, application):

        subprocess.Popen(
            [
                "open",
                "-a",
                application
            ]
        )

        return {
            "application": application,
            "status": "opened"
        }


class OpenFolderTool(Tool):

    @property
    def name(self):

        return "open_folder"

    @property
    def description(self):

        return (
            "Open an approved workspace folder "
            "in Finder."
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
                "required": ["workspace"]
            }
        }

    def __init__(self, workspace_manager):

        self.workspace_manager = (
            workspace_manager
        )

    def execute(self, workspace):

        path = (
            self.workspace_manager
            .get_workspace(workspace)
        )

        if path is None:

            raise ValueError(
                f"Unknown workspace: {workspace}"
            )

        subprocess.Popen(
            [
                "open",
                str(path)
            ]
        )

        return {
            "workspace": workspace,
            "path": str(path),
            "status": "opened"
        }
class ListApplicationsTool(Tool):

    @property
    def name(self):

        return "list_applications"

    @property
    def description(self):

        return (
            "List installed macOS applications. "
            "Use this when you need to discover "
            "the exact name of an installed application."
        )

    def declaration(self):

        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }

    def execute(self):

        try:

            result = subprocess.run(
                [
                    "find",
                    "/Applications",
                    "/System/Applications",
                    "-maxdepth",
                    "2",
                    "-name",
                    "*.app",
                    "-type",
                    "d"
                ],
                capture_output=True,
                text=True,
                timeout=10
            )

        except Exception as error:

            return {
                "status": "error",
                "error": str(error)
            }

        applications = []

        for line in result.stdout.splitlines():

            line = line.strip()

            if not line:
                continue

            name = line.rsplit(
                "/",
                1
            )[-1]

            if name.endswith(".app"):

                name = name[:-4]

            applications.append(name)

        applications = sorted(
            set(applications),
            key=str.lower
        )

        return {
            "status": "success",
            "count": len(applications),
            "applications": applications
        }

class OpenInVSCodeTool(Tool):
    @property
    def name(self):
        return "open_in_vscode"
    @property
    def description(self):
        return "Open an approved workspace or a specific file inside an approved worskpace in VS Code."
    def declaration(self):
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "workspace": {
                        "type": "string",
                        "description": "Name of the approved workspace"
                    },
                    "path": {
                        "type": "string",
                        "description": "Optional path to a file or folder relative to the workspace. If ommited, the entire workspace is opened"
                    }
                },
                "required": ["workspace"]
            }
        }
    def __init__(self, workspace_manager):
        self.workspace_manager = workspace_manager
    def execute(self, workspace, path = None):
        root = (self.workspace_manager.get_workspace(workspace))
        if root is None:
            raise ValueError(f"Unknown workspace: {workspace}")
        if path is None or not path.strip():
            target = root.resolve()
        else: 
            target = (root/path).resolve()
            try:
                target.relative_to(root)
            except ValueError:
                raise ValueError("Access outside the workspace is not allowed.")
        if not target.exists():
            raise FileNotFoundError(f"Path not found: {path}")
        try:
            result = subprocess.run(["/usr/local/bin/code",str(target)],capture_output=True,text=True,timeout=10)
        except FileNotFoundError:
            return {
                "workspace": workspace,
                "path": path,
                "status": "error",
                "error": (
                    "The 'code' command was not found. "
                    "Install the VS Code command-line "
                    "command and try again."
                )
            }

        except Exception as error:

            return {
                "workspace": workspace,
                "path": path,
                "status": "error",
                "error": str(error)
            }

        if result.returncode != 0:

            return {
                "workspace": workspace,
                "path": path,
                "status": "error",
                "error": (
                    result.stderr.strip()
                    or "VS Code failed to open the path."
                )
            }

        return {
            "workspace": workspace,
            "path": path,
            "status": "opened_in_vscode"
        }