from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel)
from PySide6.QtCore import Qt, Signal, Slot
from ui.widgets.wheel import (MahoragaWheel)
from core.state import MahoragaState
class ChatPage(QWidget):
    message_sent = Signal(str)
    def __init__(self):
        super().__init__()
        self.build_ui()
    def build_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("Mahoraga")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Eight Handled Sword Divergent Sila Divine General")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.wheel = MahoragaWheel()
        self.wheel.setMaximumHeight(280)
        self.wheel.setMinimumHeight(220)
        layout.addWidget(self.wheel, alignment = Qt.AlignCenter)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setPlaceholderText("Your conversation with Mahoraga will appear here.")

        layout.addWidget(self.chat_display)

        inputLayout = QHBoxLayout()
        self.inputBox = QLineEdit()

        self.inputBox.setPlaceholderText("Message Mahoraga")
        self.send_button = QPushButton("Send Message")

        inputLayout.addWidget(self.inputBox)
        inputLayout.addWidget(self.send_button)
        layout.addLayout(inputLayout)

        self.send_button.clicked.connect(self.send_message)
        self.inputBox.returnPressed.connect(self.send_message)

    @Slot()
    def send_message(self):
        message = self.inputBox.text().strip()

        if not message:
            return

        self.add_user_message(message)
        self.inputBox.clear()
        self.setThinking(True)
        self.message_sent.emit(message)
    def add_user_message(self, message):
        self.chat_display.append(f"<b>You:</b> {message}")
    def add_ai_message(self, message):
        self.chat_display.append(f"<b>Mahoraga:</b> {message}")
    def add_system_message(self, message):
        self.chat_display.append(f"<i>System: {message}</i>")
    def setThinking(self, thinking):
        if thinking:
            self.wheel.set_state(MahoragaState.THINKING)
            self.send_button.setEnabled(False)
            self.inputBox.setEnabled(False)
            self.send_button.setText("Thinking...")
        else:
            self.wheel.set_state(MahoragaState.IDLE)
            self.send_button.setEnabled(True)
            self.inputBox.setEnabled(True)
            self.send_button.setText("Send")