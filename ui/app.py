import sys
from pathlib import Path
from PySide6.QtWidgets import (QApplication)
from core.agent import (MahoragaAgent)
from ui.main_window import (MainWindow)
def run():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    stylesheet_path = (Path(__file__).parent / "mahoraga.qss")

    with open(stylesheet_path,"r",encoding="utf-8") as file: 
        app.setStyleSheet(file.read())
    agent = MahoragaAgent()
    window = MainWindow(agent)
    window.show()
    sys.exit(app.exec())