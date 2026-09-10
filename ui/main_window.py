import json
from pathlib import Path
from PySide6.QtCore import Qt, QThread, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QWidget,QVBoxLayout,QHBoxLayout,QPushButton,QLabel,QFrame, QStackedWidget, QMessageBox, QScrollArea, QTextBrowser, QGridLayout

from core.worker import AgentWorker
from ui.chat import ChatPage

class MainWindow(QMainWindow):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent
        self.setWindowTitle("Mahoraga")
        self.setMinimumSize(1180,720)
        self.resize(1280,800)
        self.setWindowIcon(QIcon("icon/mahoraga.png"))
        self.nav_buttons = []
        self.build_ui()
        self.setup_worker()
        self.refresh_all_pages()
    def build_ui(self):

        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(235)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 22, 16, 18)
        sidebar_layout.setSpacing(5)

        brand_row = QHBoxLayout()
        brand_row.setSpacing(10)

        brand_icon = QLabel("◉")
        brand_icon.setObjectName("brand_icon")

        title = QLabel("MAHORAGA")
        title.setObjectName("title")

        brand_row.addWidget(brand_icon)
        brand_row.addWidget(title)
        brand_row.addStretch()

        sidebar_layout.addLayout(brand_row)

        subtitle = QLabel("PERSONAL INTELLIGENCE SYSTEM")
        subtitle.setObjectName("sidebar_subtitle")
        sidebar_layout.addWidget(subtitle)

        sidebar_layout.addSpacing(28)

        nav_label = QLabel("NAVIGATION")
        nav_label.setObjectName("section_label")
        sidebar_layout.addWidget(nav_label)

        sidebar_layout.addSpacing(5)

        self.chat_button = self.create_nav_button("◉", "Chat")
        self.tasks_button = self.create_nav_button("✓", "Tasks")
        self.memory_button = self.create_nav_button("◇", "Memory")
        self.computer_button = self.create_nav_button("▣", "Computer")
        self.browser_button = self.create_nav_button("◈", "Browser")
        self.devices_button = self.create_nav_button("⬡", "Hardware")
        self.tools_button = self.create_nav_button("⚡", "Tools")

        self.settings_button = self.create_nav_button("⚙", "Settings")

        self.nav_buttons = [self.chat_button, self.tasks_button, self.memory_button, self.computer_button, self.browser_button, self.devices_button, self.tools_button, self.settings_button]
        for button in self.nav_buttons:
            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()

        system_card = QFrame()
        system_card.setObjectName("sidebar_status_card")

        system_layout = QVBoxLayout(system_card)
        system_layout.setContentsMargins(13, 11, 13, 11)

        system_header = QHBoxLayout()

        self.sidebar_status_dot = QLabel("●")
        self.sidebar_status_dot.setObjectName("status_dot")

        sidebar_status = QLabel("SYSTEM ONLINE")
        sidebar_status.setObjectName("sidebar_status")

        system_header.addWidget(self.sidebar_status_dot)
        system_header.addWidget(sidebar_status)
        system_header.addStretch()

        system_layout.addLayout(system_header)

        self.sidebar_status_detail = QLabel("AI core ready")
        self.sidebar_status_detail.setObjectName("sidebar_status_detail")

        system_layout.addWidget(self.sidebar_status_detail)

        sidebar_layout.addWidget(system_card)

        sidebar_layout.addSpacing(10)

        self.exit_button = QPushButton("  EXIT MAHORAGA")
        self.exit_button.setObjectName("exit_button")
        self.exit_button.setMinimumHeight(42)
        self.exit_button.clicked.connect(self.confirm_exit)

        sidebar_layout.addWidget(self.exit_button)
        content = QWidget()
        content.setObjectName("content")

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(72)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(28, 0, 28, 0)

        header_left = QVBoxLayout()
        header_left.setSpacing(1)

        self.header_title = QLabel("Chat")
        self.header_title.setObjectName("header_title")

        self.header_subtitle = QLabel("Talk to your personal intelligence system")
        self.header_subtitle.setObjectName("header_subtitle")

        header_left.addWidget(self.header_title)
        header_left.addWidget(self.header_subtitle)

        header_layout.addLayout(header_left)
        header_layout.addStretch()

        header_status_frame = QFrame()
        header_status_frame.setObjectName("header_status")

        header_status_layout = QHBoxLayout(header_status_frame)
        header_status_layout.setContentsMargins(13, 7, 13, 7)
        header_status_layout.setSpacing(8)

        self.header_status_dot = QLabel("●")
        self.header_status_dot.setObjectName("header_status_dot")

        self.header_status = QLabel("READY")
        self.header_status.setObjectName("header_status_text")

        header_status_layout.addWidget(self.header_status_dot)
        header_status_layout.addWidget(self.header_status)

        header_layout.addWidget(header_status_frame)

        content_layout.addWidget(header)

        self.pages = QStackedWidget()
        self.pages.setObjectName("pages")

        self.chat_page = ChatPage()

        self.dashboard_page = self.create_dashboard_page()
        self.tasks_page = self.create_tasks_page()
        self.memory_page = self.create_memory_page()
        self.computer_page = self.create_computer_page()
        self.browser_page = self.create_browser_page()
        self.devices_page = self.create_devices_page()
        self.tools_page = self.create_tools_page()
        self.settings_page = self.create_settings_page()

        pages = [
            self.chat_page,
            self.dashboard_page,
            self.tasks_page,
            self.memory_page,
            self.computer_page,
            self.browser_page,
            self.devices_page,
            self.tools_page,
            self.settings_page,
        ]

        for page in pages:
            self.pages.addWidget(page)

        content_layout.addWidget(self.pages)

        bottom = QFrame()
        bottom.setObjectName("bottom_bar")
        bottom.setFixedHeight(44)

        bottom_layout = QHBoxLayout(bottom)
        bottom_layout.setContentsMargins(22, 0, 22, 0)

        self.bottom_status = QLabel("● READY")
        self.bottom_status.setObjectName("bottom_status")

        bottom_layout.addWidget(self.bottom_status)
        bottom_layout.addStretch()

        self.bottom_info = QLabel("Mahoraga Intelligence Core")
        self.bottom_info.setObjectName("bottom_info")

        bottom_layout.addWidget(self.bottom_info)

        content_layout.addWidget(bottom)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)

        self.chat_button.clicked.connect(lambda: self.switch_page(0, "Chat"))
        self.tasks_button.clicked.connect(lambda: self.switch_page(2, "Tasks"))
        self.memory_button.clicked.connect(lambda: self.switch_page(3, "Memory"))
        self.computer_button.clicked.connect(lambda: self.switch_page(4, "Computer"))
        self.browser_button.clicked.connect(lambda: self.switch_page(5, "Browser"))
        self.devices_button.clicked.connect(lambda: self.switch_page(6, "Hardware"))
        self.tools_button.clicked.connect(lambda: self.switch_page(7, "Tools"))
        self.settings_button.clicked.connect(lambda: self.switch_page(8, "Settings"))

        self.switch_page(0, "Chat")

    def create_nav_button(self, icon, text):

        button = QPushButton(f"{icon}    {text}")
        button.setObjectName("nav_button")
        button.setProperty("active", False)
        button.setMinimumHeight(44)

        return button

    def switch_page(self, index, title):

        self.pages.setCurrentIndex(index)

        for button in self.nav_buttons:
            button.setProperty("active", False)
            button.style().unpolish(button)
            button.style().polish(button)

        button_map = {
            0: self.chat_button,
            2: self.tasks_button,
            3: self.memory_button,
            4: self.computer_button,
            5: self.browser_button,
            6: self.devices_button,
            7: self.tools_button,
            8: self.settings_button,
        }

        active_button = button_map.get(index)

        if active_button:
            active_button.setProperty("active", True)
            active_button.style().unpolish(active_button)
            active_button.style().polish(active_button)

        self.header_title.setText(title)

        subtitles = {
            "Chat": "Talk to your personal intelligence system",
            "Tasks": "Manage persistent objectives and progress",
            "Memory": "Inspect Mahoraga's long-term knowledge",
            "Computer": "Access approved files, folders and applications",
            "Browser": "Control the integrated web browser",
            "Hardware": "Inspect connected devices and serial interfaces",
            "Tools": "View the capabilities available to Mahoraga",
            "Settings": "Inspect system configuration and runtime state",
        }

        self.header_subtitle.setText(subtitles.get(title, "Mahoraga control interface"))

        if title == "Tasks":
            self.refresh_tasks()

        elif title == "Memory":
            self.refresh_memory()

        elif title == "Computer":
            self.refresh_computer()

        elif title == "Browser":
            self.refresh_browser()

        elif title == "Hardware":
            self.refresh_devices()

        elif title == "Tools":
            self.refresh_tools()

        elif title == "Settings":
            self.refresh_settings()

    def create_dashboard_page(self):

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 26, 30, 26)
        layout.setSpacing(18)

        welcome = QLabel("MAHORAGA COMMAND CENTER")
        welcome.setObjectName("page_title")

        description = QLabel("A live overview of your personal intelligence system.")
        description.setObjectName("subtitle")

        layout.addWidget(welcome)
        layout.addWidget(description)

        hero = QFrame()
        hero.setObjectName("hero_card")

        hero_layout = QHBoxLayout(hero)
        hero_layout.setContentsMargins(30, 25, 30, 25)

        from ui.widgets.wheel import MahoragaWheel

        self.dashboard_wheel = MahoragaWheel()
        self.dashboard_wheel.setFixedSize(300, 300)

        hero_layout.addWidget(self.dashboard_wheel)

        hero_info = QVBoxLayout()
        hero_info.setSpacing(12)

        online = QLabel("SYSTEM OPERATIONAL")
        online.setObjectName("hero_status")

        hero_info.addWidget(online)

        hero_heading = QLabel("Mahoraga is ready.")
        hero_heading.setObjectName("hero_heading")

        hero_info.addWidget(hero_heading)

        hero_description = QLabel("Your AI core can reason, use tools, access approved "
            "workspaces, interact with hardware and maintain memory.")
        hero_description.setObjectName("hero_description")
        hero_description.setWordWrap(True)

        hero_info.addWidget(hero_description)

        hero_info.addSpacing(10)

        self.dashboard_runtime = QLabel("Runtime: Initializing...")
        self.dashboard_runtime.setObjectName("info_text")

        hero_info.addWidget(self.dashboard_runtime)

        self.dashboard_model = QLabel("Model: Loading...")
        self.dashboard_model.setObjectName("info_text")

        hero_info.addWidget(self.dashboard_model)

        hero_info.addStretch()

        refresh = QPushButton("↻ REFRESH SYSTEM")
        refresh.setObjectName("secondary_button")
        refresh.clicked.connect(self.refresh_all_pages)

        hero_info.addWidget(refresh)

        hero_layout.addLayout(hero_info)

        layout.addWidget(hero)
        stats = QGridLayout()
        stats.setSpacing(14)

        self.stat_memory = self.create_stat_card("MEMORY", "0", "stored memories")

        self.stat_tasks = self.create_stat_card("TASKS", "0", "saved tasks")

        self.stat_devices = self.create_stat_card("DEVICES", "0", "registered devices")

        self.stat_tools = self.create_stat_card("TOOLS", "0", "available capabilities")

        stats.addWidget(self.stat_memory, 0, 0)
        stats.addWidget(self.stat_tasks, 0, 1)
        stats.addWidget(self.stat_devices, 0, 2)
        stats.addWidget(self.stat_tools, 0, 3)

        layout.addLayout(stats)
        layout.addStretch()

        return page

    def create_stat_card(self, name, value, description):

        card = QFrame()
        card.setObjectName("stat_card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 15, 18, 15)
        layout.setSpacing(2)

        name_label = QLabel(name)
        name_label.setObjectName("stat_name")

        value_label = QLabel(value)
        value_label.setObjectName("stat_value")

        description_label = QLabel(description)
        description_label.setObjectName("stat_description")

        layout.addWidget(name_label)
        layout.addWidget(value_label)
        layout.addWidget(description_label)

        card.value_label = value_label

        return card

    def create_tasks_page(self):

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 26, 30, 26)
        layout.setSpacing(16)

        title = QLabel("TASKS")
        title.setObjectName("page_title")

        subtitle = QLabel("Persistent objectives stored by Mahoraga.")
        subtitle.setObjectName("subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        top = QHBoxLayout()

        self.task_summary = QLabel("Loading tasks...")
        self.task_summary.setObjectName("section_heading")

        top.addWidget(self.task_summary)
        top.addStretch()

        refresh = QPushButton("↻  REFRESH")
        refresh.setObjectName("secondary_button")
        refresh.clicked.connect(self.refresh_tasks)

        top.addWidget(refresh)

        layout.addLayout(top)

        self.tasks_view = QTextBrowser()
        self.tasks_view.setObjectName("data_view")

        layout.addWidget(self.tasks_view)

        return page

    def refresh_tasks(self):

        path = Path("config/tasks.json")

        if not path.exists():
            self.tasks_view.setText("No task database found.\n\n Create a task through the task system to see it here.")            
            self.task_summary.setText("No task database")
            return

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, dict):
                tasks = data.get("tasks", data)
            else:
                tasks = data

            if not isinstance(tasks, list):
                tasks = []

            self.task_summary.setText(f"{len(tasks)} persistent task(s)")
            if not tasks:
                self.tasks_view.setText("NO ACTIVE TASKS\n\n Your persistent task system is ready.")
                return

            output = []

            for index, task in enumerate(tasks, start=1):

                if isinstance(task, dict):
                    title = task.get( "title", task.get("name", f"Task {index}"))

                    status = task.get( "status", "unknown")

                    output.append(f"{index}. {title}\n STATUS  {status}\n")

                    if "description" in task:
                        output.append(f"DESCRIPTION  {task['description']}\n")

                    if "steps" in task:
                        steps = task["steps"]

                        if isinstance(steps, list):
                            for step_number, step in enumerate(steps, start=1):
                                if isinstance(step, dict):
                                    step_text = step.get("title", step.get( "description", str(step)))
                                    completed = step.get("completed", False )
                                else:
                                    step_text = str(step)
                                    completed = False

                                marker = "✓" if completed else "○"

                                output.append(f"  {marker} {step_number}. {step_text}\n")

                else:
                    output.append(f"{index}. {task}\n")

            self.tasks_view.setText("".join(output))

        except Exception as error:

            self.tasks_view.setText(f"Unable to read task database.\n\n{error}")

    def create_memory_page(self):

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 26, 30, 26)
        layout.setSpacing(16)

        title = QLabel("MEMORY")
        title.setObjectName("page_title")

        subtitle = QLabel("Inspect information currently available to Mahoraga.")
        subtitle.setObjectName("subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        top = QHBoxLayout()

        self.memory_summary = QLabel("Loading memory...")
        self.memory_summary.setObjectName("section_heading")

        top.addWidget(self.memory_summary)
        top.addStretch()

        refresh = QPushButton("↻  REFRESH")
        refresh.setObjectName("secondary_button")
        refresh.clicked.connect(self.refresh_memory)

        top.addWidget(refresh)

        layout.addLayout(top)

        self.memory_view = QTextBrowser()
        self.memory_view.setObjectName("data_view")

        layout.addWidget(self.memory_view)

        return page

    def refresh_memory(self):

        try:

            memories = self.agent.memory.recall()

            if memories is None:
                memories = []

            if not isinstance(memories, list):
                memories = [memories]

            self.memory_summary.setText(f"{len(memories)} memory item(s)")
            if not memories:
                self.memory_view.setText("NO MEMORIES FOUND\n\n Mahoraga's long-term memory is currently empty.")
                return

            output = []

            for index, memory in enumerate(memories,start=1):

                if isinstance(memory, dict):

                    category = memory.get("category", "unknown")

                    content = memory.get("content", str(memory))

                    importance = memory.get("importance", "—")

                    output.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n {index}. {category.upper()}\n\n {content}\n\n IMPORTANCE   {importance}\n")

                else:

                    output.append(f"{index}. {memory}\n\n")

            self.memory_view.setText("".join(output))

        except Exception as error:

            self.memory_summary.setText("Memory unavailable")
            self.memory_view.setText(f"Unable to retrieve memory.\n\n{error}")

    def create_computer_page(self):

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 26, 30, 26)
        layout.setSpacing(16)

        title = QLabel("COMPUTER")
        title.setObjectName("page_title")

        subtitle = QLabel("Approved computer resources available to Mahoraga.")
        subtitle.setObjectName("subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        grid = QGridLayout()
        grid.setSpacing(15)

        workspace_card = self.create_feature_card("WORKSPACES", "Approved folders that Mahoraga can access.", "OPEN WORKSPACE CONFIG")

        workspace_card.button.clicked.connect(self.show_workspace_config)

        apps_card = self.create_feature_card("APPLICATIONS", "Launch supported applications through Mahoraga.", "VIEW CAPABILITIES")

        apps_card.button.clicked.connect(lambda: self.switch_page(7, "Tools"))

        files_card = self.create_feature_card("FILES", "Search, list and read files inside approved workspaces.", "VIEW TOOLS")

        files_card.button.clicked.connect(lambda: self.switch_page(7, "Tools"))

        grid.addWidget(workspace_card, 0, 0)
        grid.addWidget(apps_card, 0, 1)
        grid.addWidget(files_card, 1, 0, 1, 2)

        layout.addLayout(grid)
        layout.addStretch()

        return page

    def refresh_computer(self):
        pass

    def show_workspace_config(self):

        path = Path("config/workspaces.json")

        if not path.exists():
            self.show_data_message("WORKSPACES", "No workspace configuration exists yet.")            
            return

        try:

            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
            text = json.dumps(data,indent=2)
            self.show_data_message("APPROVED WORKSPACES", text)
        except Exception as error:
            self.show_data_message("WORKSPACE ERROR", str(error))

    def create_browser_page(self):

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 26, 30, 26)
        layout.setSpacing(16)

        title = QLabel("BROWSER")
        title.setObjectName("page_title")

        subtitle = QLabel("Integrated browser control and page interaction.")
        subtitle.setObjectName("subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        browser_card = QFrame()
        browser_card.setObjectName("large_feature_card")

        browser_layout = QVBoxLayout(browser_card)
        browser_layout.setContentsMargins(25, 25, 25, 25)
        browser_layout.setSpacing(12)

        heading = QLabel("BROWSER CONTROL")
        heading.setObjectName("card_heading")

        browser_layout.addWidget(heading)

        description = QLabel("Mahoraga can open URLs, inspect page text, click links and navigate backwards using its browser tools.")
        description.setObjectName("card_description")
        description.setWordWrap(True)

        browser_layout.addWidget(description)

        status = QLabel("Browser engine: Playwright / Chromium")
        status.setObjectName("info_text")

        browser_layout.addWidget(status)

        browser_layout.addStretch()

        open_button = QPushButton("OPEN BROWSER")
        open_button.setObjectName("primary_button")

        open_button.clicked.connect(self.open_browser)

        browser_layout.addWidget(open_button)

        layout.addWidget(browser_card)

        layout.addStretch()

        return page

    def refresh_browser(self):
        pass

    def open_browser(self):

        try:

            browser_manager = None

            for attribute in dir(self.agent.tools):

                if "browser" in attribute.lower():
                    browser_manager = getattr(self.agent.tools, attribute, None)

            self.show_data_message("BROWSER","The browser is available through Mahoraga's "
                "browser tools.\n\n"
                "Try asking Mahoraga:\n\n"
                "“Open example.com”")
        except Exception as error:

            self.show_data_message("BROWSER",str(error))

    def create_devices_page(self):

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 26, 30, 26)
        layout.setSpacing(16)

        title = QLabel("HARDWARE")
        title.setObjectName("page_title")

        subtitle = QLabel("Registered devices and hardware interfaces.")
        subtitle.setObjectName("subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        top = QHBoxLayout()

        self.device_summary = QLabel("Loading devices...")
        self.device_summary.setObjectName("section_heading")

        top.addWidget(self.device_summary)
        top.addStretch()

        refresh = QPushButton("↻  REFRESH")
        refresh.setObjectName("secondary_button")
        refresh.clicked.connect(self.refresh_devices)

        top.addWidget(refresh)

        layout.addLayout(top)

        self.devices_view = QTextBrowser()
        self.devices_view.setObjectName("data_view")

        layout.addWidget(self.devices_view)

        return page

    def refresh_devices(self):

        path = Path("config/devices.json")

        if not path.exists():

            self.device_summary.setText("No device configuration")
            self.devices_view.setText("NO DEVICES REGISTERED\n\n Connect a device through Mahoraga's hardware tools.")
            return

        try:

            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, dict):
                devices = data.get("devices",data)
            else:
                devices = data

            if isinstance(devices, dict):
                device_items = list(devices.items())
            elif isinstance(devices, list):
                device_items = [(str(index + 1), device) for index, device in enumerate(devices)]
            else:
                device_items = []

            self.device_summary.setText(f"{len(device_items)} registered device(s)")
            if not device_items:

                self.devices_view.setText("NO REGISTERED DEVICES\n\n The hardware system is ready.")

                return

            output = []

            for name, device in device_items:

                output.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n {name}\n\n")

                if isinstance(device, dict):

                    for key, value in device.items():
                        output.append(f"{key.upper()}    {value}\n")

                else:

                    output.append(f"{device}\n")

                output.append("\n")

            self.devices_view.setText("".join(output))
        except Exception as error:

            self.device_summary.setText("Device system error")
            self.devices_view.setText(str(error))

    def create_tools_page(self):

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 26, 30, 26)
        layout.setSpacing(16)

        title = QLabel("TOOLS")
        title.setObjectName("page_title")

        subtitle = QLabel("Capabilities currently exposed to the AI orchestrator.")
        subtitle.setObjectName("subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        top = QHBoxLayout()

        self.tools_summary = QLabel("Loading tools...")
        self.tools_summary.setObjectName("section_heading")

        top.addWidget(self.tools_summary)
        top.addStretch()

        refresh = QPushButton("↻  REFRESH")
        refresh.setObjectName("secondary_button")
        refresh.clicked.connect(self.refresh_tools)

        top.addWidget(refresh)

        layout.addLayout(top)

        self.tools_view = QTextBrowser()
        self.tools_view.setObjectName("data_view")

        layout.addWidget(self.tools_view)

        return page

    def refresh_tools(self):

        try:
            declarations = self.agent.tools.declarations()

            self.tools_summary.setText(f"{len(declarations)} available tool(s)")
            if not declarations:
                self.tools_view.setText("NO TOOLS REGISTERED")
                return

            output = []

            for index, tool in enumerate(declarations,start=1):

                name = tool.get("name",f"Tool {index}")

                description = tool.get("description","No description available.")

                output.append(f"{index}. {name}\n\n {description}\n\n")

            self.tools_view.setText("".join(output))
        except Exception as error:

            self.tools_summary.setText("Tools unavailable")
            self.tools_view.setText(f"Unable to inspect tools.\n\n{error}")

    def create_settings_page(self):

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 26, 30, 26)
        layout.setSpacing(16)

        title = QLabel("SETTINGS")
        title.setObjectName("page_title")

        subtitle = QLabel("Runtime information and Mahoraga configuration.")
        subtitle.setObjectName("subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.settings_view = QTextBrowser()
        self.settings_view.setObjectName("data_view")

        layout.addWidget(self.settings_view)

        refresh = QPushButton("↻  REFRESH SYSTEM INFORMATION")
        refresh.setObjectName("secondary_button")
        refresh.clicked.connect(self.refresh_settings)

        layout.addWidget(refresh)

        return page

    def refresh_settings(self):

        try:

            from core.config import config

            model = getattr(config,"GEMINI_MODEL","Unknown")
            api_status = ("CONFIGURED" if getattr(config, "GEMINI_API_KEY", None) else "NOT CONFIGURED")
        except Exception:
            model = "Unknown"
            api_status = "Unknown"

        info = [
            "MAHORAGA SYSTEM INFORMATION",
            "",
            "────────────────────────────────",
            "",
            f"MODEL              {model}",
            f"GEMINI API         {api_status}",
            f"PYTHON             Runtime active",
            f"UI FRAMEWORK       PySide6",
            f"AI ENGINE           Gemini",
            f"MEMORY             Persistent",
            f"TASKS              Persistent",
            f"BROWSER            Playwright",
            f"HARDWARE           Serial / Device Manager",
            "",
            "────────────────────────────────",
            "",
            "CONFIGURATION",
            "",
            f"Workspace config   config/workspaces.json",
            f"Device config      config/devices.json",
            f"Task config        config/tasks.json",
            "",
            "SYSTEM STATUS",
            "",
            "● AI CORE           ONLINE",
            "● ORCHESTRATOR      ONLINE",
            "● UI                ONLINE",
        ]

        self.settings_view.setText("\n".join(info))

    def create_feature_card(self, title, description, button_text):

        card = QFrame()
        card.setObjectName("feature_card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        heading = QLabel(title)
        heading.setObjectName("card_heading")

        layout.addWidget(heading)

        description_label = QLabel(description)
        description_label.setObjectName("card_description")
        description_label.setWordWrap(True)

        layout.addWidget(description_label)

        layout.addStretch()

        button = QPushButton(button_text)
        button.setObjectName("secondary_button")

        layout.addWidget(button)

        card.button = button

        return card

    def show_data_message(self, title, text):

        dialog = QMessageBox(self)
        dialog.setWindowTitle(title)
        dialog.setText(text)
        dialog.setStandardButtons(QMessageBox.Ok)
        dialog.exec()

    def refresh_all_pages(self):

        self.refresh_tasks()
        self.refresh_memory()
        self.refresh_devices()
        self.refresh_tools()
        self.refresh_settings()

        try:
            memory_count = len(self.agent.memory.recall() or [])
        except Exception:

            memory_count = 0

        try:

            tasks_path = Path("config/tasks.json")

            if tasks_path.exists():

                with open(tasks_path,"r",encoding="utf-8") as file:
                    task_data = json.load(file)

                if isinstance(task_data, dict):
                    tasks = task_data.get("tasks", task_data)
                else:
                    tasks = task_data

                task_count = (len(tasks) if isinstance(tasks, (list, dict)) else 0)

            else:

                task_count = 0

        except Exception:

            task_count = 0

        try:

            devices_path = Path("config/devices.json")
            if devices_path.exists():

                with open(devices_path, "r", encoding="utf-8") as file:

                    device_data = json.load(file)

                if isinstance(device_data, dict):
                    devices = device_data.get("devices", device_data)
                else:
                    devices = device_data

                device_count = len(devices)

            else:

                device_count = 0

        except Exception:

            device_count = 0

        try:

            tool_count = len(self.agent.tools.declarations())
        except Exception:

            tool_count = 0

        self.stat_memory.value_label.setText(str(memory_count))

        self.stat_tasks.value_label.setText(str(task_count))

        self.stat_devices.value_label.setText(str(device_count))

        self.stat_tools.value_label.setText(str(tool_count))

        try:

            from core.config import config

            self.dashboard_model.setText(f"Model: {config.GEMINI_MODEL}")
        except Exception:

            self.dashboard_model.setText("Model: Unknown")
        self.dashboard_runtime.setText("Runtime: Python / PySide6")


    def setup_worker(self):

        self.thread = QThread()

        self.worker = AgentWorker()

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.initialize)

        self.chat_page.message_sent.connect(self.worker.process)

        self.worker.finished.connect(self.handle_response)

        self.worker.error.connect(self.handle_error)

        self.thread.start()
    def confirm_exit(self):

        result = QMessageBox.question(self, "Exit Mahoraga", "Are you sure you want to exit Mahoraga?",QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if result == QMessageBox.Yes:
            self.close()

    @Slot(str)
    def handle_response(self, response):

        self.chat_page.add_ai_message(response)

        self.set_system_status("READY")

        self.chat_page.setThinking(False)
        self.chat_page.inputBox.setEnabled(True)
        self.chat_page.send_button.setEnabled(True)

    @Slot(str)
    def handle_error(self, error):

        self.chat_page.add_system_message(f"Error: {error}")

        self.set_system_status("ERROR")

        self.chat_page.setThinking(False)
        self.chat_page.inputBox.setEnabled(True)
        self.chat_page.send_button.setEnabled(True)

    def set_system_status(self, status):

        self.header_status.setText(status)
        self.bottom_status.setText(f"● {status}")
        self.sidebar_status_detail.setText(status.lower().capitalize())

        if status == "ERROR":

            self.header_status_dot.setProperty("state","error")

        else:
            self.header_status_dot.setProperty("state", "normal")

        self.header_status_dot.style().unpolish(self.header_status_dot)

        self.header_status_dot.style().polish(self.header_status_dot)
    def closeEvent(self, event):
        print("Shutting down Mahoraga")
        if hasattr(self, "thread"):
            self.thread.quit()
            self.thread.wait()
        event.accept()