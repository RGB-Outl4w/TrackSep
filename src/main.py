import sys
import os
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from ui.main_window import MainWindow
from ui.log_widget import LogWidget
from backend.log_handler import LogHandler
from backend.settings import Settings

def main():
    # Initialize the application
    app = QApplication(sys.argv)

    # Initialize settings
    settings = Settings()

    # Apply theme from settings
    theme = settings.get("theme")
    app.setStyle(theme)
    if settings.get("dark_mode") == "true":
        from PyQt5.QtGui import QPalette, QColor
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        app.setPalette(palette)

    # Set the application icon
    icon_path = os.path.join(os.path.dirname(__file__), "../assets/icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('tracksep.log'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)

    # Create log widget and handler
    log_widget = LogWidget()
    log_handler = LogHandler(log_widget)
    logger.addHandler(log_handler)

    # Create main window and pass settings
    window = MainWindow()
    window.log_widget = log_widget  # Attach the log widget
    window.settings = settings      # Pass settings to the main window
    window.show()

    # Start the application
    logger.info("Track Separator application started.")
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
