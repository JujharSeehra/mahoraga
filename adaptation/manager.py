class ExperienceManager:

    def __init__(self, database):

        self.database = database

    def record(self, experience):

        cursor = (
            self.database.connection
            .cursor()
        )

        cursor.execute(
            """
            INSERT INTO experiences
            (
                task,
                action,
                result,
                success,
                lesson,
                confidence
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                experience.task,
                experience.action,
                experience.result,
                int(experience.success),
                experience.lesson,
                experience.confidence,
            )
        )

        self.database.connection.commit()

    def successful_experiences(self):

        cursor = (
            self.database.connection
            .cursor()
        )

        cursor.execute(
            """
            SELECT
                task,
                action,
                result,
                lesson,
                confidence
            FROM experiences
            WHERE success = 1
            ORDER BY confidence DESC
            """
        )

        return cursor.fetchall()