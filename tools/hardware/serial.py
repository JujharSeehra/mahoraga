import glob
from tools.base import Tool
class ListSerialDevicesTool(Tool):
    @property
    def name(self):
        return "list_serial_devices"
    @property
    def description(self):
        return ("List serial and USB communication devices currently connected to the Mac. Use this to discover Arduino, ESP32, Raspberry Pi, and other devices that use Serial.")
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
        patterns = ["/dev/cu.*", "/dev/tty.*"]
        devices = []
        for pattern in patterns:
            devices.extend(glob.glob(pattern))
        devices = sorted(set(devices))
        return {
            "status": "success",
            "count": len(devices),
            "devices": devices
        }

from tools.hardware.serial_manager import SerialManager

class ConnectSerialDeviceTool(Tool):
    def __init__(self, serial_manager):
        self.serial_manager = serial_manager
    @property
    def name(self):
        return "connect_serial_device"
    @property
    def description(self):
        return "Connect to a serial device such as an Arduino, ESP32, Teensy, or other USB serial device"
    def declaration(self):
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                     "port": {
                        "type": "string",
                        "description": "Serial device path, such as /dev/cu.usbmoden1101"
                    },
                    "baud_rate": {
                        "type": "integer",
                        "description": "Serial Communication speed, common values include 9600 and 115200"
                    }
                },
                "required": ["port"]
            }
        }
    def execute(self, port, baud_rate = 9600):
        return self.serial_manager.connect(port, baud_rate)
class DisconnectSerialDeviceTool(Tool):

    def __init__(self, serial_manager):

        self.serial_manager = (serial_manager)

    @property
    def name(self):
        return "disconnect_serial_device"

    @property
    def description(self):
        return "Disconnect from a currently connected serial device."

    def declaration(self):
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "port": {
                        "type": "string",
                        "description": "Serial device path to disconnect."
                    }
                },
                "required": ["port"]
            }
        }

    def execute(self, port):
        return self.serial_manager.disconnect(port)
class ReadSerialTool(Tool):
    def __init__(self, serial_manager):
        self.serial_manager= serial_manager
    @property
    def name(self):
        return "read_serial"
    @property
    def description(self):
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "port": {
                        "type": "string",
                        "description": "Serial Device Path"
                    },
                    "max_lines": {
                        "type": "integet",
                        "description": "Maximum number of lines to read"
                    }
                },
                "required": ["port"]
            }
        }
    def execute(self, port, max_lines = 20):
        connection = self.serial_manager.get_connection(port)
        if connection is None:
            return {
                "status": "error",
                "port": port,
                "error": "Device is not connected"
            }
        lines = []
        try:
            for _ in range(max_lines):
                if not connection.in_waiting:
                    break
                line = connection.readline().decode("utf-8", errors = "replace").strip()
                if line:
                    lines.append(line)
        except Exception as errors:
            return {
                "status": "error",
                "port": port,
                "error": str(errors)
            }
        return {
            "status": "success",
            "port": port,
            "lines": lines,
            "count": len(lines)
        }