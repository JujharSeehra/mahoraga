from memory.database import MemoryDatabase
from memory.store import MemoryStore
from memory.retrieval import MemoryRetriever


class MemoryManager:

    def __init__(self):
        self.database = MemoryDatabase()
        self.store = MemoryStore()
        self.retriever = MemoryRetriever(self.database)

    def remember(self,content,category="general",source=None,project=None,importance=1):
        existing = self.recall(content,limit=10)

        normalized_new = (content.strip().lower())

        for memory in existing:
            normalized_existing = (memory["content"].strip().lower())
            if normalized_new == normalized_existing:
                return memory["id"]

        return self.store.remember(content=content,category=category,source=source,project=project,importance=importance)

    def recall(self,query,limit=5):

        return self.retriever.search(query,limit)

    def recall_text( self,query,limit=5):

        memories = self.recall(query,limit)

        return self.retriever.format_results(memories)