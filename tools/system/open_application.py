import subprocess


class OpenApplicationTool:

    name = "open_application"

    description = (
        "Open an installed macOS application by name. "
        "Use this when the user asks to launch an application "
        "such as VS Code, Safari, Terminal, Finder, or another "
        "installed Mac application."
    )

    parameters = {
        "type": "object",
        "properties": {
            "application": {
                "type": "string",
                "description": (
                    "The exact or recognizable name of the "
                    "macOS application to open."
                )
            }
        },
        "required": ["application"]
    }

    def execute(self, application):

        if not isinstance(application, str):
            raise ValueError("Application name must be a string.")

        application = application.strip()

        if not application:
            raise ValueError("Application name cannot be empty.")

        try:

            result = subprocess.run(["open","-a",application],capture_output=True,text=True,timeout=10)

        except subprocess.TimeoutExpired:

            return {
                "success": False,
                "application": application,
                "error": "Timed out while attempting to open the application."
            }

        except Exception as error:

            return {
                "success": False,
                "application": application,
                "error": str(error)
            }

        if result.returncode != 0:

            error = result.stderr.strip() or "macOS could not open the application."

            return {
                "success": False,
                "application": application,
                "error": error
            }

        return {
            "success": True,
            "application": application,
            "message": (f"Successfully opened {application}.")
        }