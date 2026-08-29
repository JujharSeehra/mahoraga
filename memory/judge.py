import json
from memory.learning import LearningEngine

class LearningJudge:
    def __init__(self, brain, memory = None):
        self.brain = brain
        self.learning = (LearningEngine(memory) if memory else LearningEngine())
    def evaluate(self, user_input, assistant_response):
        prompt = f"""
You are Mahoraga's Learning Judge.

Your job is to determine whether the interaction
contains useful information that should be remembered
for future tasks.

Only remember information that is genuinely reusable.

Do NOT remember:
- greetings
- casual conversation
- temporary details
- obvious facts
- the user's current question by itself
- ordinary assistant responses
- information that would not help in the future

Potentially remember:
- useful project facts
- successful solutions
- reusable procedures
- important failures
- durable user preferences
- technical discoveries
- important constraints

Return ONLY valid JSON.

The JSON must have this structure:

{{
    "should_remember": true,
    "category": "solution",
    "importance": 5,
    "project": "Mahoraga",
    "memory": "Short reusable description."
}}

If nothing should be remembered, return:

{{
    "should_remember": false
}}

Allowed categories:

- fact
- preference
- project
- solution
- procedure
- failure
- general

Importance must be an integer from 1 to 5.

The memory should be concise and useful.

USER REQUEST:
{user_input}

ASSISTANT RESPONSE:
{assistant_response}
"""

        try:

            response = self.brain.think(
                prompt
            )

            return self._parse_response(
                response
            )

        except Exception as error:

            print(
                f"Learning judge error: {error}"
            )

            return {
                "should_remember": False
            }

    def _parse_response(
        self,
        response
    ):

        text = response.strip()

        # Handle accidental markdown fences.
        if text.startswith("```"):

            lines = text.splitlines()

            lines = [
                line
                for line in lines
                if not line.strip().startswith("```")
            ]

            text = "\n".join(lines).strip()

        try:

            data = json.loads(text)

        except json.JSONDecodeError:

            return {
                "should_remember": False
            }

        if not isinstance(data, dict):

            return {
                "should_remember": False
            }

        if not data.get(
            "should_remember",
            False
        ):

            return {
                "should_remember": False
            }

        memory = data.get(
            "memory"
        )

        if not isinstance(
            memory,
            str
        ) or not memory.strip():

            return {
                "should_remember": False
            }

        category = data.get(
            "category",
            "general"
        )

        allowed_categories = {
            "fact",
            "preference",
            "project",
            "solution",
            "procedure",
            "failure",
            "general"
        }

        if category not in allowed_categories:

            category = "general"

        importance = data.get(
            "importance",
            3
        )

        try:

            importance = int(
                importance
            )

        except (
            TypeError,
            ValueError
        ):

            importance = 3

        importance = max(
            1,
            min(5, importance)
        )

        project = data.get(
            "project"
        )

        if project is not None:

            if not isinstance(
                project,
                str
            ):

                project = None

            elif not project.strip():

                project = None

        return {
            "should_remember": True,
            "category": category,
            "importance": importance,
            "project": project,
            "memory": memory.strip()
        }

    def learn_from_interaction(
        self,
        user_input,
        assistant_response
    ):

        decision = self.evaluate(
            user_input,
            assistant_response
        )

        if not decision.get(
            "should_remember"
        ):

            return None

        memory_id = self.learning.learn(
            content=decision["memory"],
            category=decision["category"],
            project=decision["project"],
            source="learning_judge",
            importance=decision["importance"]
        )

        return {
            "memory_id": memory_id,
            "memory": decision["memory"],
            "category": decision["category"],
            "importance": decision["importance"],
            "project": decision["project"]
        }