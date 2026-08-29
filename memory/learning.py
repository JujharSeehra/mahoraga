from memory.manager import MemoryManager


class LearningEngine:

    def __init__(self, memory=None):

        self.memory = (
            memory or MemoryManager()
        )

    def learn(
        self,
        content,
        category="general",
        project=None,
        source="interaction",
        importance=3
    ):

        if not content:
            return None

        content = content.strip()

        if not content:
            return None

        return self.memory.remember(
            content=content,
            category=category,
            project=project,
            source=source,
            importance=importance
        )

    def learn_solution(
        self,
        problem,
        solution,
        project=None,
        importance=5
    ):

        content = (
            f"Problem: {problem}\n"
            f"Solution: {solution}"
        )

        return self.learn(
            content=content,
            category="solution",
            project=project,
            source="successful_solution",
            importance=importance
        )

    def learn_procedure(
        self,
        task,
        procedure,
        project=None,
        importance=5
    ):

        content = (
            f"Task: {task}\n"
            f"Procedure: {procedure}"
        )

        return self.learn(
            content=content,
            category="procedure",
            project=project,
            source="successful_procedure",
            importance=importance
        )

    def learn_failure(
        self,
        problem,
        failed_approach,
        project=None,
        importance=4
    ):

        content = (
            f"Problem: {problem}\n"
            f"Failed approach: "
            f"{failed_approach}"
        )

        return self.learn(
            content=content,
            category="failure",
            project=project,
            source="failed_attempt",
            importance=importance
        )