import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.logger import Logger
from core.analyzer import Analyzer
from core.alert_manager import AlertManager

class WinnieApp:
    def __init__(self):
        # Create components in the correct order
        self.analyzer = Analyzer()  # Create analyzer first
        self.logger = Logger(self.analyzer)  # Pass analyzer to logger
        self.alert_manager = AlertManager()
        
        # Create main window
        self.main_window = MainWindow(self.logger, self.analyzer, self.alert_manager)
        self.main_window.show()

def main():
    app = QApplication(sys.argv)
    winnie = WinnieApp()
    return app.exec()

if __name__ == "__main__":
    main() 