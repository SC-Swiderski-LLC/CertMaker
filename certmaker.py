import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow


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
