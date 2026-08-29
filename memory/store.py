from memory.database import MemoryDatabase
class MemoryStore:
    def __init__(self):
        self.database = MemoryDatabase()
    def remember(self, content, category = "general", source = None, project = None, importance = 1):
        return self.database.insert(content = content, category = category, source = source, project = project, importance= importance)

        