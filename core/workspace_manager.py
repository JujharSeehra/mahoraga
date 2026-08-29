import json
from pathlib import Path


class WorkspaceManager:

    def __init__(self, config_path=None):

        if config_path is None:

            config_path = (
                Path(__file__).resolve().parent.parent
                / "config"
                / "workspaces.json"
            )

        self.config_path = Path(
            config_path
        )

        self.config_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.workspaces = []

        self.load()

    def load(self):

        if not self.config_path.exists():

            self.workspaces = []

            self.save()

            return

        with open(
            self.config_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        self.workspaces = data.get(
            "workspaces",
            []
        )

    def save(self):

        with open(
            self.config_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                {
                    "workspaces": self.workspaces
                },
                file,
                indent=4
            )

    def add_workspace(
        self,
        name,
        path
    ):

        path = (
            Path(path)
            .expanduser()
            .resolve()
        )

        if not path.exists():

            raise ValueError(
                f"Workspace does not exist: {path}"
            )

        if not path.is_dir():

            raise ValueError(
                f"Workspace is not a directory: {path}"
            )

        for workspace in self.workspaces:

            if workspace["path"] == str(path):

                return False

        self.workspaces.append({
            "name": name,
            "path": str(path)
        })

        self.save()

        return True

    def remove_workspace(self, name):

        original_count = len(
            self.workspaces
        )

        self.workspaces = [
            workspace
            for workspace in self.workspaces
            if workspace["name"].lower()
            != name.lower()
        ]

        changed = (
            len(self.workspaces)
            != original_count
        )

        if changed:
            self.save()

        return changed

    def get_workspace(self, name):

        for workspace in self.workspaces:

            if (
                workspace["name"].lower()
                == name.lower()
            ):

                return Path(
                    workspace["path"]
                )

        return None

    def list_workspaces(self):

        return self.workspaces.copy()