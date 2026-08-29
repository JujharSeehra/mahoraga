from tools.computer.apps import (
    ListApplicationsTool
)


tool = ListApplicationsTool()

result = tool.execute()

print(
    "STATUS:",
    result["status"]
)

print(
    "APPLICATION COUNT:",
    result["count"]
)

print(
    "\nFIRST APPLICATIONS:"
)

for application in result["applications"][:30]:

    print(
        "-",
        application
    )