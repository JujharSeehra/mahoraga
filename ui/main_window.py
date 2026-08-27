from PySide6.QtWidgets import ( QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QStackedWidget)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self, agent):
        super().__init__()

        self.agent = agent

        self.setWindowTitle("<b>Mahoraga</b>")
        self.setMinimumSize(1100, 700)

        self.build_ui()

    def build_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)


        sidebar = QFrame()
        sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)

        title = QLabel("<b>MAHORAGA</b>")
        title.setObjectName("title")

        sidebar_layout.addWidget(title)

        sidebar_layout.addSpacing(30)

        self.chat_button = QPushButton("Chat")
        self.dashboard_button = QPushButton("Dashboard")
        self.memory_button = QPushButton("Memory")
        self.devices_button = QPushButton("Devices")
        self.tools_button = QPushButton("Tools")
        self.settings_button = QPushButton("Settings")

        buttons = [self.chat_button,self.dashboard_button,self.memory_button,self.devices_button,self.tools_button,self.settings_button]

        for button in buttons:
            button.setMinimumHeight(45)
            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()

        status = QLabel("● ONLINE")
        status.setAlignment(Qt.AlignCenter)
        status.setObjectName("status")

        sidebar_layout.addWidget(status)


        self.pages = QStackedWidget()

        self.pages.addWidget(self.create_chat_page())
        self.pages.addWidget(self.create_dashboard_page())
        self.pages.addWidget(self.create_memory_page())
        self.pages.addWidget(self.create_devices_page())
        self.pages.addWidget(self.create_tools_page())
        self.pages.addWidget(self.create_settings_page())

        self.chat_button.clicked.connect(lambda: self.pages.setCurrentIndex(0))

        self.dashboard_button.clicked.connect(lambda: self.pages.setCurrentIndex(1))

        self.memory_button.clicked.connect(lambda: self.pages.setCurrentIndex(2))

        self.devices_button.clicked.connect(lambda: self.pages.setCurrentIndex(3))

        self.tools_button.clicked.connect(lambda: self.pages.setCurrentIndex(4))

        self.settings_button.clicked.connect(lambda: self.pages.setCurrentIndex(5))

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages)


    def create_chat_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Mahoraga")
        title.setObjectName("page_title")

        subtitle = QLabel("The Eight Handled Sword Divergent Sila Divine General")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addStretch()

        message = QLabel("Chat interface coming next.")

        message.setAlignment(Qt.AlignCenter)

        layout.addWidget(message)

        layout.addStretch()

        return page

    def create_dashboard_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Dashboard")
        title.setObjectName("page_title")

        layout.addWidget(title)

        info = QLabel("Mahoraga system status will appear here.")

        layout.addWidget(info)
        layout.addStretch()

        return page

    def create_memory_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Memory")
        title.setObjectName("page_title")

        layout.addWidget(title)

        info = QLabel("Long-term and episodic memory will appear here.")
        layout.addWidget(info)
        layout.addStretch()

        return page

    def create_devices_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Devices")
        title.setObjectName("page_title")

        layout.addWidget(title)

        info = QLabel("Connected hardware will appear here.")

        layout.addWidget(info)
        layout.addStretch()

        return page

    def create_tools_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Tools")
        title.setObjectName("page_title")

        layout.addWidget(title)

        info = QLabel("Mahoraga capabilities will appear here.")

        layout.addWidget(info)
        layout.addStretch()

        return page

    def create_settings_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Settings")
        title.setObjectName("page_title")

        layout.addWidget(title)

        info = QLabel("Mahoraga configuration will appear here.")

        layout.addWidget(info)
        layout.addStretch()

        return page