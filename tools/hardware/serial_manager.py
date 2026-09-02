import serial

class SerialManager:
    def __init__(self):
        self.connections = {}
    def connect(self, port, baud_rate = 9600):
        if port in self.connections:
            return {
                "status": "already_connected",
                "port": "port"
            }
        try:
            connection = serial.Serial(port = port, baudrate = baud_rate, timeout = 1)
        except Exception as error:
            return {
                "status": "error",
                "port": port,
                "error": str(error)
            }
        self.connections[port] = connection
        return {
            "status": "connected",
            "port": port,
            "baud_rate": baud_rate
        }
    def disconnect(self, port):
        connection = self.connections.get(port)
        if connection is None:
            return {
                "status": "not_connected",
                "port": port
            }
        try: 
            connection.close()
        except Exception as error:
            return {
                "status": "error",
                "port": port,
                "error": str(error)
            }
        del self.connections[port]
        return {
            "status": "disconnected",
            "port": port
        }
    def is_connected(self, port):
        return port in self.connections
    def list_connections(self):
        return list(self.connections.keys())
    def get_connection(self, port):
        return self.connections.get(port)