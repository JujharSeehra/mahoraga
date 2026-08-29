class PermissionManager:

    def __init__(self):

        self.always_allowed = {
            "search_files",
            "read_file",
            "list_projects",
            "system_info",

            "open_folder",
        }

    def requires_confirmation(self, tool_name):

        return tool_name not in self.always_allowed