from tools.base import Tool
class AddDeviceTool(Tool):
    def __init__(self, device_manager):
        self.device_manager = device_manager
    @property
    def name(self):
        return "add_device"
    @property
    def description(self):
        return "Save a hardware device with a friendly name so it can be used later without specifying it's serial port."
    def declaration(self):
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Friendly Name for the Device"
                    },
                    "port": {
                        "type": "string",
                        "description": "Serial port of the device"
                    },
                    "baud_rate": {
                        "type": "integer",
                        "description": "Serial Baud Rate"
                    }
                },
                "required": ["name", "port"]
            }
        }
    def execute(self, name, port, device_type = "unknown", baud_rate = 9600):
        self.device_manager.add_device(name=name, port=port, device_type=device_type, baud_rate = baud_rate)
        return {
            "status": "saved",
            "device": self.device_manager.get_device(name)
        }

class ListDevicesTool(Tool):

    def __init__(self, device_manager):
        self.device_manager = device_manager

    @property
    def name(self):
        return "list_devices"

    @property
    def description(self):
        return "List hardware devices that Mahoraga has saved."

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

        return {
            "status": "success",
            "devices": self.device_manager.list_devices()
        }

class RemoveDeviceTool(Tool):

    def __init__(self, device_manager):
        self.device_manager = device_manager

    @property
    def name(self):
        return "remove_device"

    @property
    def description(self):
        return "Remove a saved hardware device. This does not disconnect or modify the physical device."

    def declaration(self):
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the saved device."
                    }
                },
                "required": ["name"]
            }
        }

    def execute(self, name):
        removed = self.device_manager.remove_device(name)
        return {
            "status": "removed" if removed else "not_found",
            "name": name
        }