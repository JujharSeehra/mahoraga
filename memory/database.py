import sqlite3
from pathlib import Path


class MemoryDatabase:

    def __init__(self):

        self.directory = (Path.home() / ".mahoraga")
        self.directory.mkdir(parents=True,exist_ok=True)
        self.path = (self.directory / "memory.db")
        self.connection = sqlite3.connect(self.path,check_same_thread=False)
        self.connection.row_factory = (sqlite3.Row)
        self._initialize()

    def _initialize(self):

        self.connection.execute( """ CREATE TABLE IF NOT EXISTS memories ( id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT NOT NULL, category TEXT DEFAULT 'general',source TEXT, project TEXT, importance INTEGER DEFAULT 1, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, last_used_at TIMESTAMP, use_count INTEGER DEFAULT 0 ) """)
        self.connection.commit()

    def insert(self,content,category="general",source=None,project=None,importance=1):

        cursor = self.connection.execute(
            """INSERT INTO memories (content,category,source,project,importance) VALUES (?, ?, ?, ?, ?)""",(content,category,source,project,importance))

        self.connection.commit()
        return cursor.lastrowid

    def close(self):
        self.connection.close()