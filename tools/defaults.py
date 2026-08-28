from tools.registry import ToolRegistry
from tools.computer.files import (SearchFilesTool,ReadFileTool,)
from tools.system_info import (SystemInfoTool)

def create_default_registry():
    registry = ToolRegistry()
    registry.register(SearchFilesTool())
    registry.register(ReadFileTool())
    registry.register(SystemInfoTool())
    return registry