import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.logger import Logger
from core.analyzer import Analyzer
from core.alert_manager import AlertManager

class WinnieApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.logger = Logger()
        self.analyzer = Analyzer()
        self.alert_manager = AlertManager()
        self.main_window = MainWindow(self.logger, self.analyzer, self.alert_manager)

    def run(self):
        self.main_window.show()
        return self.app.exec()

if __name__ == "__main__":
    winnie = WinnieApp()
    sys.exit(winnie.run()) 