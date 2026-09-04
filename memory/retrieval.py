import re

from memory.database import MemoryDatabase


class MemoryRetriever:

    def __init__(self, database=None):

        self.database = (database or MemoryDatabase())

    def _tokenize(self, text):

        words = re.findall(r"[a-zA-Z0-9]+",text.lower())

        return [word for word in words if len(word) > 2]

    def search(self,query,limit=5):

        words = self._tokenize(query)

        if not words:
            return []

        conditions = []
        parameters = []

        for word in words:

            conditions.append( """(LOWER(content) LIKE ? OR LOWER(category) LIKE ? OR LOWER(project) LIKE ? OR LOWER(source) LIKE ?""")

            pattern = f"%{word}%"

            parameters.extend([pattern,pattern,pattern,pattern])

        sql = f"""SELECT id, content, category,source, project,importance,created_at,last_used_at, use_count FROM memories WHERE {" OR ".join(conditions)} ORDER BY importance DESC, created_at DESC LIMIT ?"""

        parameters.append(limit)

        rows = self.database.connection.execute(sql,parameters).fetchall()

        return [dict(row) for row in rows]

    def format_results(self,results):

        if not results:
            return ("No relevant memories found.")

        lines = []

        for memory in results:

            category = (memory.get("category")or "general")

            project = memory.get("project")
            content = (memory.get("content") or "")

            if project:
                lines.append(f"[{category} | {project}] {content}")

            else:
                lines.append(f"[{category}] {content}")

        return "\n".join(lines)