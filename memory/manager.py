from memory.database import (
    MemoryDatabase
)


class MemoryManager:

    def __init__(self):

        self.database = MemoryDatabase()

    def remember(
        self,
        category,
        content,
        importance=0.5
    ):

        cursor = (
            self.database.connection
            .cursor()
        )

        cursor.execute(
            """
            INSERT INTO memories
            (category, content, importance)
            VALUES (?, ?, ?)
            """,
            (
                category,
                content,
                importance,
            )
        )

        self.database.connection.commit()

    def recall(self, category=None):

        cursor = (
            self.database.connection
            .cursor()
        )

        if category:

            cursor.execute(
                """
                SELECT content
                FROM memories
                WHERE category = ?
                ORDER BY importance DESC
                """,
                (category,)
            )

        else:

            cursor.execute(
                """
                SELECT content
                FROM memories
                ORDER BY importance DESC
                """
            )

        return [
            row[0]
            for row in cursor.fetchall()
        ]