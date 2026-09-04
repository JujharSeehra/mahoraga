import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL","gemini-3.7-flash")
    WORKSPACE = Path.home() / "MahoragaWorkspace"
    APP_NAME = "Mahoraga"

    DEBUG = True
    @classmethod
    def initialize(cls):
        cls.WORKSPACE.mkdir(parents=True, exist_ok=True)


config = Config()
config.initialize()