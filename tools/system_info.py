import platform

from tools.base import Tool

class SystemInfoTool(Tool):
    name = "system_info"
    description = ("Returns basic information about the computer.")
    def execute(self):
        return {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": platform.python_version(),
        }