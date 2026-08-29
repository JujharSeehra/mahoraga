from google.genai import types


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
        self.state_manager = state_manager
        self.permission_manager = (
            permission_manager
        )

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

    def run(self, user_input):

        contents = [
            user_input
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