from core.workspace_manager import (
    WorkspaceManager
)

from tools.registry import (
    ToolRegistry
)

from tools.computer.files import (
    SearchFilesTool,
    ListFilesTool,
    ReadFileTool,
)

from tools.browser.manager import (
    BrowserManager
)

from tools.browser.browser import (
    OpenURLTool,
    GetPageTextTool,
    ClickLinkTool,
    BrowserBackTool,
)

#Add this code once we get brave: from tools.browser.search import (SearchWebTool)

from tools.computer.apps import (
    OpenApplicationTool,
    OpenFolderTool,
)


def create_tool_registry():

    workspace_manager = (
        WorkspaceManager()
    )

    browser_manager = BrowserManager()

    registry = ToolRegistry()

    registry.register(
        SearchFilesTool(
            workspace_manager
        )
    )

    registry.register(
        ListFilesTool(
            workspace_manager
        )
    )

    registry.register(
        ReadFileTool(
            workspace_manager
        )
    )

    #registry.register(SearchWebTool(browser_manager))

    registry.register(
        OpenURLTool(
            browser_manager
        )
    )

    registry.register(
        GetPageTextTool(
            browser_manager
        )
    )

    registry.register(
        ClickLinkTool(
            browser_manager
        )
    )

    registry.register(
        BrowserBackTool(
            browser_manager
        )
    )

    registry.register(
        OpenApplicationTool()
    )

    registry.register(
        OpenFolderTool(
            workspace_manager
        )
    )

    return registry