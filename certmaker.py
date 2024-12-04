import sys
import os
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import Qt

# Enable DPI scaling for high-resolution displays
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QGuiApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

def main():
    """Main function to run CertMaker."""
    # Create the application instance
    app = QApplication(sys.argv)

    # Set a consistent style (optional, but makes it look better)
    app.setStyle("Fusion")

    # Create and display the main window
    window = MainWindow()
    window.show()

    # Handle application exit
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("CertMaker exited cleanly.")

if __name__ == "__main__":
    main()
