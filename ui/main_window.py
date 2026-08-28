from PySide6.QtWidgets import ( QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QStackedWidget)
from PySide6.QtCore import (Qt, QThread, Slot)
from core.worker import AgentWorker
from ui.chat import ChatPage


class MainWindow(QMainWindow):

    def __init__(self, agent):
        super().__init__()

        self.agent = agent

        self.setWindowTitle("Mahoraga")
        self.setMinimumSize(1100, 700)

        self.build_ui()
        self.setup_worker()

    def build_ui(self):
    
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
    
    
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
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
        sidebar_layout.addStretch()
        self.settings_button = QPushButton("Settings")
        self.exit_button = QPushButton("EXIT")
        self.exit_button.clicked.connect(self.close)

        buttons = [self.chat_button,self.dashboard_button,self.memory_button,self.devices_button,self.tools_button,self.settings_button, self.exit_button]
    
        for button in buttons:
            button.setMinimumHeight(45)
            sidebar_layout.addWidget(button)
    
        sidebar_layout.addStretch()
    
        status = QLabel("● ONLINE")
        status.setAlignment(Qt.AlignCenter)
        status.setObjectName("status")
    
        sidebar_layout.addWidget(status)
    
    
        self.pages = QStackedWidget()
        self.chat_page = ChatPage()
        self.pages.addWidget(self.chat_page)
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
    def setup_worker(self):

        self.thread = QThread()
        self.worker = AgentWorker(self.agent)
        self.worker.moveToThread(self.thread)
        self.chat_page.message_sent.connect(self.worker.process)
        self.worker.finished.connect(self.handle_response)
        self.worker.error.connect(self.handle_error) 
        self.thread.start()


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
    def closeEvent(self, event):
        print("Shutting down Mahoraga")
        if hasattr(self, "thread"):
            self.thread.quit()
            self.thread.wait()
        event.accept()
    @Slot(str)
    def handle_response(self, response):
        self.chat_page.add_ai_message(response)
        self.chat_page.setThinking(False)
        self.chat_page.inputBox.setEnabled(True)
        self.chat_page.send_button.setEnabled(True)
    @Slot(str)
    def handle_error(self, error):
        self.chat_page.add_system_message(f"Error: {error}")
        self.chat_page.setThinking(False)
        self.chat_page.inputBox.setEnabled(True)
        self.chat_page.send_button.setEnabled(True)