import sys

from PySide6.QtWidgets import QApplication

from core.agent import MahoragaAgent
from ui.main_window import MainWindow


def run():

    app = QApplication(sys.argv)

    agent = MahoragaAgent()

    window = MainWindow(agent)

    window.show()

    sys.exit(app.exec())