from core.workspace_manager import (WorkspaceManager)

from tools.registry import (ToolRegistry)

from tools.computer.files import (SearchFilesTool, ListFilesTool, ReadFileTool, OpenFileTool)

from tools.browser.manager import BrowserManager

from tools.browser.browser import OpenURLTool, GetPageTextTool, ClickLinkTool, BrowserBackTool

#Add this code once we get brave: from tools.browser.search import (SearchWebTool)

from tools.computer.apps import OpenApplicationTool, OpenFolderTool, ListApplicationsTool, OpenInVSCodeTool

from tools.hardware.serial import ListSerialDevicesTool, ConnectSerialDeviceTool, DisconnectSerialDeviceTool, ReadSerialTool

from tools.hardware.serial_manager import SerialManager

from devices.manager import DeviceManager
from tools.hardware.devices import AddDeviceTool, ListDevicesTool, RemoveDeviceTool

def create_tool_registry():

    workspace_manager = (WorkspaceManager())

    browser_manager = BrowserManager()

    registry = ToolRegistry()

    serial_manager = SerialManager()

    device_manager = DeviceManager()

    registry.register(SearchFilesTool(workspace_manager))

    registry.register(ListFilesTool(workspace_manager))

    registry.register(ReadFileTool(workspace_manager))
    registry.register(OpenFileTool(workspace_manager))

    #registry.register(SearchWebTool(browser_manager))

    registry.register(OpenURLTool(browser_manager))

    registry.register(GetPageTextTool(browser_manager))

    registry.register(ClickLinkTool(browser_manager))

    registry.register(BrowserBackTool(browser_manager))

    registry.register(OpenApplicationTool())
    registry.register(ListApplicationsTool())

    registry.register(OpenFolderTool(workspace_manager))
    registry.register(OpenInVSCodeTool(workspace_manager))

    registry.register(ListSerialDevicesTool())

    registry.register(ConnectSerialDeviceTool(serial_manager))
    registry.register(DisconnectSerialDeviceTool(serial_manager))

    registry.register(ReadSerialTool(serial_manager))

    registry.register(AddDeviceTool(device_manager))
    registry.register(ListDevicesTool(device_manager))
    registry.register(RemoveDeviceTool(device_manager))


    return registry