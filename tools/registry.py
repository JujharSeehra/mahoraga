class ToolRegistry:
    def __init__(self):
        self.tools = {}
    def register(self, tool):
        name = tool.name
        if name in self.tools:
            raise ValueError(f"Tool already exists: {name}")
        self.tools[name] = tool
    def get(self, name):
        return self.tools.get(name)
    def all(self):
        return list(self.tools.values())
    def describe(self):
        descriptions = []
        for tool in self.tools.values():
            descriptions.append({
                "name": tool.name,
                "description": tool.description,
            })
        return descriptions