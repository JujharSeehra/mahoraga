import sys
from pathlib import Path
from PySide6.QtWidgets import (QApplication)
from core.agent import (MahoragaAgent)
from ui.main_window import (MainWindow)
import os
from dotenv import load_dotenv
from PySide6.QtWidgets import QInputDialog, QLineEdit, QMessageBox
def run():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    stylesheet_path = (Path(__file__).parent / "mahoraga.qss")

    with open(stylesheet_path,"r",encoding="utf-8") as file: 
        app.setStyleSheet(file.read())
    app_support = Path.home() / "Library" / "Application Support" / "Mahoraga"
    app_support.mkdir(parents=True, exist_ok=True)

    env_path = app_support / ".env"
    load_dotenv(env_path)
    if not os.getenv("GEMINI_API_KEY"):
        load_dotenv()
    if not os.getenv("GEMINI_API_KEY"):
        api_key, ok = QInputDialog.getText(
            None,
        "Gemini API Key",
        "Enter your Gemini API key:",
        QLineEdit.Password,)

        if not ok or not api_key.strip():
            QMessageBox.critical(None, "API Key Required", "Mahoraga requires a Gemini API key to run.")
            return
        api_key = api_key.strip()
        env_path.write_text(f"GEMINI_API_KEY={api_key}\n", encoding="utf-8")
        os.environ["GEMINI_API_KEY"] = api_key
    agent = MahoragaAgent()
    window = MainWindow(agent)
    window.show()
    sys.exit(app.exec())