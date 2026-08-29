from google.genai import types
from memory.learning import LearningEngine
from memory.judge import LearningJudge
from memory.triggers import LearningTrigger

class Orchestrator:

    def __init__(
        self,
        brain,
        tools,
        memory=None,
        state_manager=None,
        permission_manager=None,
    ):

        self.brain = brain
        self.tools = tools
        self.memory = memory
        self.learning = (LearningEngine(self.memory) if self.memory else None)
        self.learning_judge = (LearningJudge(brain=self.brain, memory=self.memory) if self.memory else None)
        self.learning_trigger = ( LearningTrigger() if self.memory else None)
        self.state_manager = state_manager
        self.permission_manager = (permission_manager)

    def get_tool_declarations(self):

        return self.tools.declarations()

    def get_tool(self, name):

        return self.tools.get(name)

    def extract_function_calls(
        self,
        response
    ):

        calls = []

        for candidate in response.candidates:

            if candidate.content is None:
                continue

            for part in candidate.content.parts:

                if part.function_call:

                    calls.append(
                        part.function_call
                    )

        return calls

    def execute_tool(
        self,
        function_call
    ):

        name = function_call.name

        arguments = dict(
            function_call.args or {}
        )

        tool = self.get_tool(name)

        if tool is None:

            raise ValueError(
                f"Unknown tool requested: {name}"
            )

        if (
            self.permission_manager
            and self.permission_manager
            .requires_confirmation(name)
        ):

            raise PermissionError(
                f"Tool requires confirmation: {name}"
            )

        return tool.execute(
            **arguments
        )

    def get_memory_context(
        self,
        user_input,
        limit=5
    ):

        if self.memory is None:

            return ""

        try:

            memories = self.memory.recall(
                user_input,
                limit=limit
            )

        except Exception as error:

            print(
                f"Memory retrieval error: {error}"
            )

            return ""

        if not memories:

            return ""

        lines = [
            "RELEVANT LONG-TERM MEMORY:",
            ""
        ]

        for memory in memories:

            category = (
                memory.get("category")
                or "general"
            )

            project = (
                memory.get("project")
            )

            content = (
                memory.get("content")
                or ""
            )

            if project:

                lines.append(
                    f"[{category} | {project}] "
                    f"{content}"
                )

            else:

                lines.append(
                    f"[{category}] "
                    f"{content}"
                )

        lines.extend([
            "",
            "Use these memories when relevant.",
            "Do not assume a memory is correct "
            "if it conflicts with newer information."
        ])

        return "\n".join(lines)
    def learn_from_interaction(
        self,
        user_input,
        response
    ):

        if (
            self.learning_judge is None
            or self.learning_trigger is None
        ):

            return None

        if not self.learning_trigger.should_evaluate(
            user_input
        ):

            return None

        if hasattr(response, "text"):

            response_text = response.text

        else:

            response_text = str(response)

        result = (
            self.learning_judge
            .learn_from_interaction(
                user_input=user_input,
                assistant_response=response_text
            )
        )

        return result

    def run(self, user_input):

        memory_context = (
            self.get_memory_context(
                user_input
            )
        )

        if memory_context:

            initial_content = (
                f"{memory_context}\n\n"
                f"CURRENT USER REQUEST:\n"
                f"{user_input}"
            )

        else:

            initial_content = user_input

        contents = [
            initial_content
        ]

        for _ in range(10):

            response = (
                self.brain.think_with_tools(
                    contents,
                    self.get_tool_declarations()
                )
            )

            function_calls = (
                self.extract_function_calls(
                    response
                )
            )

            # Gemini has finished using tools.
            if not function_calls:

                return response

            # Give Gemini the model's previous
            # response so it knows which tool
            # calls it made.
            contents.append(
                response.candidates[0].content
            )

            for call in function_calls:

                result = self.execute_tool(
                    call
                )

                # Proper Gemini function-response
                # object.
                function_response = (
                    types.Part.from_function_response(
                        name=call.name,
                        response=result
                    )
                )

                contents.append(
                    function_response
                )

        raise RuntimeError(
            "Mahoraga reached the maximum "
            "number of tool calls."
        )