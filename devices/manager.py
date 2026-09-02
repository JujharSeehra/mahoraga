import json
from pathlib import Path
class DeviceManager:
    def __init__(self, config_path = None):
        if config_path is None:
            config_path = (Path(__file__).resolve().parent.parent/"config"/"devices.json")
        self.config_path = Path(config_path)
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.devices = {}
        self.load()
    def load(self):
        if not self.config_path.exists():
            self.devices = {}
            self.save()
            return
        with open(self.config_path, "r", encoding = "utf-8") as file:
            data = json.load(file)
        self.devices = data.get("devices", {})
    def save(self):
        with open(self.config_path, "w", encoding = "utf-8") as file:
            json.dump({"devices": self.devices}, file, indent = 4)
    def add_device( self, name, port, device_type = "unknown", baud_rate = 9600):
        name = name.strip()
        if not name:
            raise ValueError("Device name cannot be empty.")
        self. devices[name.lower()] = {
            "name": name,
            "port": port,
            "device_type": device_type,
            "baud_rate": baud_rate
        }
        self.save()
        return True
    def remove_device(self, name):
        key = name.lower()
        if key not in self.devices:
            return False
        del self.devices[key]
        self.save()
        return True
    def get_device(self, name):
        return self.devices.get(name.lower())
    def list_devices(self):
        return list(self.devices.values())